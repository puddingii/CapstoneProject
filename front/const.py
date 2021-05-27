import sys


class Const:
    def __init__(self):
        self.__dict__['MEMBER_LINES_KEYS'] = ['ID', 'NAME', 'PHONE', 'ADDRESS']
        self.__dict__['VISITOR_LINES_KEYS'] = ['NAME', 'DATE', 'PHONE', 'ADDRESS']
        self.__dict__['MEMBER_TXT_PATH'] = 'log/member.txt'
        self.__dict__['VISITOR_TXT_PATH'] = 'log/visitor.txt'

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise Exception('Error: Cannot assign a value to a variable.')
        self.__dict__[name] = value

    def __delattr__(self, name):
        if name in self.__dict__:
            raise Exception('Error: Unable to delete variable.')


# noinspection PyTypeChecker
sys.modules[__name__] = Const()
