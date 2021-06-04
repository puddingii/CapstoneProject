import QtQuick 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.15

Button {
    id: imageButton

    property url imagePath: "../../images/svg/webcam.svg"
    property int imageWidth: 40
    property int imageHeight: 40
    property color colorDefault: "#070b1b"
    property color colorMouseOver: "#181c2c"
    property color colorPressed: "#04050d"
    property bool isVisible: false

    QtObject {
        id: internal

        property var dynamicColor: if(imageButton.down) {
                                      imageButton.down ? colorPressed : colorDefault
                                   } else {
                                      imageButton.hovered ? colorMouseOver : colorDefault
                                   }
    }

    width: 200
    height: 70

    background:
    Rectangle {
        id: backgroundMenuBtn
        color: internal.dynamicColor


        Image {
            id: iconBtn
            width: imageWidth
            height: imageHeight
            opacity: 1
            source: imagePath
            sourceSize.width: imageWidth
            sourceSize.height: imageHeight
            fillMode: Image.PreserveAspectFit
            anchors.verticalCenter: backgroundMenuBtn.verticalCenter
            anchors.horizontalCenter: backgroundMenuBtn.horizontalCenter
        }

        Rectangle {
            width: 10
            height: 70
            color: "#ffffff"
            visible: isVisible
            anchors.left: backgroundMenuBtn.left
            anchors.verticalCenter: backgroundMenuBtn.verticalCenter
        }
    }
}
