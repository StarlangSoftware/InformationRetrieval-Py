from InformationRetrieval.Index.CategoryNode import CategoryNode
from InformationRetrieval.Index.TermDictionary import TermDictionary


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

    def topNString(self, dictionary: TermDictionary, N: int) -> str:
        queue = [self.__root]
        result = ""
        while len(queue) > 0:
            node = queue.pop(0)
            if node != self.__root:
                result = result + node.topNString(dictionary, N) + "\n"
            queue.extend(node.getChildren())
        return result

    def __repr__(self):
        return self.__root.__repr__()
