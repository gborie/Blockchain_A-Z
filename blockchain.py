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
        # Create genesis block calling the function create_block that takes 2 arguments:
        ## proof with arbitrary value of 1
        ## previous_hash with arbitrary value of '0' as genesis block and using quotes to work with SHA-256
        self.create_block(proof = 1, previous_hash = '0')
