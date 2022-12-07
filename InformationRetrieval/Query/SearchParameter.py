from InformationRetrieval.Document.DocumentWeighting import DocumentWeighting
from InformationRetrieval.Index.TermWeighting import TermWeighting
from InformationRetrieval.Query.CategoryDeterminationType import CategoryDeterminationType
from InformationRetrieval.Query.FocusType import FocusType
from InformationRetrieval.Query.RetrievalType import RetrievalType


class SearchParameter:

    __category_determination_type: CategoryDeterminationType
    __focus_type: FocusType
    __retrieval_type: RetrievalType
    __document_weighting: DocumentWeighting
    __term_weighting: TermWeighting
    __documents_retrieved: int

    def __init__(self):
        self.__retrieval_type = RetrievalType.RANKED
        self.__document_weighting = DocumentWeighting.NO_IDF
        self.__term_weighting = TermWeighting.NATURAL
        self.__documents_retrieved = 1
        self.__category_determination_type = CategoryDeterminationType.KEYWORD
        self.__focus_type = FocusType.OVERALL

    def getRetrievalType(self) -> RetrievalType:
        return self.__retrieval_type

    def getDocumentWeighting(self) -> DocumentWeighting:
        return self.__document_weighting

    def getTermWeighting(self) -> TermWeighting:
        return self.__term_weighting

    def getDocumentsRetrieved(self) -> int:
        return self.__documents_retrieved

    def getCategoryDeterminationType(self) -> CategoryDeterminationType:
        return self.__category_determination_type

    def getFocusType(self) -> FocusType:
        return self.__focus_type

    def setRetrievalType(self, retrievalType: RetrievalType):
        self.__retrieval_type = retrievalType

    def setDocumentWeighting(self, documentWeighting: DocumentWeighting):
        self.__document_weighting = documentWeighting

    def setTermWeighting(self, termWeighting: TermWeighting):
        self.__term_weighting = termWeighting

    def setDocumentsRetrieved(self, documentsRetrieved: int):
        self.__documents_retrieved = documentsRetrieved

    def setCategoryDeterminationType(self, categoryDeterminationType: CategoryDeterminationType):
        self.__category_determination_type = categoryDeterminationType

    def setFocusType(self, focusType: FocusType):
        self.__focus_type = focusType
