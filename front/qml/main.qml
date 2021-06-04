import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.15
import "components"

Window {
    id: mainWindow
    color: "#00000000"
    width: 1280
    height: 720
    visible: true
    title: qsTr("Hello World")
    flags: Qt.Window|Qt.FramelessWindowHint

    Rectangle {
        id: background
        color: "#181c2c"
        anchors.fill: parent
        anchors.leftMargin: 0
        anchors.rightMargin: 0
        anchors.topMargin: 0
        anchors.bottomMargin: 0

        Rectangle {
            id: titleBar
            height: 35
            color: "#070b1b"
            anchors.left: background.left
            anchors.right: background.right
            anchors.top: background.top
            anchors.leftMargin: 0
            anchors.rightMargin: 0
            anchors.topMargin: 0

            DragHandler {
                onActiveChanged: {
                    if(active) {
                        mainWindow.startSystemMove()
                    }
                }
            }

            Row {
                id: titleInformation
                height:35
                anchors.left: titleBar.left
                anchors.leftMargin: 10

                Image {
                    id: logoImage
                    width: 28
                    height: 28
                    source: "../images/svg/mask.svg"
                    sourceSize.width: 35
                    sourceSize.height: 35
                    fillMode: Image.PreserveAspectFit
                    anchors.verticalCenter: titleInformation.verticalCenter
                }

                Label {
                    id: logoTitleLabel
                    color: "#ffffff"
                    text: qsTr("턱스트 멈춰!")
                    font.family: "Segoe UI"
                    font.bold: true
                    font.pointSize: 13
                    anchors.left: logoImage.right
                    anchors.leftMargin: 5
                    anchors.verticalCenter: titleInformation.verticalCenter
                }
            }

            Row {
                id: rowBtn
                width: 70
                height: 35
                anchors.right: titleBar.right
                anchors.top: titleBar.top
                anchors.bottom: titleBar.bottom
                anchors.rightMargin: 0
                anchors.topMargin: 0
                anchors.bottomMargin: 0

                // Minimize Button
                TopBarButton {
                    id: btnMinimize
                    onClicked: {
                        mainWindow.showMinimized()
                    }
                }

                // Close Button
                TopBarButton {
                    id: btnClose
                    btnColorClicked: "#ff3333"
                    btnIconSource: "../images/svg/close_icon.svg"
                    onClicked: mainWindow.close()
                }
            }
        }
        Rectangle {
            id: menuList
            width: 200
            color: "#070b1b"
            anchors.top: titleBar.bottom
            anchors.left: background.left
            anchors.bottom: processLogBar.top

            Column {
                id: columnLeftMenu
                width: 200
                height: 210
                anchors.top: titleBar.bottom
                anchors.horizontalCenter: menuList.horizontalCenter

//                LeftMenuButton {
//                    id: btnCam
//                    onClicked: {
//                        isVisible = true
//                        btnMember.isVisible = false
//                        btnVisitor.isVisible = false
//                        pagesView.setSource(Qt.resolvedUrl("pages/camPage.qml"))
//                    }
//                }

                LeftMenuButton {
                    id: btnMember
                    imagePath: "../images/svg/list.svg"
                    onClicked: {
                        isVisible = true
                        //btnCam.isVisible = false
                        btnVisitor.isVisible = false
                        pagesView.setSource(Qt.resolvedUrl("pages/memberPage.qml"))
                        backend.set_member_count()
                        backend.set_member_value()
                    }
                }
                LeftMenuButton {
                    id: btnVisitor
                    imagePath: "../images/svg/profile-user.svg"
                    onClicked: {
                        isVisible = true
                        btnMember.isVisible = false
                        //btnCam.isVisible = false
                        pagesView.setSource(Qt.resolvedUrl("pages/visitorPage.qml"))
                        backend.set_visitor_count()
                        backend.set_visitor_value()
                    }
                }
            }
        }

        Rectangle {
            id: processLogBar
            height: 35
            color: "#070b1b"
            anchors.left: background.left
            anchors.right: background.right
            anchors.bottom: background.bottom

            Label {
                id: logText
                color: "#ffffff"
                text: qsTr("Log : ")
                font.family: "Segoe UI"
                font.bold: true
                font.pointSize: 13
                anchors.left: processLogBar.left
                anchors.leftMargin: 20
                anchors.verticalCenter: processLogBar.verticalCenter
            }
        }

        Rectangle {
            id: contentPage
            color: "#00000000"
            clip: true
            anchors.left: menuList.right
            anchors.right: background.right
            anchors.top: titleBar.bottom
            anchors.bottom: processLogBar.top
            anchors.leftMargin: 0
            anchors.rightMargin: 0
            anchors.topMargin: 0
            anchors.bottomMargin: 0

            Loader {
                id: pagesView
                anchors.fill: contentPage
                source: Qt.resolvedUrl("pages/memberPage.qml")
            }
        }
    }

    Connections{
        target: backend
    }
}
