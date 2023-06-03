from __future__ import annotations
from DataStructure.Heap.MinHeap import MinHeap

from InformationRetrieval.Query.QueryResultItem import QueryResultItem


class QueryResult:

    __items: [QueryResultItem]

    def __init__(self):
        self.__items = []

    def add(self, docId: int, score: float = 0.0):
        self.__items.append(QueryResultItem(docId, score))

    def size(self) -> int:
        return len(self.__items)

    def getItems(self) -> [QueryResultItem]:
        return self.__items

    def intersectionFastSearch(self, queryResult: QueryResult) -> QueryResult:
        result = QueryResult()
        i = 0
        j = 0
        while i < self.size() and j < queryResult.size():
            item1 = self.__items[i]
            item2 = queryResult.__items[j]
            if item1.getDocId() == item2.getDocId():
                result.add(item1.getDocId())
                i = i + 1
                j = j + 1
            else:
                if item1.getDocId() < item2.getDocId():
                    i = i + 1
                else:
                    j = j + 1
        return result

    def intersectionBinarySearch(self, queryResult: QueryResult) -> QueryResult:
        result = QueryResult()
        for searched_item in self.__items:
            low = 0
            high = queryResult.size() - 1
            middle = (low + high) // 2
            found = False
            while low <= high:
                if searched_item.getDocId() > queryResult.__items[middle].getDocId():
                    low = middle + 1
                elif searched_item.getDocId() < queryResult.__items[middle].getDocId():
                    high = middle - 1
                else:
                    found = True
                    break
                middle = (low + high) // 2
            if found:
                result.add(searched_item.getDocId(), searched_item.getScore())
        return result

    def intersectionLinearSearch(self, queryResult: QueryResult) -> QueryResult:
        result = QueryResult()
        for searched_item in self.__items:
            for item in queryResult.__items:
                if searched_item.getDocId() == item.getDocId():
                    result.add(searched_item.getDocId(), searched_item.getScore())
        return result

    def getBest(self, K: int):
        minHeap = MinHeap(K, lambda x1, x2: 1 if x1.getScore() > x2.getScore() else (0 if x1.getScore() == x2.getScore() else -1))
        i = 0
        while i < K and i < len(self.__items):
            minHeap.insert(self.__items[i])
            i = i + 1
        for i in range(K + 1, len(self.__items)):
            top_item = minHeap.delete()
            if isinstance(top_item, QueryResultItem) and top_item.getScore() > self.__items[i].getScore():
                minHeap.insert(top_item)
            else:
                minHeap.insert(self.__items[i])
        self.__items.clear()
        i = 0
        while i < K and not minHeap.isEmpty():
            self.__items.insert(0, minHeap.delete())
            i = i + 1

    def __repr__(self):
        return f"{self.__items}"
