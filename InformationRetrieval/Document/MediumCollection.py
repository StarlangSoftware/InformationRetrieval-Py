from InformationRetrieval.Document.DiskCollection import DiskCollection
from InformationRetrieval.Document.Parameter import Parameter
from InformationRetrieval.Index.InvertedIndex import InvertedIndex
from InformationRetrieval.Index.PositionalIndex import PositionalIndex
from InformationRetrieval.Index.TermDictionary import TermDictionary
from InformationRetrieval.Index.TermType import TermType


class MediumCollection(DiskCollection):

    def __init__(self,
                 directory: str,
                 parameter: Parameter):
        """
        Constructor for the MediumCollection class. In medium collections, dictionary is kept in memory and indexes are
        stored in the disk and don't fit in memory in their construction phase and usage phase. For that reason, in their
        construction phase, multiple disk reads and optimizations are needed.
        :param directory: Directory where the document collection resides.
        :param parameter: Search parameter
        """
        super().__init__(directory, parameter)
        self.constructIndexesInDisk()

    def constructDistinctWordList(self, termType: TermType) -> set:
        """
        Given the document collection, creates a hash set of distinct terms. If term type is TOKEN, the terms are single
        word, if the term type is PHRASE, the terms are bi-words. Each document is loaded into memory and distinct
        word list is created. Since the dictionary can be kept in memory, all operations can be done in memory.
        :param termType: If term type is TOKEN, the terms are single word, if the term type is PHRASE, the terms are
                         bi-words.
        :return: Hash set of terms occurring in the document collection.
        """
        words = set()
        for doc in self.documents:
            document_text = doc.loadDocument()
            doc_words = document_text.constructDistinctWordList(termType)
            words = words.union(doc_words)
        return words

    def constructIndexesInDisk(self):
        """
        In block sort based indexing, the indexes are created in a block wise manner. They do not fit in memory, therefore
        documents are read one by one. According to the search parameter, inverted index, positional index, phrase
        indexes, N-Gram indexes are constructed in disk.
        """
        word_list = self.constructDistinctWordList(TermType.TOKEN)
        self.__dictionary = TermDictionary(self.comparator, word_list)
        self.constructInvertedIndexInDisk(self.__dictionary, TermType.TOKEN)
        if self.parameter.constructPositionalIndex():
            self.constructPositionalIndexInDisk(self.__dictionary, TermType.TOKEN)
        if self.parameter.constructPhraseIndex():
            word_list = self.constructDistinctWordList(TermType.PHRASE)
            self.__phrase_dictionary = TermDictionary(self.comparator, word_list)
            self.constructInvertedIndexInDisk(self.__phrase_dictionary, TermType.PHRASE)
            if self.parameter.constructPositionalIndex():
                self.constructPositionalIndexInDisk(self.__phrase_dictionary, TermType.PHRASE)
        if self.parameter.constructNGramIndex():
            self.constructNGramIndex()

    def constructInvertedIndexInDisk(self,
                                     dictionary: TermDictionary,
                                     termType: TermType):
        """
        In block sort based indexing, the inverted index is created in a block wise manner. It does not fit in memory,
        therefore documents are read one by one. For each document, the terms are added to the inverted index. If the
        number of documents read are above the limit, current partial inverted index file is saved and new inverted index
        file is open. After reading all documents, we combine the inverted index files to get the final inverted index
        file.
        :param dictionary: Term dictionary.
        :param termType: If term type is TOKEN, the terms are single word, if the term type is PHRASE, the terms are
                         bi-words.
        """
        i = 0
        block_count = 0
        inverted_index = InvertedIndex()
        for doc in self.documents:
            if i < self.parameter.getDocumentLimit():
                i = i + 1
            else:
                inverted_index.saveSorted("tmp-" + block_count.__str__())
                inverted_index = InvertedIndex()
                block_count = block_count + 1
                i = 0
            document_text = doc.loadDocument()
            word_list = document_text.constructDistinctWordList(termType)
            for word in word_list:
                term_id = dictionary.getWordIndex(word)
                inverted_index.add(term_id, doc.getDocId())
        if len(self.documents) != 0:
            inverted_index.saveSorted("tmp-" + block_count.__str__())
            block_count = block_count + 1
        if termType == TermType.TOKEN:
            self.combineMultipleInvertedIndexesInDisk(self.name, "", block_count)
        else:
            self.combineMultipleInvertedIndexesInDisk(self.name + "-phrase", "", block_count)

    def constructPositionalIndexInDisk(self,
                                       dictionary: TermDictionary,
                                       termType: TermType):
        """
        In block sort based indexing, the positional index is created in a block wise manner. It does not fit in memory,
        therefore documents are read one by one. For each document, the terms are added to the positional index. If the
        number of documents read are above the limit, current partial positional index file is saved and new positional
        index file is open. After reading all documents, we combine the posiitonal index files to get the final
        positional index file.
        :param dictionary: Term dictionary.
        :param termType: If term type is TOKEN, the terms are single word, if the term type is PHRASE, the terms are
                         bi-words.
        """
        i = 0
        block_count = 0
        positional_index = PositionalIndex()
        for doc in self.documents:
            if i < self.parameter.getDocumentLimit():
                i = i + 1
            else:
                positional_index.saveSorted("tmp-" + block_count.__str__())
                positional_index = PositionalIndex()
                block_count = block_count + 1
                i = 0
            document_text = doc.loadDocument()
            terms = document_text.constructTermList(doc.getDocId(), termType)
            for term_occurrence in terms:
                termId = dictionary.getWordIndex(term_occurrence.getTerm().getName())
                positional_index.addPosition(termId, term_occurrence.getDocId(), term_occurrence.getPosition())
        if len(self.documents) != 0:
            positional_index.saveSorted("tmp-" + block_count.__str__())
            block_count = block_count + 1
        if termType == TermType.TOKEN:
            self.combineMultiplePositionalIndexesInDisk(self.name, block_count)
        else:
            self.combineMultiplePositionalIndexesInDisk(self.name + "-phrase", block_count)
