class QueryResultItem:

    __doc_id: int
    __score: float

    def __init__(self, docId: int, score: float):
        self.__doc_id = docId
        self.__score = score

    def getDocId(self) -> int:
        return self.__doc_id

    def getScore(self) -> float:
        return self.__score

    def __repr__(self):
        return f"{self.__doc_id} {self.__score}"
