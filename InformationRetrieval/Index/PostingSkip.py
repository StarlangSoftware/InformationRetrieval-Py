from __future__ import annotations

from InformationRetrieval.Index.Posting import Posting


class PostingSkip(Posting):

    __skip_available: bool = False
    __skip: PostingSkip = None
    __next: PostingSkip = None

    def __init__(self, Id: int):
        """
        Constructor for the PostingSkip class. Sets the document id.
        :param Id: Document id.
        """
        super().__init__(Id)

    def hasSkip(self) -> bool:
        """
        Checks if this posting has a skip pointer or not.
        :return: True, if this posting has a skip pointer, false otherwise.
        """
        return self.__skip_available

    def addSkip(self, skip: PostingSkip):
        """
        Adds a skip pointer to the next skip posting.
        :param skip: Next posting to jump.
        """
        self.__skip_available = True
        self.__skip = skip

    def setNext(self, _next: PostingSkip):
        """
        Updated the skip pointer.
        :param _next: New skip pointer
        """
        self.__next = _next

    def next(self) -> PostingSkip:
        """
        Accessor for the skip pointer.
        :return: Next posting to skip.
        """
        return self.__next

    def getSkip(self) -> PostingSkip:
        """
        Accessor for the skip.
        :return: Skip
        """
        return self.__skip
