import hashlib
import time

class Item:
    def __init__(self,owner_addr, price, duration, _id, rating, status="available"):
        self.owner_addr = owner_addr
        self.renter_addr = None
        self.price = price
        self.duration = duration
        self.id = _id
        self.status = status
        self.rating = rating
    
    def addRenter(self,addr):
        if self.status == "available":
            self.renter_addr = addr
            self.status = "rented"
        else:
            return
        

