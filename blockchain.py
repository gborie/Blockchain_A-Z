# Module 1 - Create a Blockchain

# Each block will have its own timestamp
import datetime
# Hash the blocks
import hashlib
# Encode blocks before hashing them
import json
# Web application with Flask and return messages in Postman with jsonify
from flask import Flask, jsonify


# Part 1 - Building a Blockchain

class Blockchain:

    # Always start with the init method that will take self as an argument
    # Self refers to the object that we will create once the class is made
    # Once we create a class we can make as many objects as we want
    def __init__(self):
        # Initialize the chain containing the blocks as an empty list
        self.chain = []
        # Create genesis block calling the method create_block that takes 2 arguments:
        ## proof with arbitrary value of 1
        ## previous_hash with arbitrary value of '0' as genesis block and using quotes to work with SHA-256
        self.create_block(proof = 1, previous_hash = '0')

    # Method to create genesis block and next blocks once mined
    # The create_block method is applied right after mining a block
    def create_block(self, proof, previous_hash):
        # Block stored in a dict with 4 keys: index, timestamp - exact time when block is mined,
        # proof - found when block mined, and previous_hash
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()), # Use string to avoid formatting issues
                 'proof': proof,
                 'previous_hash': previous_hash}
        # Append block to self.chain list
        self.chain.append(block)
        # Return block to display the 4 keys of this block in Postman
        return block

    # Method to get the last block of the current chain
    def get_previous_block(self):
        return self.chain[-1]

    # proof_of_work is the number that miners have to find to mine a new block
    # Problem challanging to solve so it does not lose value (cryptoccy) but easy to verify
    def proof_of_work(self, previous_proof):
        # new_proof initialized to 1
        new_proof = 1
        # check_proof inialized to false
        check_proof = False
        # while loop as long as check_proof is False
        while check_proof is False:
            # hash_operation non symetrical operation with new_proof**2 - previous_proof**2
            # encode method to encode string in right format expected by SHA-256
            # hexdigest to get hexadecimal characters
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            # The more leading zeros the harder to mine the block. Bitcoin is using 18 zeros
            if hash_operation[:4] == '0000':
                # Miner win and check_proof updated to True
                check_proof = True
            else:
                # Miner don't win and try again with new_proof incremented by 1
                new_proof += 1
        # return new_proof if miner win
        return new_proof

    # We need to check if everything is right in our blockchain to make sure we have a valid Blockchain
    ## First we make a hash method that will return the SHA256 cryptographic hash of an input(block)
    def hash(self, block):
        # We use json library to make object a string with dumps method
        # It takes 2 arguments, block and sort_keys = True so the block is sorted by the keys
        encoded_block = json.dumps(block, sort_keys = True).encode()
        # We return the cryptographic hash of our block
        return hashlib.sha256(encoded_block).hexdigest()

    ## Check 1 - Check previous_hash of each block is equal to the hash of the previous block
    ## Check 2 - Check if each block in the blockchain has a correct proof_of_work - return cryptographic hash starting with '0000'
    def is_chain_valid(self, chain):
        # Initialize variables of the loop
        previous_block = chain[0] # First block of the chain
        block_index = 1 # Each block has the index key in the dict. First block starts at index = 1
        # While loop to iterate over all the block in the chain
        while block_index < len(chain):
            # Check 1: previous hash valid
            block = chain[block_index]
            # if 'previous_hash' key in current block is different than hash of previous block return false as chain non-valid
            if block['previous_hash'] != self.hash(previous_block):
                return False
            # Check 2: proof of work valid
            previous_proof = previous_block['proof'] # Take previous proof
            proof = block['proof'] # Take current proof
            # Compute hash_operation
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            # Check hash-operation starts with '0000' or return false
            if hash_operation[:4] != '0000':
                return False
            # Update variables of the loop for next while loop iteration
            previous_block = block
            block_index += 1
        # Returns True if everything is right in our blockchain or no False returned
        return True


# Part 2 - Mining our Blockchain

# Creating a Web App
# Create app object from Flask class imported at the top
app = Flask(__name__)

# Creating a Blockchain
blockchain = Blockchain()

# Mining a new block via GET request
@app.route('/mine_block', methods = ['GET'])
# Get method to get something like a block and post method to create something like transactions
# mine_block function doesn't take arguments
def mine_block():
    # Get the previous proof from previous block for proof_of_work method
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    # call proof_of_work method with previous_proof as argument to get the proof for new block
    proof = blockchain.proof_of_work(previous_proof)
    # Get previous_hash needed for hash method
    previous_hash = blockchain.hash(previous_block)
    # Call create_block method with proof and previous_hash arguments
    block = blockchain.create_block(proof, previous_hash)
    # Display response to Get request with all info of block + congrats message in json format
    response = {'message': 'Congratulations, you just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    # Return response using jsonify function and http status code 200
    return jsonify(response), 200

# Getting the full Blockchain and length via GET request
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

# Running the app
# Call run method from app object with 2 arguments: host and Port
# host '0.0.0.0' to make the server publicly available
app.run(host = '0.0.0.0', port = 5000)
