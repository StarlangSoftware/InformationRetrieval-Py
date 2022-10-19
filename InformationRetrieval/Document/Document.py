from Corpus.Corpus import Corpus
from Corpus.Sentence import Sentence
from Corpus.TurkishSplitter import TurkishSplitter
from Dictionary.Word import Word
from MorphologicalAnalysis.FsmMorphologicalAnalyzer import FsmMorphologicalAnalyzer
from MorphologicalDisambiguation.MorphologicalDisambiguator import MorphologicalDisambiguator

from InformationRetrieval.Document.CategoryHierarchy import CategoryHierarchy
from InformationRetrieval.Document.DocumentText import DocumentText
from InformationRetrieval.Document.DocumentType import DocumentType


class Document:

    __absolute_file_name: str
    __file_name: str
    __doc_id: int
    __size: int = 0
    __document_type: DocumentType
    __category_hierarchy: CategoryHierarchy

    def __init__(self, documentType: DocumentType, absoluteFileName: str, fileName: str, docId: int):
        self.__absolute_file_name = absoluteFileName
        self.__file_name = fileName
        self.__doc_id = docId
        self.__document_type = documentType

    def loadDocument(self) -> DocumentText:
        if self.__document_type == DocumentType.NORMAL:
            document_text = DocumentText(self.__absolute_file_name, TurkishSplitter())
            self.__size = document_text.numberOfWords()
        elif self.__document_type == DocumentType.CATEGORICAL:
            corpus = Corpus(self.__absolute_file_name)
            if corpus.sentenceCount() >= 2:
                self.__category_hierarchy = CategoryHierarchy(corpus.getSentence(0).__str__())
                document_text = DocumentText()
                sentences = TurkishSplitter().split(corpus.getSentence(1).__str__())
                for sentence in sentences:
                    document_text.addSentence(sentence)
                    self.__size = document_text.numberOfWords()
            else:
                return None
        return document_text

    def getDocId(self) -> int:
        return self.__doc_id

    def getFileName(self) -> str:
        return self.__file_name

    def getAbsoluteFileName(self) -> str:
        return self.__absolute_file_name

    def getSize(self) -> int:
        return self.__size

    def setSize(self, size: int):
        self.__size = size

    def setCategoryHierarchy(self, categoryHierarchy: str):
        self.__category_hierarchy = CategoryHierarchy(categoryHierarchy)

    def getCategoryHierarchy(self) -> CategoryHierarchy:
        return self.__category_hierarchy
