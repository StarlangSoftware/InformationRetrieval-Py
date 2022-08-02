from Dictionary.Word import Word

from InformationRetrieval.Index.InvertedIndex import InvertedIndex
from InformationRetrieval.Index.TermOccurrence import TermOccurrence


class NGramIndex(InvertedIndex):

    def __init__(self,
                 dictionaryOrfileName: object,
                 terms: [TermOccurrence] = None):
        super().__init__(dictionaryOrfileName, terms)

    @staticmethod
    def constructNGrams(word: str, termId: int, k: int) -> [TermOccurrence]:
        nGrams = []
        if len(word) >= k - 1:
            for j in range(-1, len(word) - k + 2):
                if j == -1:
                    term = "$" + word[0:k - 1]
                elif j == len(word) - k + 1:
                    term = word[j: j + k - 1] + "$"
                else:
                    term = word[j: j + k]
                nGrams.append(TermOccurrence(Word(term), termId, j))
        return nGrams
