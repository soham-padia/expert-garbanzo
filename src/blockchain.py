# src/blockchain.py
import time
from .block import Block
from .parameters import *

class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), "0")
        self.chain.append(genesis_block)

    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def mine(self, miner_id):
        last_block = self.chain[-1]
        new_block = Block(index=last_block.index + 1,
                          transactions=self.pending_transactions,
                          timestamp=time.time(),
                          previous_hash=last_block.hash)
        self.chain.append(new_block)
        self.pending_transactions = []
        return new_block
