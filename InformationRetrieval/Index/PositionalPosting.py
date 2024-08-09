from InformationRetrieval.Index.Posting import Posting


class PositionalPosting:

    __positions: [Posting]
    __doc_id: int

    def __init__(self, docId: int):
        """
        Constructor for the PositionalPosting class. Sets the document id and initializes the position array.
        :param docId: document id of the posting.
        """
        self.__positions = []
        self.__doc_id = docId

    def add(self, position: int):
        """
        Adds a position to the position list.
        :param position: Position added to the position list.
        """
        self.__positions.append(Posting(position))

    def getDocId(self) -> int:
        """
        Accessor for the document id attribute.
        :return: Document id.
        """
        return self.__doc_id

    def getPositions(self) -> [Posting]:
        """
        Accessor for the positions attribute.
        :return: Position list.
        """
        return self.__positions

    def size(self) -> int:
        """
        Returns size of the position list.
        :return: Size of the position list.
        """
        return len(self.__positions)

    def __str__(self) -> str:
        """
        Converts the positional posting to a string. String is of the form, document id, number of positions, and all
        positions separated via space.
        :return: String form of the positional posting.
        """
        result = self.__doc_id.__str__() + " " + len(self.__positions).__str__()
        for posting in self.__positions:
            result = result + " " + posting.getId().__str__()
        return result
