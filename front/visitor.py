import const


class Visitor:
    def __init__(self, path: str):
        self.__path = path
        self.__visitor_list = self.read_txt()

    @staticmethod
    def split_line(line: str) -> dict:
        nodes = dict()
        words = line.split()
        for i, key in enumerate(const.VISITOR_LINES_KEYS):
            nodes[key] = words[i]
        return nodes

    def read_txt(self) -> list:
        visitor_list = list()
        with open(self.__path, 'r', encoding='UTF-8') as file:
            while True:
                line = file.readline()
                if not line:
                    break
                visitor = self.split_line(line)
                visitor_list.append(visitor)
        return visitor_list

    @property
    def get_visitor_list(self) -> list:
        return self.__visitor_list
