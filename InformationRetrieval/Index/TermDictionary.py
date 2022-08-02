from functools import cmp_to_key

from Dictionary.Dictionary import Dictionary
from Dictionary.Word import Word

from InformationRetrieval.Index.Term import Term
from InformationRetrieval.Index.TermOccurrence import TermOccurrence


class TermDictionary(Dictionary):

    def __init__(self, comparator: object, fileNameOrTerms):
        super().__init__(comparator)
        if isinstance(fileNameOrTerms, str):
            fileName: str = fileNameOrTerms
            infile = open(fileName + "-dictionary.txt", mode='r', encoding='utf-8')
            line = infile.readline()
            while not line:
                termId = int(line[0:line.index(" ")])
                self.words.append(Term(line[line.index(" ") + 1:], termId))
                line = infile.readline()
            infile.close()
        else:
            if isinstance(fileNameOrTerms, list):
                termId = 0
                terms: [TermOccurrence] = fileNameOrTerms
                if len(terms) > 0:
                    term = terms[0]
                    self.addTerm(term.getTerm().getName(), termId)
                    termId = termId + 1
                    previousTerm = term
                    i = 1
                    while i < len(terms):
                        term: TermOccurrence = terms[i]
                        if term.isDifferent(previousTerm):
                            self.addTerm(term.getTerm().getName(), termId)
                            termId = termId + 1
                        i = i + 1
                        previousTerm = term
            else:
                wordList: [Word] = []
                for word in fileNameOrTerms:
                    wordList.append(Word(word))
                wordList.sort(key=cmp_to_key(comparator))
                termID = 0
                for termWord in wordList:
                    self.addTerm(termWord.getName(), termID)
                    termID = termID + 1

    def __getPosition(self, word: Word) -> int:
        lo = 0
        hi = len(self.words) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if self.comparator(self.words[mid], word) < 0:
                lo = mid + 1
            elif self.comparator(self.words[mid], word) > 0:
                hi = mid - 1
            else:
                return mid
        return -lo

    def addTerm(self, name: str, termId: int):
        middle = self.__getPosition(Word(name))
        if middle < 0:
            self.words.insert(-middle, Term(name, termId))

    def save(self, fileName: str):
        outfile = open(fileName, mode='w', encoding='utf-8')
        for word in self.words:
            term: Term = word
            outfile.write(term.getTermId().__str__() + " " + term.getName() + "\n")
        outfile.close()