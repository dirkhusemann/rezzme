# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'clientselector.ui'
#
# Created: Mon Nov  3 11:05:18 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ClientSelector(object):
    def setupUi(self, ClientSelector):
        ClientSelector.setObjectName("ClientSelector")
        ClientSelector.resize(QtCore.QSize(QtCore.QRect(0,0,400,153).size()).expandedTo(ClientSelector.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(ClientSelector)
        self.vboxlayout.setObjectName("vboxlayout")

        self.labelMessage = QtGui.QLabel(ClientSelector)

        font = QtGui.QFont()
        font.setFamily("Bitstream Vera Sans")
        self.labelMessage.setFont(font)
        self.labelMessage.setObjectName("labelMessage")
        self.vboxlayout.addWidget(self.labelMessage)

        self.gridlayout = QtGui.QGridLayout()
        self.gridlayout.setObjectName("gridlayout")

        self.label_2 = QtGui.QLabel(ClientSelector)

        font = QtGui.QFont()
        font.setFamily("Bitstream Vera Sans")
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,0,0,1,1)

        self.labelClientPath = QtGui.QLabel(ClientSelector)

        font = QtGui.QFont()
        font.setFamily("Bitstream Vera Sans")
        self.labelClientPath.setFont(font)
        self.labelClientPath.setObjectName("labelClientPath")
        self.gridlayout.addWidget(self.labelClientPath,0,1,1,1)

        self.pushButtonSelectClient = QtGui.QPushButton(ClientSelector)

        font = QtGui.QFont()
        font.setFamily("Bitstream Vera Sans")
        self.pushButtonSelectClient.setFont(font)
        self.pushButtonSelectClient.setObjectName("pushButtonSelectClient")
        self.gridlayout.addWidget(self.pushButtonSelectClient,0,2,1,1)

        self.lineEditClientTag = QtGui.QLineEdit(ClientSelector)

        font = QtGui.QFont()
        font.setFamily("Bitstream Vera Sans")
        self.lineEditClientTag.setFont(font)
        self.lineEditClientTag.setObjectName("lineEditClientTag")
        self.gridlayout.addWidget(self.lineEditClientTag,1,1,1,2)

        self.label_4 = QtGui.QLabel(ClientSelector)

        font = QtGui.QFont()
        font.setFamily("Bitstream Vera Sans")
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridlayout.addWidget(self.label_4,1,0,1,1)
        self.vboxlayout.addLayout(self.gridlayout)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")

        self.pushButtonOK = QtGui.QPushButton(ClientSelector)

        font = QtGui.QFont()
        font.setFamily("Bitstream Vera Sans")
        self.pushButtonOK.setFont(font)
        self.pushButtonOK.setObjectName("pushButtonOK")
        self.hboxlayout.addWidget(self.pushButtonOK)

        self.pushButtonCancel = QtGui.QPushButton(ClientSelector)

        font = QtGui.QFont()
        font.setFamily("Bitstream Vera Sans")
        self.pushButtonCancel.setFont(font)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.hboxlayout.addWidget(self.pushButtonCancel)
        self.vboxlayout.addLayout(self.hboxlayout)

        spacerItem = QtGui.QSpacerItem(20,0,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem)
        self.label_4.setBuddy(self.lineEditClientTag)

        self.retranslateUi(ClientSelector)
        QtCore.QObject.connect(self.pushButtonCancel,QtCore.SIGNAL("clicked()"),ClientSelector.reject)
        QtCore.QMetaObject.connectSlotsByName(ClientSelector)

    def retranslateUi(self, ClientSelector):
        ClientSelector.setWindowTitle(QtGui.QApplication.translate("ClientSelector", "Virtual world client selector", None, QtGui.QApplication.UnicodeUTF8))
        self.labelMessage.setText(QtGui.QApplication.translate("ClientSelector", "Select a new client and give it a short tag:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("ClientSelector", "client:", None, QtGui.QApplication.UnicodeUTF8))
        self.labelClientPath.setText(QtGui.QApplication.translate("ClientSelector", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonSelectClient.setToolTip(QtGui.QApplication.translate("ClientSelector", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Bitstream Vera Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">click here to select a new virtual world client using a file selector</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonSelectClient.setText(QtGui.QApplication.translate("ClientSelector", "&select client", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditClientTag.setToolTip(QtGui.QApplication.translate("ClientSelector", "enter a short, but descriptive tag here; e.g., \"secondlife 2.10.99\".", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("ClientSelector", "&tag:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonOK.setToolTip(QtGui.QApplication.translate("ClientSelector", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Bitstream Vera Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">click here when you are done</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonOK.setText(QtGui.QApplication.translate("ClientSelector", "&done", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonCancel.setToolTip(QtGui.QApplication.translate("ClientSelector", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Bitstream Vera Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">click here when you want to cancel this dialog</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonCancel.setText(QtGui.QApplication.translate("ClientSelector", "&cancel", None, QtGui.QApplication.UnicodeUTF8))

