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
        super().__init__(directory, parameter)
        self.constructIndexesInDisk()

    def constructDistinctWordList(self, termType: TermType) -> set:
        words = set()
        for doc in self.documents:
            document_text = doc.loadDocument()
            doc_words = document_text.constructDistinctWordList(termType)
            words = words.union(doc_words)
        return words

    def constructIndexesInDisk(self):
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
