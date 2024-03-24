from os import environ
import logging
import requests
from util import hex2str,str2hex
from rental import Item
import json

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

items = {}
owner_items = {}
next_id = 0

rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]
logger.info(f"HTTP rollup_server url is {rollup_server}")

def add_report(output=""):
    logger.info("Adding report " + output)
    report = {"payload": str2hex(output)}
    response = requests.post(rollup_server + "/report", json=report)
    logger.info(f"Received report status {response.status_code}")

def add_notice(data):
    logger.info(f"Adding notice {data}")
    notice = {"payload": str2hex(data)}
    response = requests.post(rollup_server + "/notice", json=notice)
    logger.info(f"Received notice status {response.status_code} body {response.content}")

def handle_advance(data):
    
    try:
        payload = json.loads(hex2str(data["payload"]))
    except:
        logger.info(f"Rejected")
        return "reject"
    method = payload.get("method")
    sender = data["metadata"]["msg_sender"]
    logger.info(f"Received advance request data {payload}")

    handler = adv_handlers.get(method)
    if not handler:
        add_report("Invalid method")
        return "reject"

    return handler(payload,sender)

def rentItem(payload,sender):
    # item = payload.get("item")
    item_id = payload.get("item_id")
    item_id = int(item_id)
    if not item_id:
        add_report("ItemID not present")
    
    item = items.get(item_id)
    
    if not item:
        add_report("Item not present")
        return "reject"
    
    item.addRenter(sender)
    add_notice(f"item with id {next_id} was rented by {sender}")

    return "accept"

def addItem(payload,sender):
    global next_id
    item = payload.get("item")
    if not item:
        add_report("No item")
        return "reject"
    
    i = Item(owner_addr=sender, price=item["price"],duration=item["duration"],_id = next_id,rating=item["rating"])
    items[next_id] = i
    if sender not in owner_items:
        owner_items[sender] = [next_id]
    else:
        owner_items[sender].append(next_id)

    add_notice(f"item with id {next_id} was added by {sender}")
    next_id+=1
    return "accept"

def getItems():
    item_keys  = items.keys()
    items_list = []
    for key in item_keys:
        item = items.get(key)
        items_list.append({
            "owner": item.owner_addr,
            "price": item.price,
            "duration": item.duration,
            "_id": item.id,
            "rating": item.rating,
            "renter": item.renter_addr,
            "status": item.status
        })
    output = json.dumps({"items": items_list})
    add_report(output=output)
    return "accept"


def handle_inspect(data):
    try:
        payload = json.loads(hex2str(data["payload"]))
    except:
        return "reject"
    method = payload.get("method")
    logger.info(f"Received inspect request data {payload}")

    handler = ins_handlers.get(method)
    if not handler:
        add_notice("Invalid method")
        return "reject"

    return handler()

handlers = {
    "advance_state": handle_advance,
    "inspect_state": handle_inspect,
}

adv_handlers = {
    "rentItem": rentItem,
    "addItem": addItem
}
ins_handlers = {
    "getItems": getItems
}

# Advance
# Rent or add item

# Inspect
# get all items

finish = {"status": "accept"}

while True:
    logger.info("Sending finish")
    response = requests.post(rollup_server + "/finish", json=finish)
    logger.info(f"Received finish status {response.status_code}")
    if response.status_code == 202:
        logger.info("No pending rollup request, trying again")
    else:
        rollup_request = response.json()
        data = rollup_request["data"]
        
        handler = handlers[rollup_request["request_type"]]
        finish["status"] = handler(rollup_request["data"])
