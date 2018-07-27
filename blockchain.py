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
