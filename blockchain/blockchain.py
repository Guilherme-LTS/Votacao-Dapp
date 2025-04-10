import hashlib
import json
from time import time
from blockchain.voto import Voto

class Blockchain:
    def __init__(self):
        self.chain = []
        self.transacoes = []
        self.criar_bloco(genesis=True)

    def criar_bloco(self, nonce=1, hash_anterior='0', genesis=False):
        bloco = {
            'indice': len(self.chain) + 1,
            'timestamp': time(),
            'transacoes': self.transacoes if not genesis else [],
            'nonce': nonce,
            'hash_anterior': hash_anterior
        }
        bloco['hash'] = self.hash_bloco(bloco)
        self.transacoes = []
        self.chain.append(bloco)
        return bloco

    def adicionar_voto(self, voto):
        self.transacoes.append(voto.to_dict())

    def hash_bloco(self, bloco):
        bloco_serializado = json.dumps(bloco, sort_keys=True).encode()
        return hashlib.sha256(bloco_serializado).hexdigest()

    def get_chain(self):
        return self.chain
