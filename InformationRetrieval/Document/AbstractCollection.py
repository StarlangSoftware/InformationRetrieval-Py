import os

from InformationRetrieval.Document.Document import Document
from InformationRetrieval.Document.DocumentType import DocumentType
from InformationRetrieval.Document.Parameter import Parameter
from InformationRetrieval.Index.CategoryTree import CategoryTree
from InformationRetrieval.Index.IncidenceMatrix import IncidenceMatrix
from InformationRetrieval.Index.InvertedIndex import InvertedIndex
from InformationRetrieval.Index.NGramIndex import NGramIndex
from InformationRetrieval.Index.PositionalIndex import PositionalIndex
from InformationRetrieval.Index.TermDictionary import TermDictionary


class AbstractCollection:

    dictionary: TermDictionary
    phrase_dictionary: TermDictionary
    bi_gram_dictionary: TermDictionary
    tri_gram_dictionary: TermDictionary
    documents: [Document]
    incidence_matrix: IncidenceMatrix
    inverted_index: InvertedIndex
    bi_gram_index: NGramIndex
    tri_gram_index: NGramIndex
    positional_index: PositionalIndex
    phrase_index: InvertedIndex
    phrase_positional_index: PositionalIndex
    comparator: object
    name: str
    parameter: Parameter
    category_tree: CategoryTree
    attribute_list: set

    def __init__(self,
                 directory: str,
                 parameter: Parameter):
        self.name = directory
        self.comparator = parameter.getWordComparator()
        self.parameter = parameter
        if self.parameter.getDocumentType() == DocumentType.CATEGORICAL:
            self.loadAttributeList()
        self.documents = []
        for root, dirs, files in os.walk(directory):
            file_limit = len(files)
            if parameter.limitNumberOfDocumentsLoaded():
                file_limit = parameter.getDocumentLimit()
            j = 0
            files.sort()
            for file in files:
                if j >= file_limit:
                    break
                file_name = os.path.join(root, file)
                if file.endswith(".txt"):
                    document = Document(parameter.getDocumentType(), file_name, file, j)
                    self.documents.append(document)
                    j = j + 1
        if parameter.getDocumentType() == DocumentType.CATEGORICAL:
            self.loadCategories()

    def loadCategories(self):
        self.category_tree = CategoryTree(self.name)
        input_file = open(self.name + "-categories.txt", mode="r", encoding="utf-8")
        line = input_file.readline().strip()
        while line != "":
            items = line.split("\t")
            doc_id = int(items[0])
            self.documents[doc_id].setCategory(self.category_tree, items[1])
            line = input_file.readline().strip()
        input_file.close()

    def loadAttributeList(self):
        self.attribute_list = set()
        input_file = open(self.name + "-attributelist.txt", mode="r", encoding="utf-8")
        line = input_file.readline().strip()
        while line != "":
            self.attribute_list.add(line)
            line = input_file.readline().strip()
        input_file.close()

    def size(self) -> int:
        return len(self.documents)

    def vocabularySize(self) -> int:
        return self.dictionary.size()

    def constructNGramIndex(self):
        terms = self.dictionary.constructTermsFromDictionary(2)
        self.bi_gram_dictionary = TermDictionary(self.comparator, terms)
        self.bi_gram_index = NGramIndex(self.bi_gram_dictionary, terms)
        terms = self.dictionary.constructTermsFromDictionary(3)
        self.tri_gram_dictionary = TermDictionary(self.comparator, terms)
        self.tri_gram_index = NGramIndex(self.tri_gram_dictionary, terms)
