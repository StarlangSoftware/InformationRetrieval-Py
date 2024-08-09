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
        """
        In single pass in memory indexing, the index files are merged to get the final index file. This method
        checks if all parallel index files are combined or not.
        :param currentIdList: Current pointers for the terms in parallel index files. currentIdList[0] is the current term
                             in the first index file to be combined, currentIdList[2] is the current term in the second
                             index file to be combined etc.
        :return: True, if all merge operation is completed, false otherwise.
        """
        for _id in currentIdList:
            if _id != -1:
                return True
        return False

    def selectIndexesWithMinimumTermIds(self, currentIdList: [int]) -> [int]:
        """
        In single pass in memory indexing, the index files are merged to get the final index file. This method
        identifies the indexes whose terms to be merged have the smallest term id. They will be selected and
        combined in the next phase.
        :param currentIdList: Current pointers for the terms in parallel index files. currentIdList[0] is the current term
                             in the first index file to be combined, currentIdList[2] is the current term in the second
                             index file to be combined etc.
        :return: An array list of indexes for the index files, whose terms to be merged have the smallest term id.
        """
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
        """
        In single pass in memory indexing, the index files are merged to get the final index file. This method
        implements the merging algorithm. Reads the index files in parallel and at each iteration merges the posting
        lists of the smallest term and put it to the merged index file. Updates the pointers of the indexes accordingly.
        :param name: Name of the collection.
        :param tmpName: Temporary name of the index files.
        :param blockCount: Number of index files to be merged.
        """
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
        """
        In single pass in memory indexing, the index files are merged to get the final index file. This method
        implements the merging algorithm. Reads the index files in parallel and at each iteration merges the positional
        posting lists of the smallest term and put it to the merged index file. Updates the pointers of the indexes accordingly.
        :param name: Name of the collection.
        :param blockCount: Number of index files to be merged.
        """
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
