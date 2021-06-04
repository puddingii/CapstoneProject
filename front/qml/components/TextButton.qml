import QtQuick 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.15

Button {
    id: textButton

    property color colorDefault: "#151515"
    property color colorMouseOver: "#1c1c1c"
    property color colorPressed: "#3f7ebd"
    property bool isVisible: false
    property string textValue: "CREATE"

    QtObject {
        id: internal

        property var dynamicColor: if(textButton.down) {
                                      textButton.down ? colorPressed : colorDefault
                                   } else {
                                      textButton.hovered ? colorMouseOver : colorDefault
                                   }
    }

    width: 60
    height: 40

    background:
    Rectangle {
        id: backgroundMenuBtn
        color: internal.dynamicColor
        radius: 5

        Label {
            id: iconBtn
            color: "#ffffff"
            text: textValue
            font.bold: true
            font.pointSize: 10
            opacity: 1
            anchors.verticalCenter: backgroundMenuBtn.verticalCenter
            anchors.horizontalCenter: backgroundMenuBtn.horizontalCenter
        }
    }
}
