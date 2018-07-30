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
