from InformationRetrieval.Document.AbstractCollection import AbstractCollection
from InformationRetrieval.Document.Parameter import Parameter
from InformationRetrieval.Index.PositionalPostingList import PositionalPostingList
from InformationRetrieval.Index.PostingList import PostingList


class DiskCollection(AbstractCollection):

    def __init__(self,
                 directory: str,
                 parameter: Parameter):
        super().__init__(directory, parameter)

    def notCombinedAllIndexes(self, currentIdList: [int]) -> bool:
        for _id in currentIdList:
            if _id != -1:
                return True
        return False

    def selectIndexesWithMinimumTermIds(self, currentIdList: [int]) -> [int]:
        result = []
        _min = float('inf')
        for _id in currentIdList:
            if _id != -1 and _id < _min:
                _min = _id
        for i in range(len(currentIdList)):
            if currentIdList[i] == _min:
                result.append(i)
        return result

    def combineMultipleInvertedIndexesInDisk(self,
                                             name: str,
                                             tmpName: str,
                                             blockCount: int):
        current_id_list = []
        current_posting_lists = []
        files = []
        output_file = open(name + "-postings.txt", mode="w", encoding="utf-8")
        for i in range(blockCount):
            files.append(open("tmp-" + tmpName + i.__str__() + "-postings.txt", mode="r", encoding="utf-8"))
            line = files[i].readline().strip()
            items = line.split(" ")
            current_id_list.append(int(items[0]))
            line = files[i].readline().strip()
            current_posting_lists.append(PostingList(line))
        while self.notCombinedAllIndexes(current_id_list):
            indexes_to_combine = self.selectIndexesWithMinimumTermIds(current_id_list)
            merged_posting_list = current_posting_lists[indexes_to_combine[0]]
            for i in range(1, len(indexes_to_combine)):
                merged_posting_list = merged_posting_list.union(current_posting_lists[indexes_to_combine[i]])
            merged_posting_list.writeToFile(output_file, current_id_list[indexes_to_combine[0]])
            for i in indexes_to_combine:
                line = files[i].readline().strip()
                if line != "":
                    items = line.split(" ")
                    current_id_list[i] = int(items[0])
                    line = files[i].readline().strip()
                    current_posting_lists[i] = PostingList(line)
                else:
                    current_id_list[i] = -1
        for i in range(blockCount):
            files[i].close()
        output_file.close()

    def combineMultiplePositionalIndexesInDisk(self,
                                               name: str,
                                               blockCount: int):
        current_id_list = []
        current_posting_lists = []
        files = []
        output_file = open(name + "-positionalPostings.txt", mode="w", encoding="utf-8")
        for i in range(blockCount):
            files.append(open("tmp-" + i.__str__() + "-positionalPostings.txt", mode="r", encoding="utf-8"))
            line = files[i].readline().strip()
            items = line.split(" ")
            current_id_list.append(int(items[0]))
            current_posting_lists.append(PositionalPostingList(files[i], int(items[1])))
        while self.notCombinedAllIndexes(current_id_list):
            indexes_to_combine = self.selectIndexesWithMinimumTermIds(current_id_list)
            merged_posting_list = current_posting_lists[indexes_to_combine[0]]
            for i in range(1, len(indexes_to_combine)):
                merged_posting_list = merged_posting_list.union(current_posting_lists[indexes_to_combine[i]])
            merged_posting_list.writeToFile(output_file, current_id_list[indexes_to_combine[0]])
            for i in indexes_to_combine:
                line = files[i].readline().strip()
                if line != "":
                    items = line.split(" ")
                    current_id_list[i] = int(items[0])
                    current_posting_lists[i] = PositionalPostingList(files[i], int(items[1]))
                else:
                    current_id_list[i] = -1
        for i in range(blockCount):
            files[i].close()
        output_file.close()
