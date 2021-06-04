# This Python file uses the following encoding: utf-8
import sys
import os
import const


from member import Member
from visitor import Visitor
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtCore import QObject, Slot, Signal


class MainWindow(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.__member = Member(path=const.MEMBER_TXT_PATH)
        self.__visitor = Visitor(path=const.VISITOR_TXT_PATH)
        self.set_member_value()

    # signal set member value texts
    setMemberIdValue = Signal(str)
    setMemberNameValue = Signal(str)
    setMemberPhoneValue = Signal(str)
    setMemberAddressValue = Signal(str)
    setMemberCount = Signal(int)

    # signal set visitor value texts
    setVisitorIdValue = Signal(str)
    setVisitorNameValue = Signal(str)
    setVisitorPhoneValue = Signal(str)
    setVisitorAddressValue = Signal(str)
    setVisitorCount = Signal(int)

    @Slot()
    def set_member_count(self):
        self.setMemberCount.emit(len(self.__member.get_member_list))

    @Slot()
    def set_member_value(self):
        for member_info in self.__member.get_member_list:
            self.setMemberIdValue.emit(member_info[const.MEMBER_LINES_KEYS[0]])
            self.setMemberNameValue.emit(
                member_info[const.MEMBER_LINES_KEYS[1]])
            self.setMemberPhoneValue.emit(
                member_info[const.MEMBER_LINES_KEYS[2]])
            self.setMemberAddressValue.emit(
                member_info[const.MEMBER_LINES_KEYS[3]])

    @Slot(str)
    def get_member_information(self, member_info):
        self.__member.create_member(line=member_info)
        member_list = self.__member.get_member_list
        self.setMemberIdValue.emit(member_list[-1][const.MEMBER_LINES_KEYS[0]])
        self.setMemberNameValue.emit(
            member_list[-1][const.MEMBER_LINES_KEYS[1]])
        self.setMemberPhoneValue.emit(
            member_list[-1][const.MEMBER_LINES_KEYS[2]])
        self.setMemberAddressValue.emit(
            member_list[-1][const.MEMBER_LINES_KEYS[3]])
        self.setMemberCount.emit(1)

    @Slot(str)
    def get_member_index(self, member_index):
        self.__member.delete_member(search_id=member_index)
        self.set_member_count()
        self.set_member_value()

    @Slot()
    def set_visitor_count(self):
        self.setVisitorCount.emit(len(self.__visitor.get_visitor_list))

    @Slot()
    def set_visitor_value(self):
        for visitor_info in self.__visitor.get_visitor_list:
            self.setVisitorIdValue.emit(
                visitor_info[const.VISITOR_LINES_KEYS[0]])
            self.setVisitorNameValue.emit(
                visitor_info[const.VISITOR_LINES_KEYS[1]])
            self.setVisitorPhoneValue.emit(
                visitor_info[const.VISITOR_LINES_KEYS[2]])
            self.setVisitorAddressValue.emit(
                visitor_info[const.VISITOR_LINES_KEYS[3]])


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    # Get Context
    main = MainWindow()
    engine.rootContext().setContextProperty("backend", main)
    engine.load(os.path.join(os.path.dirname(__file__), "qml/main.qml"))

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())
