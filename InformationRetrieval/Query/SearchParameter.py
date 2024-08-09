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
    __search_attributes: bool

    def __init__(self):
        """
        Empty constructor for SearchParameter object.
        """
        self.__retrieval_type = RetrievalType.RANKED
        self.__document_weighting = DocumentWeighting.NO_IDF
        self.__term_weighting = TermWeighting.NATURAL
        self.__documents_retrieved = 1
        self.__category_determination_type = CategoryDeterminationType.KEYWORD
        self.__focus_type = FocusType.OVERALL
        self.__search_attributes = False

    def getRetrievalType(self) -> RetrievalType:
        """
        Accessor for the retrieval type.
        :return: Retrieval type.
        """
        return self.__retrieval_type

    def getDocumentWeighting(self) -> DocumentWeighting:
        """
        Accessor for the document weighting scheme in tf-idf search
        :return: Document weighting scheme in tf-idf search
        """
        return self.__document_weighting

    def getTermWeighting(self) -> TermWeighting:
        """
        Accessor for the term weighting scheme in tf-idf search
        :return: Term weighting scheme in tf-idf search
        """
        return self.__term_weighting

    def getDocumentsRetrieved(self) -> int:
        """
        Accessor for the maximum number of documents retrieved.
        :return: Maximum number of documents retrieved
        """
        return self.__documents_retrieved

    def getCategoryDeterminationType(self) -> CategoryDeterminationType:
        """
        Accessor for the category determination type
        :return: Category determination type
        """
        return self.__category_determination_type

    def getFocusType(self) -> FocusType:
        """
        Accessor for the focus type.
        :return: Focus type
        """
        return self.__focus_type

    def getSearchAttributes(self) -> bool:
        """
        Accessor for the search attributes field. The parameter will determine if an attribute search is performed.
        :return: Search attribute
        """
        return self.__search_attributes

    def setRetrievalType(self, retrievalType: RetrievalType):
        """
        Setter for the retrievalType.
        :param retrievalType: New retrieval type
        """
        self.__retrieval_type = retrievalType

    def setDocumentWeighting(self, documentWeighting: DocumentWeighting):
        """
        Mutator for the documentWeighting scheme used in tf-idf search.
        :param documentWeighting: New document weighting scheme for tf-idf search.
        :return:
        """
        self.__document_weighting = documentWeighting

    def setTermWeighting(self, termWeighting: TermWeighting):
        """
        Mutator for the termWeighting scheme used in tf-idf search.
        :param termWeighting: New term weighting scheme for tf-idf search.
        """
        self.__term_weighting = termWeighting

    def setDocumentsRetrieved(self, documentsRetrieved: int):
        """
        Mutator for the maximum number of documents retrieved.
        :param documentsRetrieved: New value for the maximum number of documents retrieved.
        """
        self.__documents_retrieved = documentsRetrieved

    def setCategoryDeterminationType(self, categoryDeterminationType: CategoryDeterminationType):
        """
        Mutator for the category determination type.
        :param categoryDeterminationType: New category determination type
        """
        self.__category_determination_type = categoryDeterminationType

    def setFocusType(self, focusType: FocusType):
        """
        Mutator for the focus type.
        :param focusType: New focus type
        """
        self.__focus_type = focusType

    def setSearchAttributes(self, searchAttributes: bool):
        """
        Mutator for the search attributes field. The parameter will determine if an attribute search is performed.
        :param searchAttributes: New search attribute
        """
        self.__search_attributes = searchAttributes
