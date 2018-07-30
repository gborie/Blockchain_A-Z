# Module 2 - Create a Cryptocurrency

# Each block will have its own timestamp
import datetime
# Hash the blocks
import hashlib
# Encode blocks before hashing them
import json
# Web application with Flask, return messages in Postman with jsonify
# And request module to connect the nodes in our decentralized network
from flask import Flask, jsonify, request
# Needed when checking chains of nodes
import requests
# Create an address for each nodes in network
from uuid import uuid4
# Parse url of each of the nodes
from urllib.parse import urlparse


# Part 1 - Building a Blockchain
class Blockchain:

    def __init__(self):
        self.chain = []
        # chain containing the transactions initialized as an empty list
        self.transactions = []
        self.create_block(proof = 1, previous_hash = '0')
        # nodes initialized as an empty set
        self.nodes = set()

    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 # transactions key added to block
                 'transactions': self.transactions}
        # self.transactions added to method
        self.transactions = []
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True

    # Method to add transactions to transactions list with sender, receiver and amount arguments
    # And return the index of the new block
    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({'sender': sender,
                                  'receiver': receiver,
                                  'amount': amount})
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1

    # Method to add a node to the nodes set with self and address as arguments
    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    # Replace any chain shorter than longest chain among nodes on network
    def replace_chain(self):
        # network contains all the nodes
        network = self.nodes
        longest_chain = None
        # Compare length of chains of all the nodes to find longest one
        max_length = len(self.chain)
        # Iterate over the nodes in the network to find longest chain
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False
