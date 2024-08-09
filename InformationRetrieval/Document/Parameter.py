from MorphologicalAnalysis.FsmMorphologicalAnalyzer import FsmMorphologicalAnalyzer
from MorphologicalDisambiguation.MorphologicalDisambiguator import MorphologicalDisambiguator

from InformationRetrieval.Document.DocumentType import DocumentType
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
    __limit_number_of_documents_loaded: bool = False
    __document_limit: int = 1000
    __word_limit: int = 10000
    __document_type: DocumentType = DocumentType.NORMAL
    __representative_count: int = 10

    def __init__(self):
        """
        Empty constructor for the general query search.
        """
        self.__word_comparator = TermOccurrence.ignoreCaseComparator

    def getIndexType(self) -> IndexType:
        """
        Accessor for the index type search parameter. Index can be inverted index or incidence matrix.
        :return: Index type search parameter
        """
        return self.__index_type

    def getWordComparator(self) -> object:
        """
        Accessor for the word comparator. Word comparator is a function to compare terms.
        :return: Word comparator
        """
        return self.__word_comparator

    def loadIndexesFromFile(self) -> bool:
        """
        Accessor for the loadIndexesFromFile search parameter. If loadIndexesFromFile is true, all the indexes will be
        read from the file, otherwise they will be reconstructed.
        :return: loadIndexesFromFile search parameter
        """
        return self.__load_indexes_from_file

    def getDisambiguator(self) -> MorphologicalDisambiguator:
        """
        Accessor for the disambiguator search parameter. The disambiguator is used for morphological disambiguation for
        the terms in Turkish.
        :return: disambiguator search parameter
        """
        return self.__disambiguator

    def getFsm(self) -> FsmMorphologicalAnalyzer:
        """
        Accessor for the fsm search parameter. The fsm is used for morphological analysis for  the terms in Turkish.
        :return: fsm search parameter
        """
        return self.__fsm

    def constructPhraseIndex(self) -> bool:
        """
        Accessor for the constructPhraseIndex search parameter. If constructPhraseIndex is true, phrase indexes will be
        reconstructed or used in query processing.
        :return: constructPhraseIndex search parameter
        """
        return self.__phrase_index

    def normalizeDocument(self) -> bool:
        """
        Accessor for the normalizeDocument search parameter. If normalizeDocument is true, the terms in the document will
        be preprocessed by morphological anaylysis and some preprocessing techniques.
        :return: normalizeDocument search parameter
        """
        return self.__normalize_document

    def constructPositionalIndex(self) -> bool:
        """
        Accessor for the positionalIndex search parameter. If positionalIndex is true, positional indexes will be
        reconstructed or used in query processing.
        :return: positionalIndex search parameter
        """
        return self.__positional_index

    def constructNGramIndex(self) -> bool:
        """
        Accessor for the constructNGramIndex search parameter. If constructNGramIndex is true, N-Gram indexes will be
        reconstructed or used in query processing.
        :return: constructNGramIndex search parameter
        """
        return self.__construct_n_gram_index

    def limitNumberOfDocumentsLoaded(self) -> bool:
        """
        Accessor for the limitNumberOfDocumentsLoaded search parameter. If limitNumberOfDocumentsLoaded is true,
        the query result will be filtered according to the documentLimit search parameter.
        :return: limitNumberOfDocumentsLoaded search parameter
        """
        return self.__limit_number_of_documents_loaded

    def getDocumentLimit(self) -> int:
        """
        Accessor for the documentLimit search parameter. If limitNumberOfDocumentsLoaded is true,  the query result will
        be filtered according to the documentLimit search parameter.
        :return: limitNumberOfDocumentsLoaded search parameter
        """
        return self.__document_limit

    def getWordLimit(self) -> int:
        """
        Accessor for the wordLimit search parameter. wordLimit is the limit on the partial term dictionary size. For
        large collections, we term dictionaries are divided into multiple files, this parameter sets the number of terms
        in those separate dictionaries.
        :return: wordLimit search parameter
        """
        return self.__word_limit

    def getRepresentativeCount(self) -> int:
        """
        Accessor for the representativeCount search parameter. representativeCount is the maximum number of representative
        words in the category based query search.
        :return: representativeCount search parameter
        """
        return self.__representative_count

    def setIndexType(self, indexType: IndexType):
        """
        Mutator for the index type search parameter. Index can be inverted index or incidence matrix.
        :param indexType: Index type search parameter
        """
        self.__index_type = indexType

    def setWordComparator(self, wordComparator: object):
        """
        Mutator for the word comparator. Word comparator is a function to compare terms.
        :param wordComparator: Word comparator
        """
        self.__word_comparator = wordComparator

    def setLoadIndexesFromFile(self, loadIndexesFromFile: bool):
        """
        Mutator for the loadIndexesFromFile search parameter. If loadIndexesFromFile is true, all the indexes will be
        read from the file, otherwise they will be reconstructed.
        :param loadIndexesFromFile: loadIndexesFromFile search parameter
        """
        self.__load_indexes_from_file = loadIndexesFromFile

    def setDisambiguator(self, disambiguator: MorphologicalDisambiguator):
        """
        Mutator for the disambiguator search parameter. The disambiguator is used for morphological disambiguation for
        the terms in Turkish.
        :param disambiguator: disambiguator search parameter
        """
        self.__disambiguator = disambiguator

    def setFsm(self, fsm: FsmMorphologicalAnalyzer):
        """
        Mutator for the fsm search parameter. The fsm is used for morphological analysis for the terms in Turkish.
        :param fsm: fsm search parameter
        """
        self.__fsm = fsm

    def setNormalizeDocument(self, normalizeDocument: bool):
        """
        Mutator for the normalizeDocument search parameter. If normalizeDocument is true, the terms in the document will
        be preprocessed by morphological anaylysis and some preprocessing techniques.
        :param normalizeDocument: normalizeDocument search parameter
        """
        self.__normalize_document = normalizeDocument

    def setPhraseIndex(self, phraseIndex: bool):
        """
        Mutator for the constructPhraseIndex search parameter. If constructPhraseIndex is true, phrase indexes will be
        reconstructed or used in query processing.
        :param phraseIndex: constructPhraseIndex search parameter
        """
        self.__phrase_index = phraseIndex

    def setPositionalIndex(self, positionalIndex: bool):
        """
        Mutator for the positionalIndex search parameter. If positionalIndex is true, positional indexes will be
        reconstructed or used in query processing.
        :param positionalIndex: positionalIndex search parameter
        """
        self.__positional_index = positionalIndex

    def setNGramIndex(self, nGramIndex: bool):
        """
        Mutator for the constructNGramIndex search parameter. If constructNGramIndex is true, N-Gram indexes will be
        reconstructed or used in query processing.
        :param nGramIndex: constructNGramIndex search parameter
        """
        self.__construct_n_gram_index = nGramIndex

    def setLimitNumberOfDocumentsLoaded(self, limitNumberOfDocumentsLoaded: bool):
        """
        Mutator for the limitNumberOfDocumentsLoaded search parameter. If limitNumberOfDocumentsLoaded is true,
        the query result will be filtered according to the documentLimit search parameter.
        :param limitNumberOfDocumentsLoaded: limitNumberOfDocumentsLoaded search parameter
        """
        self.__limit_number_of_documents_loaded = limitNumberOfDocumentsLoaded

    def setDocumentLimit(self, documentLimit: int):
        """
        Mutator for the documentLimit search parameter. If limitNumberOfDocumentsLoaded is true,  the query result will
        be filtered according to the documentLimit search parameter.
        :param documentLimit: documentLimit search parameter
        """
        self.__document_limit = documentLimit

    def setWordLimit(self, wordLimit: int):
        """
        Mutator for the documentLimit search parameter. If limitNumberOfDocumentsLoaded is true,  the query result will
        be filtered according to the documentLimit search parameter.
        :param wordLimit: wordLimit search parameter
        """
        self.__word_limit = wordLimit

    def setRepresentativeCount(self, representativeCount: int):
        """
        Mutator for the representativeCount search parameter. representativeCount is the maximum number of representative
        words in the category based query search.
        :param representativeCount: representativeCount search parameter
        """
        self.__representative_count = representativeCount

    def getDocumentType(self) -> DocumentType:
        """
        Accessor for the document type search parameter. Document can be normal or a categorical document.
        :return: Document type search parameter
        """
        return self.__document_type

    def setDocumentType(self, documentType: DocumentType):
        """
        Mutator for the document type search parameter. Document can be normal or a categorical document.
        :param documentType: Document type search parameter
        """
        self.__document_type = documentType
