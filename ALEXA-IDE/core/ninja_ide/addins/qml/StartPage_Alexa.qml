//Last Modified: 2013-09-02 by Alan Pipitone
import QtQuick 1.1

Rectangle {
    id: root

    property int _padding: (mainArea.width / 4)
    property bool compressed: true

    signal markAsFavorite(string pat, bool value)
    signal openProject(string path)
    signal removeProject(string path)
    signal openPreferences

    gradient: Gradient {
         GradientStop { position: 0.0; color: "#1e1e1e" }
         GradientStop { position: 1.0; color: "#a4a4a4" }
     }

    onWidthChanged: {
        if(root.width < 800){
            compressed = true;
            root._padding = (mainArea.width / 2);
            logo.width = 300;
            logo.source = "img/alexa-ide-small.png"
            txtProjects.visible = false;
            projectList.visible = false;
        }else{
            compressed = false;
            root._padding = (mainArea.width / 4);
            logo.source = "img/alexa-ide.png"
            logo.width = logo.sourceSize.width;
            txtProjects.visible = true;
            projectList.visible = true;
        }
    }

    Rectangle {
        id: mainArea
        color: "white"
        anchors.fill: parent
        radius: 10
        anchors.margins: parent.height / 14
        smooth: true
        Image {
            id: logo
            source: "img/alexa-ide.png"
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.leftMargin: root.compressed ? 10 : root.get_padding(logo);
            anchors.topMargin: 10
            fillMode: Image.PreserveAspectFit
        }

        Text {
            id: txtWelcome
            anchors.left: parent.left
            anchors.top: logo.bottom
            anchors.leftMargin: root.compressed ? 10 : root.get_padding(txtWelcome);
            anchors.topMargin: 15
            color: "#2f2d2d"
            text: "Welcome!"
            font.bold: true
            font.pointSize: 45
            style: Text.Raised
            styleColor: "black"
        }

        Text {
            id: txtDescription
            width: compressed ? parent.width - 20 : root._padding * 1.5
            anchors.left: parent.left
            anchors.top: txtWelcome.bottom
            anchors.leftMargin: root.compressed ? 10 : root.get_padding(txtDescription);
            anchors.topMargin: 10
            // text: "NINJA-IDE (from: \"Ninja-IDE Is Not Just Another IDE\"), is a cross-platform integrated development environment specially designed to build Python Applications. NINJA-IDE provides tools to simplify the Python-software development and handles all kinds of situations thanks to its rich extensibility.";
            text: "AL'EXA-IDE is an integrated development environment (based on NINJA-IDE) specially design to build Al'exa's Test Cases. Al'exa is a Python module that provides capabilities to automate and test user interfaces by using computer vision. Al’exa is already nsclient++ compliant so that Nagios, Icinga, Shinken can schedule them and get the performance data back. Al'exa is developed and maintained by Alan Pipitone."
            wrapMode: Text.WordWrap
        }

        Column {
            id: colButtons
            anchors.top: txtDescription.bottom
            anchors.left: parent.left
            anchors.leftMargin: root.compressed ? 10 : root.get_padding(colButtons);
            anchors.topMargin: root.compressed ? 25 : 50

            property int buttonWidth: compressed ? (mainArea.width / 2) - 20 : (mainArea.width / 4) - 50
            Row {
                spacing: 10
                Button {
                    width: colButtons.buttonWidth
                    height: 35
                    text: "Al'exa WebSite"
                    onClicked: Qt.openUrlExternally("http://www.alexa-monitoring.com")
                }
                Button {
                    width: colButtons.buttonWidth
                    height: 35
                    text: "Preferences"
                    onClicked: openPreferences();
                }
            }
        }

        Text {
            id: txtProjects
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.rightMargin: root.get_padding(txtProjects);
            anchors.topMargin: 30
            color: "#2f2d2d"
            text: "Recent Projects:"
            font.bold: true
            font.pointSize: 30
            style: Text.Raised
            styleColor: "black"
        }

        ProjectList {
            id: projectList
            width: (parent.width / 2) - 20
            height: parent.height - txtProjects.height - 70
            anchors.right: parent.right
            anchors.top: txtProjects.bottom
            anchors.rightMargin: root.get_padding(projectList)
            anchors.topMargin: 10

            onMarkAsFavorite: root.markAsFavorite(path, value);
            onOpenProject: root.openProject(path);
            onRemoveProject: root.removeProject(path);
        }
    }

    Row {
        spacing: 10
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.topMargin: 5
        anchors.rightMargin: parent.height / 14

        Text {
            text: "Powered by:"
            color: "white"
            style: Text.Raised
            styleColor: "black"
            height: logoNinja.height
            verticalAlignment: Text.AlignVCenter
        }
        Image {
            id: logoNinja
            source: "img/powered_ninja.png"
        }
    }

    Text {
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.leftMargin: parent.height / 14
        anchors.bottomMargin: 5
        color: "black"
        text: "Copyright © 2013 AL'EXA-IDE under GPLv3 License agreements"
    }

    function get_padding(item){
        var newPadding = (root._padding - (item.width / 2)) - 10;
        return newPadding;
    }

    function add_project(name, path, favorite){
        projectList.add_project(name, path, favorite);
    }

}
