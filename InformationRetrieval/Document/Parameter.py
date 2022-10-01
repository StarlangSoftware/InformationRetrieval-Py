from MorphologicalAnalysis.FsmMorphologicalAnalyzer import FsmMorphologicalAnalyzer
from MorphologicalDisambiguation.MorphologicalDisambiguator import MorphologicalDisambiguator

from InformationRetrieval.Document.IndexType import IndexType
from InformationRetrieval.Index.TermOccurrence import TermOccurrence


class Parameter:

    __index_type: IndexType = IndexType.INVERTED_INDEX
    __word_comparator: object
    __load_indexes_from_file: bool = False
    __disambiguator: MorphologicalDisambiguator
    __fsm: FsmMorphologicalAnalyzer
    __normalize_document: bool = False
    __phrase_index: bool = True
    __positional_index: bool = True
    __construct_n_gram_index: bool = True
    __construct_index_in_disk: bool = False
    __construct_dictionary_in_disk: bool = False
    __limit_number_of_documents_loaded: bool = False
    __document_limit: int = 1000
    __word_limit: int = 10000

    def __init__(self):
        self.__word_comparator = TermOccurrence.ignoreCaseComparator

    def getIndexType(self) -> IndexType:
        return self.__index_type

    def getWordComparator(self) -> object:
        return self.__word_comparator

    def loadIndexesFromFile(self) -> bool:
        return self.__load_indexes_from_file

    def getDisambiguator(self) -> MorphologicalDisambiguator:
        return self.__disambiguator

    def getFsm(self) -> FsmMorphologicalAnalyzer:
        return self.__fsm

    def constructPhraseIndex(self) -> bool:
        return self.__phrase_index

    def normalizeDocument(self) -> bool:
        return self.__normalize_document

    def constructPositionalIndex(self) -> bool:
        return self.__positional_index

    def constructNGramIndex(self) -> bool:
        return self.__construct_n_gram_index

    def constructIndexInDisk(self) -> bool:
        return self.__construct_index_in_disk

    def limitNumberOfDocumentsLoaded(self) -> bool:
        return self.__limit_number_of_documents_loaded

    def getDocumentLimit(self) -> int:
        return self.__document_limit

    def constructDictionaryInDisk(self) -> bool:
        return self.__construct_dictionary_in_disk

    def getWordLimit(self) -> int:
        return self.__word_limit

    def setIndexType(self, indexType: IndexType):
        self.__index_type = indexType

    def setWordComparator(self, wordComparator: object):
        self.__word_comparator = wordComparator

    def setLoadIndexesFromFile(self, loadIndexesFromFile: bool):
        self.__load_indexes_from_file = loadIndexesFromFile

    def setDisambiguator(self, disambiguator: MorphologicalDisambiguator):
        self.__disambiguator = disambiguator

    def setFsm(self, fsm: FsmMorphologicalAnalyzer):
        self.__fsm = fsm

    def setNormalizeDocument(self, normalizeDocument: bool):
        self.__normalize_document = normalizeDocument

    def setPhraseIndex(self, phraseIndex: bool):
        self.__phrase_index = phraseIndex

    def setPositionalIndex(self, positionalIndex: bool):
        self.__positional_index = positionalIndex

    def setNGramIndex(self, nGramIndex: bool):
        self.__construct_n_gram_index = nGramIndex

    def setConstructIndexInDisk(self, constructIndexInDisk: bool):
        self.__construct_index_in_disk = constructIndexInDisk

    def setLimitNumberOfDocumentsLoaded(self, limitNumberOfDocumentsLoaded: bool):
        self.__limit_number_of_documents_loaded = limitNumberOfDocumentsLoaded

    def setDocumentLimit(self, documentLimit: int):
        self.__document_limit = documentLimit

    def setConstructDictionaryInDisk(self, constructDictionaryInDisk: bool):
        self.__construct_dictionary_in_disk = constructDictionaryInDisk
        if self.__construct_dictionary_in_disk:
            self.__construct_index_in_disk = True

    def setWordLimit(self, wordLimit: int):
        self.__word_limit = wordLimit
