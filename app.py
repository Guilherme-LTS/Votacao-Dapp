from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from blockchain.blockchain import Blockchain
from blockchain.voto import Voto
from blockchain.eleitor import ControleEleitores

app = Flask(__name__)
CORS(app)

blockchain = Blockchain()
controle = ControleEleitores()

@app.route('/')
def index():
    return send_from_directory('frontend', 'index.html')

@app.route('/frontend/<path:filename>')
def frontend_static(filename):
    return send_from_directory('frontend', filename)

@app.route('/votar', methods=['POST'])
def votar():
    dados = request.get_json()
    eleitor_id = dados.get('eleitor_id')
    candidato = dados.get('candidato')

    if controle.ja_votou(eleitor_id):
        return jsonify({'mensagem': 'Eleitor já votou!'}), 403

    voto = Voto(eleitor_id, candidato)
    blockchain.adicionar_voto(voto)
    controle.registrar_voto(eleitor_id)

    return jsonify({'mensagem': 'Voto registrado com sucesso'}), 200

@app.route('/minerar', methods=['GET'])
def minerar():
    bloco = blockchain.minerar()
    return jsonify({'mensagem': 'Bloco minerado com sucesso', 'bloco': bloco}), 200

@app.route('/chain', methods=['GET'])
def chain():
    return jsonify({'chain': blockchain.chain}), 200

@app.route('/resultados', methods=['GET'])
def resultados():
    return jsonify({'resultados': blockchain.resultados_votacao()}), 200

@app.route('/nodes/register', methods=['POST'])
def registrar_nos():
    dados = request.get_json()
    nodes = dados.get('nodes')
    if not nodes:
        return jsonify({'mensagem': 'Lista de nós está vazia'}), 400
    for node in nodes:
        blockchain.registrar_node(node)
    return jsonify({'mensagem': 'Nós registrados', 'nodes': list(blockchain.nodes)}), 201

@app.route('/nodes/resolve', methods=['GET'])
def consenso():
    atualizado = blockchain.resolver_conflitos()
    if atualizado:
        return jsonify({'mensagem': 'Cadeia atualizada via consenso'}), 200
    else:
        return jsonify({'mensagem': 'Cadeia já está atualizada'}), 200

if __name__ == '__main__':
    import os
    porta = int(os.environ.get('FLASK_RUN_PORT', 5000))
    app.run(port=porta, debug=True)
