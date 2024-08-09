from Dictionary.Word import Word


class Term(Word):

    __term_id: int

    def __init__(self, name: str, termId: int):
        """
        Constructor for the Term class. Sets the fields.
        :param name: Text of the term
        :param termId: Id of the term
        """
        super().__init__(name)
        self.__term_id = termId

    def getTermId(self) -> int:
        """
        Accessor for the term id attribute.
        :return: Term id attribute
        """
        return self.__term_id
