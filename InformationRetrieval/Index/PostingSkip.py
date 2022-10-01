from __future__ import annotations

from InformationRetrieval.Index.Posting import Posting


class PostingSkip(Posting):

    __skip_available: bool = False
    __skip: PostingSkip = None
    __next: PostingSkip = None

    def __init__(self, Id: int):
        super().__init__(Id)

    def hasSkip(self) -> bool:
        return self.__skip_available

    def addSkip(self, skip: PostingSkip):
        self.__skip_available = True
        self.__skip = skip

    def setNext(self, _next: PostingSkip):
        self.__next = _next

    def next(self) -> PostingSkip:
        return self.__next

    def getSkip(self) -> PostingSkip:
        return self.__skip
