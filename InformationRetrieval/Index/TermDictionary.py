from functools import cmp_to_key

from Dictionary.Dictionary import Dictionary
from Dictionary.Word import Word

from InformationRetrieval.Index.Term import Term
from InformationRetrieval.Index.TermOccurrence import TermOccurrence


class TermDictionary(Dictionary):

    def constructor1(self, fileName: str):
        """
        Constructor of the TermDictionary. Reads the terms and their ids from the given dictionary file. Each line stores
        the term id and the term name separated via space.
        :param fileName: Dictionary file name
        """
        file_name: str = fileName
        input_file = open(file_name + "-dictionary.txt", mode='r', encoding='utf-8')
        line = input_file.readline().strip()
        while line != "":
            term_id = int(line[0:line.index(" ")])
            self.words.append(Term(line[line.index(" ") + 1:], term_id))
            line = input_file.readline().strip()
        input_file.close()

    def constructor2(self, terms: list):
        """
        Constructs the TermDictionary from a list of tokens (term occurrences). The terms array should be sorted
        before calling this method. Constructs the distinct terms and their corresponding term ids.
        :param terms: Sorted list of tokens in the memory collection.
        """
        term_id = 0
        terms: [TermOccurrence] = terms
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

    def constructor3(self, comparator: object, words: set):
        """
        Constructs the TermDictionary from a hash set of tokens (strings). Constructs sorted dictinct terms array and
        their corresponding term ids.
        :param comparator: Comparator method to compare two terms.
        :param words: Hash set of tokens in the memory collection.
        """
        word_list: [Word] = []
        for word in words:
            word_list.append(Word(word))
        word_list.sort(key=cmp_to_key(comparator))
        term_id = 0
        for term_word in word_list:
            self.addTerm(term_word.getName(), term_id)
            term_id = term_id + 1

    def __init__(self,
                 comparator: object,
                 fileNameOrTerms = None):
        super().__init__(comparator)
        if fileNameOrTerms is not None:
            if isinstance(fileNameOrTerms, str):
                self.constructor1(fileNameOrTerms)
            else:
                if isinstance(fileNameOrTerms, list):
                    self.constructor2(fileNameOrTerms)
                else:
                    self.constructor3(comparator, fileNameOrTerms)

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
        """
        Adds a new term to the sorted words array. First the term is searched in the words array using binary search,
        then the word is added into the correct place.
        :param name: Lemma of the term
        :param termId: Id of the term
        """
        middle = self.__getPosition(Word(name))
        if middle < 0:
            self.words.insert(-middle - 1, Term(name, termId))

    def save(self, fileName: str):
        """
        Saves the term dictionary into the dictionary file. Each line stores the term id and the term name separated via
        space.
        :param fileName: Dictionary file name. Real dictionary file name is created by attaching -dictionary.txt to this
                         file name
        """
        output_file = open(fileName + "-dictionary.txt", mode='w', encoding='utf-8')
        for word in self.words:
            term: Term = word
            output_file.write(term.getTermId().__str__() + " " + term.getName() + "\n")
        output_file.close()

    @staticmethod
    def constructNGrams(word: str,
                        termId: int,
                        k: int) -> [TermOccurrence]:
        """
        Constructs all NGrams from a given word. For example, 3 grams for word "term" are "$te", "ter", "erm", "rm$".
        :param word: Word for which NGrams will b created.
        :param termId: Term id to add into the posting list.
        :param k: N in NGram.
        :return: An array of NGrams for a given word.
        """
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
        """
        Constructs all NGrams for all words in the dictionary. For example, 3 grams for word "term" are "$te", "ter",
        "erm", "rm$".
        :param k: N in NGram.
        :return: A sorted array of NGrams for all words in the dictionary.
        """
        terms : [TermOccurrence] = []
        for i in range(self.size()):
            word = self.getWordWithIndex(i).getName()
            terms.extend(TermDictionary.constructNGrams(word, i, k))
        terms.sort(key=cmp_to_key(TermOccurrence.termOccurrenceComparator))
        return terms
