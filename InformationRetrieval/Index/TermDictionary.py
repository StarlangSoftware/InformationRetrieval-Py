from functools import cmp_to_key

from Dictionary.Dictionary import Dictionary
from Dictionary.Word import Word

from InformationRetrieval.Index.Term import Term
from InformationRetrieval.Index.TermOccurrence import TermOccurrence


class TermDictionary(Dictionary):

    def __init__(self,
                 comparator: object,
                 fileNameOrTerms = None):
        super().__init__(comparator)
        if fileNameOrTerms is not None:
            if isinstance(fileNameOrTerms, str):
                file_name: str = fileNameOrTerms
                input_file = open(file_name + "-dictionary.txt", mode='r', encoding='utf-8')
                line = input_file.readline().strip()
                while line != "":
                    term_id = int(line[0:line.index(" ")])
                    self.words.append(Term(line[line.index(" ") + 1:], term_id))
                    line = input_file.readline().strip()
                input_file.close()
            else:
                if isinstance(fileNameOrTerms, list):
                    term_id = 0
                    terms: [TermOccurrence] = fileNameOrTerms
                    if len(terms) > 0:
                        term = terms[0]
                        self.addTerm(term.getTerm().getName(), term_id)
                        term_id = term_id + 1
                        previous_term = term
                        i = 1
                        while i < len(terms):
                            term: TermOccurrence = terms[i]
                            if term.isDifferent(previous_term):
                                self.addTerm(term.getTerm().getName(), term_id)
                                term_id = term_id + 1
                            i = i + 1
                            previous_term = term
                else:
                    word_list: [Word] = []
                    for word in fileNameOrTerms:
                        word_list.append(Word(word))
                    word_list.sort(key=cmp_to_key(comparator))
                    term_id = 0
                    for term_word in word_list:
                        self.addTerm(term_word.getName(), term_id)
                        term_id = term_id + 1

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
        return -(lo + 1)

    def addTerm(self,
                name: str,
                termId: int):
        middle = self.__getPosition(Word(name))
        if middle < 0:
            self.words.insert(-middle - 1, Term(name, termId))

    def save(self, fileName: str):
        output_file = open(fileName + "-dictionary.txt", mode='w', encoding='utf-8')
        for word in self.words:
            term: Term = word
            output_file.write(term.getTermId().__str__() + " " + term.getName() + "\n")
        output_file.close()

    @staticmethod
    def constructNGrams(word: str,
                        termId: int,
                        k: int) -> [TermOccurrence]:
        n_grams = []
        if len(word) >= k - 1:
            for j in range(-1, len(word) - k + 2):
                if j == -1:
                    term = "$" + word[0:k - 1]
                elif j == len(word) - k + 1:
                    term = word[j: j + k - 1] + "$"
                else:
                    term = word[j: j + k]
                n_grams.append(TermOccurrence(Word(term), termId, j))
        return n_grams

    def constructTermsFromDictionary(self, k: int) -> [TermOccurrence]:
        terms : [TermOccurrence] = []
        for i in range(self.size()):
            word = self.getWordWithIndex(i).getName()
            terms.extend(TermDictionary.constructNGrams(word, i, k))
        terms.sort(key=cmp_to_key(TermOccurrence.termOccurrenceComparator))
        return terms
