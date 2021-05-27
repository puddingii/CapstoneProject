import const


class Member:
    def __init__(self, path: str):
        self.__path = path
        self.__member_list = self.read_txt()

    @staticmethod
    def split_line(line: str) -> dict:
        nodes = dict()
        words = line.split()
        for i, key in enumerate(const.MEMBER_LINES_KEYS):
            nodes[key] = words[i]
        return nodes

    @staticmethod
    def assemble_line(member: dict) -> str:
        line = ' '.join(member.values())
        return line

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

    def write_text(self, member: dict):
        with open(self.__path, 'a', encoding='UTF-8') as file:
            file.write(self.assemble_line(member=member) + '\n')

    def update_text(self, index: int):
        with open(self.__path, 'w', encoding='UTF-8') as file:
            for i, member_info in enumerate(self.__member_list):
                if i != index:
                    file.write(self.assemble_line(member=member_info) + '\n')

    def create_member(self, line: str):
        member = self.split_line(line)
        self.__member_list.append(member)
        self.write_text(member=member)

    def delete_member(self, search_id: str):
        for i, member_info in enumerate(self.__member_list):
            if search_id == member_info[const.MEMBER_LINES_KEYS[0]]:
                self.update_text(index=i)
                del self.__member_list[i]
                break

    @property
    def get_member_list(self) -> list:
        return self.__member_list
