import hashlib
import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.difficulty = 4
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = {
            'index': 0,
            'timestamp': time.ctime(),
            'data': 'Genesis Block',
            'previous_hash': '0',
            'nonce': 0,
            'hash': self.calculate_hash(0, 'Genesis Block', '0', 0, []),
            'transactions': [],
            'valid': True
        }
        self.chain.append(genesis_block)

    def calculate_hash(self, index, data, prev_hash, nonce, transactions):
        block_string = f"{index}{data}{prev_hash}{nonce}{transactions}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def add_block(self, transactions):
        prev = self.chain[-1]
        index = prev['index'] + 1
        prev_hash = prev['hash']
        nonce = 0

        # proof-of-work
        while True:
            h = self.calculate_hash(index, "Transaction Block", prev_hash, nonce, transactions)
            if h.startswith("0" * self.difficulty):
                break
            nonce += 1

        block = {
            'index': index,
            'timestamp': time.ctime(),
            'data': 'Transaction Block',
            'previous_hash': prev_hash,
            'nonce': nonce,
            'hash': h,
            'transactions': transactions,
            'valid': True
        }
        self.chain.append(block)
        self.validate_chain()

    def tamper_block(self, index):
        if index == 0 or index >= len(self.chain):
            return False
        # **Only change data** — do NOT recompute hash or nonce
        blk = self.chain[index]
        if blk['transactions']:
            blk['transactions'][0]['amount'] += 9999
            # leave blk['hash'] as-is → data ≠ hash now
            self.validate_chain()
            return True
        return False

    def validate_chain(self):
        for i, blk in enumerate(self.chain):
            # 1) data integrity check
            expected = self.calculate_hash(
                blk['index'], blk['data'], blk['previous_hash'],
                blk['nonce'], blk['transactions']
            )
            if blk['hash'] != expected:
                blk['valid'] = False
                continue

            # 2) link check (skip genesis)
            if i > 0 and blk['previous_hash'] != self.chain[i-1]['hash']:
                blk['valid'] = False
            else:
                blk['valid'] = True
