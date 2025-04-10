class Voto:
    def __init__(self, eleitor_id, candidato):
        self.eleitor_id = eleitor_id
        self.candidato = candidato

    def to_dict(self):
        return {
            'eleitor_id': self.eleitor_id,
            'candidato': self.candidato
        }
