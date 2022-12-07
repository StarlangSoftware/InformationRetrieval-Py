from InformationRetrieval.Index.CategoryNode import CategoryNode
from InformationRetrieval.Index.TermDictionary import TermDictionary
from InformationRetrieval.Query.CategoryDeterminationType import CategoryDeterminationType
from InformationRetrieval.Query.Query import Query


class CategoryTree:

    __root: CategoryNode

    def __init__(self, rootName: str):
        self.__root = CategoryNode(rootName, None)

    def addCategoryHierarchy(self, hierarchy: str) -> CategoryNode:
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
        result = []
        if categoryDeterminationType == CategoryDeterminationType.KEYWORD:
            self.__root.getCategoriesWithKeyword(query, result)
        elif categoryDeterminationType == CategoryDeterminationType.COSINE:
            self.__root.getCategoriesWithCosine(query, dictionary, result)
        return result

    def setRepresentativeCount(self, representativeCount: int):
        self.__root.setRepresentativeCount(representativeCount)

    def __repr__(self):
        return self.__root.__repr__()
