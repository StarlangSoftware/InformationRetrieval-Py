from Corpus.Corpus import Corpus
from Corpus.TurkishSplitter import TurkishSplitter

from InformationRetrieval.Document.DocumentText import DocumentText
from InformationRetrieval.Document.DocumentType import DocumentType
from InformationRetrieval.Index.CategoryNode import CategoryNode
from InformationRetrieval.Index.CategoryTree import CategoryTree


class Document:

    __absolute_file_name: str
    __file_name: str
    __doc_id: int
    __size: int = 0
    __document_type: DocumentType
    __category: CategoryNode

    def __init__(self, documentType: DocumentType, absoluteFileName: str, fileName: str, docId: int):
        """
        Constructor for the Document class. Sets the attributes.
        :param documentType: Type of the document. Can be normal for normal documents, categorical for categorical
                             documents.
        :param absoluteFileName: Absolute file name of the document
        :param fileName: Relative file name of the document.
        :param docId: Id of the document
        """
        self.__absolute_file_name = absoluteFileName
        self.__file_name = fileName
        self.__doc_id = docId
        self.__document_type = documentType

    def loadDocument(self) -> DocumentText:
        """
        Loads the document from input stream. For normal documents, it reads as a corpus. For categorical documents, the
        first line contains categorical information, second line contains name of the product, third line contains
        detailed info about the product.
        :return: Loaded document text.
        """
        if self.__document_type == DocumentType.NORMAL:
            document_text = DocumentText(self.__absolute_file_name, TurkishSplitter())
            self.__size = document_text.numberOfWords()
        elif self.__document_type == DocumentType.CATEGORICAL:
            corpus = Corpus(self.__absolute_file_name)
            if corpus.sentenceCount() >= 2:
                document_text = DocumentText()
                sentences = TurkishSplitter().split(corpus.getSentence(1).__str__())
                for sentence in sentences:
                    document_text.addSentence(sentence)
                    self.__size = document_text.numberOfWords()
            else:
                return None
        return document_text

    def loadCategory(self, categoryTree: CategoryTree):
        """
        Loads the category of the document and adds it to the category tree. Category information is stored in the first
        line of the document.
        :param categoryTree: Category tree to which new product will be added.
        """
        if self.__document_type == DocumentType.CATEGORICAL:
            corpus = Corpus(self.__absolute_file_name)
            if corpus.sentenceCount() >= 2:
                self.__category = categoryTree.addCategoryHierarchy(corpus.getSentence(0).__str__())

    def getDocId(self) -> int:
        """
        Accessor for the docId attribute.
        :return: docId attribute.
        """
        return self.__doc_id

    def getFileName(self) -> str:
        """
        Accessor for the fileName attribute.
        :return: fileName attribute.
        """
        return self.__file_name

    def getAbsoluteFileName(self) -> str:
        """
        Accessor for the absoluteFileName attribute.
        :return: absoluteFileName attribute.
        """
        return self.__absolute_file_name

    def getSize(self) -> int:
        """
        Accessor for the size attribute.
        :return: size attribute.
        """
        return self.__size

    def setSize(self, size: int):
        """
        Mutator for the size attribute.
        :param size: New size attribute.
        """
        self.__size = size

    def setCategory(self, categoryTree: CategoryTree, category: str):
        """
        Mutator for the category attribute.
        :param categoryTree: Category tree to which new category will be added.
        :param category: New category that will be added
        """
        self.__category = categoryTree.addCategoryHierarchy(category)

    def getCategory(self) -> str:
        """
        Accessor for the category attribute.
        :return:Category attribute as a String
        """
        return self.__category.__str__()

    def getCategoryNode(self) -> CategoryNode:
        """
        Accessor for the category attribute.
        :return: Category attribute as a CategoryNode
        """
        return self.__category
