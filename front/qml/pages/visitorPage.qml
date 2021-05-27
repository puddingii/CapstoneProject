import QtQuick 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.15

Item {
    ListModel {
        id: visitorList
    }

    QtObject {
        id: internal
        property string nameValue: ""
        property string dateValue: ""
        property string phoneValue: ""
        property int count: 0
    }

    Connections {
        target: backend

        function onSetVisitorCount(count) {
            internal.count += count
        }
        function onSetVisitorIdValue(nameValue) {
            internal.nameValue = nameValue
        }
        function onSetVisitorNameValue(dateValue) {
            internal.dateValue = dateValue
        }
        function onSetVisitorPhoneValue(phoneValue) {
            internal.phoneValue = phoneValue
        }
        function onSetVisitorAddressValue(addressValue) {
            visitorList.append({"idValue": internal.nameValue,
                               "nameValue": internal.dateValue,
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
            id: tableBackgound
            color: "#01071E"
            radius: 8
            anchors.left: background.left
            anchors.right: background.right
            anchors.top: background.top
            anchors.bottom: background.bottom
            anchors.leftMargin: 25
            anchors.rightMargin: 25
            anchors.topMargin: 25
            anchors.bottomMargin: 25

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
                    id: nameLabelBackground
                    color: "#00000000"
                    width: 150
                    height: 35
                    anchors.left: indexLabelsRow.left
                    anchors.verticalCenter: indexLabelsRow.verticalCenter

                    Label {
                        id: nameLabel
                        color: "#ffffff"
                        text: qsTr("NAME")
                        font.bold: true
                        font.family: "Segoe UI"
                        font.pointSize: 15
                        anchors.left: nameLabelBackground.left
                        anchors.leftMargin: 10
                        anchors.verticalCenter: indexLabelsRow.verticalCenter
                    }
                }

                Rectangle {
                    id: dateLabelBackground
                    color: "#00000000"
                    width: 250
                    height: 35
                    anchors.left: nameLabelBackground.right
                    anchors.verticalCenter: indexLabelsRow.verticalCenter

                    Label {
                        id: dateLabel
                        color: "#ffffff"
                        text: qsTr("DATE")
                        font.bold: true
                        font.family: "Segoe UI"
                        font.pointSize: 15
                        anchors.right: dateLabelBackground.right
                        anchors.rightMargin: 10
                        anchors.verticalCenter: indexLabelsRow.verticalCenter
                    }
                }

                Rectangle {
                    id: phoneLabelBackground
                    color: "#00000000"
                    width: 250
                    height: 35
                    anchors.left: dateLabelBackground.right
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
                    width: 360
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
                    size: scrollview.height / visitorListView.height
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
                    id: visitorListView
                    height: internal.count * 35
                    y: -verticalBar.position * height

                    model: visitorList

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
                                id: nameValueBackground
                                color: "#00000000"
                                width: 150
                                height: 35
                                anchors.left: element.left
                                anchors.verticalCenter: element.verticalCenter

                                Label {
                                    id: nameLabelValue
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
                                    anchors.left: nameValueBackground.left
                                    anchors.top: nameValueBackground.top
                                    anchors.bottom: nameValueBackground.bottom
                                    anchors.topMargin: 5
                                    anchors.bottomMargin: 5
                                    anchors.verticalCenter: element.verticalCenter
                                }
                            }

                            Rectangle {
                                id: dateValueBackground
                                color: "#00000000"
                                width: 250
                                height: 35
                                anchors.left: nameValueBackground.right
                                anchors.verticalCenter: element.verticalCenter

                                Label {
                                    id: dateLabelValue
                                    color: "#ffffff"
                                    text: nameValue
                                    font.bold: true
                                    font.family: "Segoe UI"
                                    font.pointSize: 15
                                    anchors.right: dateValueBackground.right
                                    anchors.rightMargin: 10
                                    anchors.verticalCenter: element.verticalCenter
                                }
                            }

                            Rectangle {
                                id: phoneValueBackground
                                color: "#00000000"
                                width: 250
                                height: 35
                                anchors.left: dateValueBackground.right
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
                                width: 360
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
