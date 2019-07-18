import hashlib
import requests
import json
import os

import sys

# TODO: Implement functionality to search for a proof 
def valid_proof(last_proof, proof):
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:4] == "0000"

def proof_of_work(last_proof):
    print("Searching for next proof")
    proof = 0
    while valid_proof(last_proof, proof) is False:
        proof += 1
    print("Proof found: " + str(proof))
    return proof

if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    # Run forever until interrupted
    while True:
        # TODO: Get the last proof from the server and look for a new one
        last_proof = requests.get(f"{node}/last-proof").text
        new_proof = proof_of_work(last_proof)
        # TODO: When found, POST it to the server {"proof": new_proof}
        response = requests.post(f"{node}/mine", data=json.dumps({'proof': new_proof}), headers={'content-type': 'application/json'}).json()
        message, transactions = response["message"], response["transactions"]
        # TODO: If the server responds with 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
        if message == "New Block Forged":
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(message)
