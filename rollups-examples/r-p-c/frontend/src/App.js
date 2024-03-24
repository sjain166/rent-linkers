import "./App.css";
import React, { useState, useEffect } from "react";
import { ethers } from "ethers";
import ProductForm from "./ProductForm";

function App() {
    const [signer, setSigner] = useState(undefined);

    useEffect(() => {
        if (window.ethereum === "undefined")
            return alert("You need metamask to use this application");

        try {
            window.ethereum
                .request({ method: "eth_requestAccounts" })
                .then(() => {
                    const provider = new ethers.providers.Web3Provider(
                        window.ethereum
                    );
                    const signerr = provider.getSigner();
                    console.log("Signer: ",signerr)
                    setSigner(signerr);
                });
        } catch (error) {
            console.log(error);
            alert("Connecting to metamask failed.");
        }
    }, []);

    return (
        <div className="App">
            <div>
                <ProductForm wallet={signer} />
            </div>
            {/* <div>
                <ListChallenges signer={signer} />
            </div> */}
        </div>
    );
}

export default App;