from InformationRetrieval.Index.CategoryNode import CategoryNode
from InformationRetrieval.Index.TermDictionary import TermDictionary
from InformationRetrieval.Query.CategoryDeterminationType import CategoryDeterminationType
from InformationRetrieval.Query.Query import Query


class CategoryTree:

    __root: CategoryNode

    def __init__(self, rootName: str):
        """
        Simple constructor of the tree. Sets the root node of the tree.
        :param rootName: Category name of the root node.
        """
        self.__root = CategoryNode(rootName, None)

    def addCategoryHierarchy(self, hierarchy: str) -> CategoryNode:
        """
        Adds a path (and if required nodes in the path) to the category tree according to the hierarchy string. Hierarchy
        string is obtained by concatenating the names of all nodes in the path from root node to a leaf node separated
        with '%'.
        :param hierarchy: Hierarchy string
        :return: The leaf node added when the hierarchy string is processed.
        """
        categories = hierarchy.split("%")
        current = self.__root
        for category in categories:
            node = current.getChild(category)
            if node is None:
                node = CategoryNode(category, current)
            current = node
        return current

    def getCategories(self,
                      query: Query,
                      dictionary: TermDictionary,
                      categoryDeterminationType: CategoryDeterminationType) -> [CategoryNode]:
        """
        The method checks the query words in the category words of all nodes in the tree and returns the nodes that
        satisfies the condition. If any word in the query appears in any category word, the node will be returned.
        :param query: Query string
        :param dictionary: Term dictionary
        :param categoryDeterminationType: Category determination type
        :return: The category nodes whose names contain at least one word from the query string
        """
        result = []
        if categoryDeterminationType == CategoryDeterminationType.KEYWORD:
            self.__root.getCategoriesWithKeyword(query, result)
        elif categoryDeterminationType == CategoryDeterminationType.COSINE:
            self.__root.getCategoriesWithCosine(query, dictionary, result)
        return result

    def setRepresentativeCount(self, representativeCount: int):
        """
        The method sets the representative count. The representative count filters the most N frequent words.
        :param representativeCount: Number of representatives.
        """
        self.__root.setRepresentativeCount(representativeCount)

    def __repr__(self):
        return self.__root.__repr__()
