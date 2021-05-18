class Member:
    def __init__(self, path: str):
        self.__path = path
        self.__member_list = self.read_txt()

    @staticmethod
    def split_line(line: str) -> dict:
        nodes = dict()
        words = line.split()
        MEMBER_LINES_KEYS = ['ID', 'NAME', 'PHONE', 'ADDRESS']
        for i, key in enumerate(MEMBER_LINES_KEYS):
            nodes[key] = words[i]
        return nodes

    def read_txt(self) -> list:
        member_list = list()
        with open(self.__path, 'r', encoding='UTF-8') as file:
            while True:
                line = file.readline()
                if not line:
                    break
                member = self.split_line(line)
                member_list.append(member)
        return member_list

    @property
    def get_member_list(self) -> list:
        return self.__member_list
