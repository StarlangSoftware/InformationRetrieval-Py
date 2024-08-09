from Corpus.Corpus import Corpus
from Corpus.SentenceSplitter import SentenceSplitter

from Dictionary.Word import Word

from InformationRetrieval.Index.TermOccurrence import TermOccurrence
from InformationRetrieval.Index.TermType import TermType


class DocumentText(Corpus):

    def __init__(self,
                 fileName: str = None,
                 sentenceSplitter: SentenceSplitter = None):
        """
        Another constructor for the DocumentText class. Calls super with the given file name and sentence splitter.
        :param fileName: File name of the corpus
        :param sentenceSplitter: Sentence splitter class that separates sentences.
        """
        super().__init__(fileName, sentenceSplitter)

    def constructDistinctWordList(self, termType: TermType) -> set:
        """
        Given the corpus, creates a hash set of distinct terms. If term type is TOKEN, the terms are single word, if
        the term type is PHRASE, the terms are bi-words.
        :param termType: If term type is TOKEN, the terms are single word, if the term type is PHRASE, the terms are
                         bi-words.
        :return: Hash set of terms occurring in the document.
        """
        words = set()
        for i in range(self.sentenceCount()):
            sentence = self.getSentence(i)
            for j in range(sentence.wordCount()):
                if termType == TermType.TOKEN:
                    words.add(sentence.getWord(j).getName())
                elif termType == TermType.PHRASE:
                    if j < sentence.wordCount() - 1:
                        words.add(sentence.getWord(j).getName() + " " + sentence.getWord(j + 1).getName())
        return words

    def constructTermList(self,
                          docId: int,
                          termType: TermType) -> [TermOccurrence]:
        """
        Given the corpus, creates an array of terms occurring in the document in that order. If term type is TOKEN, the
        terms are single word, if the term type is PHRASE, the terms are bi-words.
        :param docId: Id of the document
        :param termType: If term type is TOKEN, the terms are single word, if the term type is PHRASE, the terms are
                         bi-words.
        :return: Array list of terms occurring in the document.
        """
        terms = []
        size = 0
        for i in range(self.sentenceCount()):
            sentence = self.getSentence(i)
            for j in range(sentence.wordCount()):
                if termType == TermType.TOKEN:
                    terms.append(TermOccurrence(sentence.getWord(j), docId, size))
                    size = size + 1
                elif termType == TermType.PHRASE:
                    if j < sentence.wordCount() - 1:
                        terms.append(TermOccurrence(Word(sentence.getWord(j).getName() + " " + sentence.getWord(j + 1).getName()), docId, size))
                        size = size + 1
        return terms
