from dataclasses import dataclass

@dataclass
class Connessione:
    id_connessione: int
    id_linea: int
    id_stazA: int
    id_stazP: int

    def __hash__(self):
        return hash(self.id_connessione)

    def __eq__(self, other):
        return self.id_connessione == other.id_connessione