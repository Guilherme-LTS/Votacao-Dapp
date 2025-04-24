import hashlib
import json
from time import time
from urllib.parse import urlparse
import requests

class Blockchain:
    def __init__(self):
        self.chain = []
        self.transacoes = []
        self.nodes = set()
        self.criar_bloco_genesis()

    def criar_bloco_genesis(self):
        self.criar_bloco(nonce=1, hash_anterior='0')

    def criar_bloco(self, nonce, hash_anterior):
        bloco = {
            'indice': len(self.chain) + 1,
            'timestamp': time(),
            'transacoes': self.transacoes.copy(),
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
        bloco_temp = bloco.copy()
        bloco_temp.pop('hash', None)
        bloco_serializado = json.dumps(bloco_temp, sort_keys=True).encode()
        return hashlib.sha256(bloco_serializado).hexdigest()

    def proof_of_work(self, hash_anterior):
        nonce = 0
        while True:
            bloco = {
                'indice': len(self.chain) + 1,
                'timestamp': time(),
                'transacoes': self.transacoes,
                'nonce': nonce,
                'hash_anterior': hash_anterior
            }
            hash_valido = self.hash_bloco(bloco)
            if hash_valido.startswith('0000'):
                return nonce
            nonce += 1

    def minerar(self):
        hash_anterior = self.chain[-1]['hash']
        nonce = self.proof_of_work(hash_anterior)
        bloco = self.criar_bloco(nonce, hash_anterior)
        return bloco

    def registrar_node(self, endereco):
        parsed = urlparse(endereco)
        if parsed.netloc:
            self.nodes.add(parsed.netloc)
        elif parsed.path:
            self.nodes.add(parsed.path)

    def validar_cadeia(self, cadeia):
        if not cadeia:
            return False
        for i in range(1, len(cadeia)):
            anterior = cadeia[i - 1]
            atual = cadeia[i]
            if atual['hash_anterior'] != self.hash_bloco(anterior):
                return False
            if not self.hash_bloco(atual).startswith('0000'):
                return False
        return True

    def resolver_conflitos(self):
        nova_cadeia = None
        max_len = len(self.chain)

        for node in self.nodes:
            try:
                resposta = requests.get(f'http://{node}/chain')
                if resposta.status_code == 200:
                    cadeia = resposta.json()['chain']
                    if len(cadeia) > max_len and self.validar_cadeia(cadeia):
                        max_len = len(cadeia)
                        nova_cadeia = cadeia
            except Exception as e:
                print(f"Erro ao conectar com {node}: {e}")
                continue

        if nova_cadeia:
            self.chain = nova_cadeia
            return True

        return False

    def resultados_votacao(self):
        resultados = {}
        for bloco in self.chain:
            for tx in bloco['transacoes']:
                candidato = tx['candidato']
                resultados[candidato] = resultados.get(candidato, 0) + 1
        return resultados
