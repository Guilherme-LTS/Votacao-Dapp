from flask import Flask, jsonify, request
from flask_cors import CORS
from blockchain.blockchain import Blockchain
from blockchain.voto import Voto
from blockchain.eleitor import ControleEleitores

app = Flask(__name__)
CORS(app)

blockchain = Blockchain()
controle = ControleEleitores()

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

    return jsonify({'mensagem': 'Voto computado com sucesso!'}), 200

@app.route('/minerar', methods=['GET'])
def minerar():
    bloco = blockchain.criar_bloco()
    return jsonify({'mensagem': 'Bloco minerado', 'bloco': bloco}), 200

@app.route('/resultados', methods=['GET'])
def resultados():
    votos = {}
    for bloco in blockchain.get_chain():
        for transacao in bloco['transacoes']:
            candidato = transacao['candidato']
            votos[candidato] = votos.get(candidato, 0) + 1

    return jsonify({'resultados': votos}), 200

if __name__ == '__main__':
    app.run(debug=True)
