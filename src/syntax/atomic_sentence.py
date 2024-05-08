from src.syntax.atom import Atom, BoolAtom
from src.syntax.sentence import Sentence


class AtomicSentence(Sentence):
    def __init__(self, atom: Atom):
        super().__init__()
        self.atom = atom

    def __str__(self):
        return str(self.atom)
\

