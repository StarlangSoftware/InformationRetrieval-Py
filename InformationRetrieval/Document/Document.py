from Corpus.Corpus import Corpus
from Corpus.Sentence import Sentence
from Corpus.TurkishSplitter import TurkishSplitter
from Dictionary.Word import Word
from MorphologicalAnalysis.FsmMorphologicalAnalyzer import FsmMorphologicalAnalyzer
from MorphologicalDisambiguation.MorphologicalDisambiguator import MorphologicalDisambiguator

from InformationRetrieval.Document.DocumentText import DocumentText


class Document:

    __absolute_file_name: str
    __file_name: str
    __doc_id: int
    __size: int = 0

    def __init__(self, absoluteFileName: str, fileName: str, docId: int):
        self.__absolute_file_name = absoluteFileName
        self.__file_name = fileName
        self.__doc_id = docId

    def loadDocument(self) -> DocumentText:
        document_text = DocumentText(self.__absolute_file_name, TurkishSplitter())
        self.__size = document_text.numberOfWords()
        return document_text

    def normalizeDocument(self,
                          disambiguator: MorphologicalDisambiguator,
                          fsm: FsmMorphologicalAnalyzer) -> Corpus:
        corpus = Corpus(self.__absolute_file_name)
        for i in range(corpus.sentenceCount()):
            sentence = corpus.getSentence(i)
            parses = fsm.robustMorphologicalAnalysis(sentence)
            correct_parses = disambiguator.disambiguate(parses)
            new_sentence = Sentence()
            for fsm_parse in correct_parses:
                new_sentence.addWord(Word(fsm_parse.getWord().getName()))
            corpus.addSentence(new_sentence)
        self.__size = corpus.numberOfWords()
        return corpus

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
