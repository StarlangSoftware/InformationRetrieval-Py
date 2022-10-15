from InformationRetrieval.Document.DocumentWeighting import DocumentWeighting
from InformationRetrieval.Index.TermWeighting import TermWeighting
from InformationRetrieval.Query.RetrievalType import RetrievalType


class SearchParameter:

    __retrieval_type: RetrievalType
    __document_weighting: DocumentWeighting
    __term_weighting: TermWeighting
    __documents_retrieved: int

    def __init__(self):
        self.__retrieval_type = RetrievalType.RANKED
        self.__document_weighting = DocumentWeighting.NO_IDF
        self.__term_weighting = TermWeighting.NATURAL
        self.__documents_retrieved = 1

    def getRetrievalType(self) -> RetrievalType:
        return self.__retrieval_type

    def getDocumentWeighting(self) -> DocumentWeighting:
        return self.__document_weighting

    def getTermWeighting(self) -> TermWeighting:
        return self.__term_weighting

    def getDocumentsRetrieved(self) -> int:
        return self.__documents_retrieved

    def setRetrievalType(self, retrievalType: RetrievalType):
        self.__retrieval_type = retrievalType

    def setDocumentWeighting(self, documentWeighting: DocumentWeighting):
        self.__document_weighting = documentWeighting

    def setTermWeighting(self, termWeighting: TermWeighting):
        self.__term_weighting = termWeighting

    def setDocumentsRetrieved(self, documentsRetrieved: int):
        self.__documents_retrieved = documentsRetrieved
