class ControleEleitores:
    def __init__(self):
        self.eleitores_que_votaram = set()

    def ja_votou(self, eleitor_id):
        return eleitor_id in self.eleitores_que_votaram

    def registrar_voto(self, eleitor_id):
        self.eleitores_que_votaram.add(eleitor_id)
