from InformationRetrieval.Index.Posting import Posting


class PositionalPosting:

    __positions: [Posting]
    __doc_id: int

    def __init__(self, docId: int):
        self.__positions = []
        self.__doc_id = docId

    def add(self, position: int):
        self.__positions.append(Posting(position))

    def getDocId(self) -> int:
        return self.__doc_id

    def getPositions(self) -> [Posting]:
        return self.__positions

    def size(self) -> int:
        return len(self.__positions)

    def __str__(self) -> str:
        result = self.__doc_id.__str__() + " " + len(self.__positions).__str__()
        for posting in self.__positions:
            result = result + " " + posting.getId().__str__()
        return result
