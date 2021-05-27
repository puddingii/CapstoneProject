import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Styles 1.2
import QtGraphicalEffects 1.15

TextField {
    id: textField

    // Properties
    property color colorDefault: "#282c34"
    property color colorOnFocus: "#242831"
    property color colorMouseOver: "#2B2F38"

    QtObject{
        id: internal

        property var dynamicColor: if(textField.focus) {
                                        textField.focus ? colorOnFocus : colorDefault
                                   }
                                   else {
                                       textField.hovered ? colorMouseOver : colorDefault
                                   }
    }

    implicitWidth: 300
    implicitHeight: 40
    placeholderText: qsTr("Please Type Member's Information")
    color: "#ffffff"

    background: Rectangle {
        id: textBackground
        color: internal.dynamicColor
        radius: 10
    }

    selectByMouse: true
    selectedTextColor: "#FFFFFF"
    selectionColor: "#ff007f"
    placeholderTextColor: "#81848c"
    font.pointSize: 12
    font.family: "Segoe UI"
}

/*##^##
Designer {
    D{i:0;autoSize:true;height:40;width:640}
}
##^##*/
