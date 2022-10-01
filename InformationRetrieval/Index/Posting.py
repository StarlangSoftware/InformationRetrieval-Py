class Posting:

    __id: int

    def __init__(self, Id: int):
        self.__id = Id

    def getId(self) -> int:
        return self.__id
