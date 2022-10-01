from InformationRetrieval.Index.TermDictionary import TermDictionary
from InformationRetrieval.Index.TermOccurrence import TermOccurrence
from InformationRetrieval.Query.Query import Query
from InformationRetrieval.Query.QueryResult import QueryResult


class IncidenceMatrix:

    __incidence_matrix: [[bool]]
    __dictionary_size: int
    __document_size: int

    def __init__(self,
                 terms: [TermOccurrence],
                 dictionary: TermDictionary,
                 documentSize: int):
        self.__dictionary_size = dictionary.size()
        self.__document_size = documentSize
        self.__incidence_matrix = [[False for _ in range(self.__document_size)] for _ in range(self.__dictionary_size)]
        if len(terms) > 0:
            term: TermOccurrence = terms[0]
            i = 1
            self.set(dictionary.getWordIndex(term.getTerm().getName()), term.getDocId())
            while i < len(terms):
                term = terms[i]
                self.set(dictionary.getWordIndex(term.getTerm().getName()), term.getDocId())
                i = i + 1

    def set(self,
            row: int,
            col: int):
        self.__incidence_matrix[row][col] = True

    def search(self,
               query: Query,
               dictionary: TermDictionary) -> QueryResult:
        result = QueryResult()
        result_row = [True for _ in range(self.__document_size)]
        for i in range(query.size()):
            term_index = dictionary.getWordIndex(query.getTerm(i).getName())
            if term_index != -1:
                for j in range(self.__document_size):
                    result_row[j] = result_row[j] and self.__incidence_matrix[term_index][j]
            else:
                return result
        for i in range(self.__document_size):
            if result_row[i]:
                result.add(i)
        return result
