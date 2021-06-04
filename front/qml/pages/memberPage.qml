import QtQuick 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.15
import "../components"

Item {
    ListModel {
        id: memberList
    }

    QtObject {
        id: internal
        property string idValue: ""
        property string nameValue: ""
        property string phoneValue: ""
        property int count: 0
    }

    Connections {
        target: backend

        function onSetMemberCount(count) {
            internal.count += count
        }
        function onSetMemberIdValue(idValue) {
            internal.idValue = idValue
        }
        function onSetMemberNameValue(nameValue) {
            internal.nameValue = nameValue
        }
        function onSetMemberPhoneValue(phoneValue) {
            internal.phoneValue = phoneValue
        }
        function onSetMemberAddressValue(addressValue) {
            memberList.append({"idValue": internal.idValue,
                               "nameValue": internal.nameValue,
                               "phoneValue": internal.phoneValue,
                               "addressValue": addressValue})
        }
    }

    Rectangle {
        id: background
        width: 1080
        height: 650
        color: "#00000000"

        Rectangle {
            id: inputBackgound
            height: 66
            color: "#070b1b"
            radius: 8
            anchors.left: background.left
            anchors.right: background.right
            anchors.top: background.top
            anchors.leftMargin: 25
            anchors.rightMargin: 25
            anchors.topMargin: 20

            CustomTextField {
                id: textarea
                width: 864
                height: 40
                anchors.left: inputBackgound.left
                anchors.leftMargin: 12
                anchors.verticalCenter: inputBackgound.verticalCenter
            }

            TextButton {
                id: createBtn
                anchors.left: textarea.right
                anchors.leftMargin: 10
                anchors.verticalCenter: inputBackgound.verticalCenter
                onClicked: {
                    backend.get_member_information(textarea.text)
                }
            }

            TextButton {
                id: deleteBtn
                textValue: "DELETE"
                anchors.left: createBtn.right
                anchors.leftMargin: 10
                anchors.verticalCenter: inputBackgound.verticalCenter
                onClicked: {
                    memberList.clear()
                    internal.count = 0
                    backend.get_member_index(textarea.text)
                }
            }
        }

        Rectangle {
            id: tableBackgound
            color: "#070b1b"
            radius: 8
            anchors.left: background.left
            anchors.right: background.right
            anchors.top: inputBackgound.bottom
            anchors.bottom: background.bottom
            anchors.leftMargin: 25
            anchors.rightMargin: 25
            anchors.topMargin: 15
            anchors.bottomMargin: 20

            Rectangle {
                id: indexLabelsRow
                color: "#00000000"
                height: 35
                anchors.left: tableBackgound.left
                anchors.right: tableBackgound.right
                anchors.top: tableBackgound.top
                anchors.leftMargin: 10
                anchors.rightMargin: 10
                anchors.topMargin: 10

                Rectangle {
                    id: idLabelBackground
                    color: "#00000000"
                    width: 100
                    height: 35
                    anchors.left: indexLabelsRow.left
                    anchors.verticalCenter: indexLabelsRow.verticalCenter

                    Label {
                        id: idLabel
                        color: "#ffffff"
                        text: qsTr("ID")
                        font.bold: true
                        font.family: "Segoe UI"
                        font.pointSize: 15
                        anchors.left: idLabelBackground.left
                        anchors.leftMargin: 10
                        anchors.verticalCenter: indexLabelsRow.verticalCenter
                    }
                }

                Rectangle {
                    id: nameLabelBackground
                    color: "#00000000"
                    width: 200
                    height: 35
                    anchors.left: idLabelBackground.right
                    anchors.verticalCenter: indexLabelsRow.verticalCenter

                    Label {
                        id: nameLabel
                        color: "#ffffff"
                        text: qsTr("NAME")
                        font.bold: true
                        font.family: "Segoe UI"
                        font.pointSize: 15
                        anchors.right: nameLabelBackground.right
                        anchors.rightMargin: 10
                        anchors.verticalCenter: indexLabelsRow.verticalCenter
                    }
                }

                Rectangle {
                    id: phoneLabelBackground
                    color: "#00000000"
                    width: 250
                    height: 35
                    anchors.left: nameLabelBackground.right
                    anchors.verticalCenter: indexLabelsRow.verticalCenter

                    Label {
                        id: phoneLabel
                        color: "#ffffff"
                        text: qsTr("PHONE")
                        font.bold: true
                        font.family: "Segoe UI"
                        font.pointSize: 15
                        anchors.right: phoneLabelBackground.right
                        anchors.rightMargin: 10
                        anchors.verticalCenter: indexLabelsRow.verticalCenter
                    }
                }

                Rectangle {
                    id: addressLabelBackground
                    color: "#00000000"
                    width: 460
                    height: 35
                    anchors.left: phoneLabelBackground.right
                    anchors.verticalCenter: indexLabelsRow.verticalCenter

                    Label {
                        id: addressLabel
                        color: "#ffffff"
                        text: qsTr("ADDRESS")
                        font.bold: true
                        font.family: "Segoe UI"
                        font.pointSize: 15
                        anchors.right: addressLabelBackground.right
                        anchors.rightMargin: 10
                        anchors.verticalCenter: indexLabelsRow.verticalCenter
                    }
                }
            }

            ToolSeparator {
                id: tableSeperator
                height: 5
                anchors.left: tableBackgound.left
                anchors.right: tableBackgound.right
                anchors.top: indexLabelsRow.bottom
                anchors.leftMargin: 10
                anchors.rightMargin: 10
            }

            Flickable {
                id: scrollview
                width: 1010
                clip: true
                anchors.left: tableBackgound.left
                anchors.right: tableBackgound.right
                anchors.top: tableSeperator.bottom
                anchors.bottom: tableBackgound.bottom
                anchors.leftMargin: 10
                anchors.rightMargin: 10
                anchors.topMargin: 10
                anchors.bottomMargin: 10

                ScrollBar {
                    id: verticalBar
                    hoverEnabled: true
                    active: hovered || pressed
                    orientation: Qt.Vertical
                    size: scrollview.height / memberListView.height
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    policy: ScrollBar.AlwaysOn

                    contentItem: Rectangle {
                        color: verticalBar.pressed ? "#41d400" : "#51ff04"
                        implicitWidth: 6
                        implicitHeight: 100
                        radius: 10
                    }
                }

                ListView {
                    id: memberListView
                    height: internal.count * 35
                    y: -verticalBar.position * height

                    model: memberList

                    delegate:
                        Rectangle {
                            id: element
                            color: "#00000000"
                            height: 35
                            anchors.left: tableBackgound.left
                            anchors.right: tableBackgound.right
                            anchors.top: tableBackgound.top
                            anchors.leftMargin: 10
                            anchors.rightMargin: 10
                            anchors.topMargin: 10

                            Rectangle {
                                id: idValueBackground
                                color: "#00000000"
                                width: 100
                                height: 35
                                anchors.left: element.left
                                anchors.verticalCenter: element.verticalCenter

                                Label {
                                    id: idLabelValue
                                    color: "#ffffff"
                                    text: idValue
                                    font.bold: true
                                    font.family: "Segoe UI"
                                    font.pointSize: 15
                                    anchors.left: seperator.left
                                    anchors.leftMargin: 10
                                    anchors.verticalCenter: element.verticalCenter
                                }

                                Rectangle {
                                    id: seperator
                                    color: "#ffffff"
                                    width: 5
                                    anchors.left: idValueBackground.left
                                    anchors.top: idValueBackground.top
                                    anchors.bottom: idValueBackground.bottom
                                    anchors.topMargin: 5
                                    anchors.bottomMargin: 5
                                    anchors.verticalCenter: element.verticalCenter
                                }
                            }

                            Rectangle {
                                id: nameValueBackground
                                color: "#00000000"
                                width: 200
                                height: 35
                                anchors.left: idValueBackground.right
                                anchors.verticalCenter: element.verticalCenter

                                Label {
                                    id: nameLabelValue
                                    color: "#ffffff"
                                    text: nameValue
                                    font.bold: true
                                    font.family: "Segoe UI"
                                    font.pointSize: 15
                                    anchors.right: nameValueBackground.right
                                    anchors.rightMargin: 10
                                    anchors.verticalCenter: element.verticalCenter
                                }
                            }

                            Rectangle {
                                id: phoneValueBackground
                                color: "#00000000"
                                width: 250
                                height: 35
                                anchors.left: nameValueBackground.right
                                anchors.verticalCenter: element.verticalCenter

                                Label {
                                    id: phoneLabelValue
                                    color: "#ffffff"
                                    text: phoneValue
                                    font.bold: true
                                    font.family: "Segoe UI"
                                    font.pointSize: 15
                                    anchors.right: phoneValueBackground.right
                                    anchors.rightMargin: 10
                                    anchors.verticalCenter: element.verticalCenter
                                }
                            }

                            Rectangle {
                                id: addressValueBackground
                                color: "#00000000"
                                width: 460
                                height: 35
                                anchors.left: phoneValueBackground.right
                                anchors.verticalCenter: element.verticalCenter

                                Label {
                                    id: addressLabelValue
                                    color: "#ffffff"
                                    text: addressValue
                                    font.bold: true
                                    font.family: "Segoe UI"
                                    font.pointSize: 15
                                    anchors.right: addressValueBackground.right
                                    anchors.rightMargin: 10
                                    anchors.verticalCenter: element.verticalCenter
                                }
                            }
                        }
                }
            }
        }
    }
}

/*##^##
Designer {
    D{i:0;autoSize:true;height:650;width:1080}
}
##^##*/
