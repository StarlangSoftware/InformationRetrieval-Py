from __future__ import annotations
from Dictionary.Word import Word


class TermOccurrence:

    _term: Word
    _docID: int
    _position: int

    def __init__(self, term: Word, docID: int, position: int):
        self._term = term
        self._docID = docID
        self._position = position

    @staticmethod
    def makeComparator(comparator: object):
        def compare(termA: TermOccurrence, termB: TermOccurrence):
            if termA.getTerm().getName() != termB.getTerm().getName():
                return comparator.compare(termA.getTerm(), termB.getTerm())
            elif termA.getDocID() == termB.getDocID():
                if termA.getPosition() == termB.getPosition():
                    return 0
                elif termA.getPosition() < termB.getPosition():
                    return -1
                else:
                    return 1
            elif termA.getDocID() < termB.getDocID():
                return -1
            else:
                return 1
        return compare

    def getTerm(self) -> Word:
        return self._term

    def getDocID(self) -> int:
        return self._docID

    def getPosition(self) -> int:
        return self._position

    def isDifferent(self, currentTerm: TermOccurrence) -> bool:
        return self._term.getName() != currentTerm.getTerm().getName()
