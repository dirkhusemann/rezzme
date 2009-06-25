# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about.ui'
#
# Created: Thu Jun 25 18:52:41 2009
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_About(object):
    def setupUi(self, About):
        About.setObjectName("About")
        About.resize(QtCore.QSize(QtCore.QRect(0,0,572,504).size()).expandedTo(About.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(About)
        self.vboxlayout.setObjectName("vboxlayout")

        self.textBrowser = QtGui.QTextBrowser(About)

        font = QtGui.QFont()
        font.setFamily("Bitstream Vera Sans")
        self.textBrowser.setFont(font)
        self.textBrowser.setFrameShape(QtGui.QFrame.StyledPanel)
        self.textBrowser.setFrameShadow(QtGui.QFrame.Sunken)
        self.textBrowser.setObjectName("textBrowser")
        self.vboxlayout.addWidget(self.textBrowser)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")

        self.pushButton = QtGui.QPushButton(About)
        self.pushButton.setObjectName("pushButton")
        self.hboxlayout.addWidget(self.pushButton)

        self.pushButtonChangeLog = QtGui.QPushButton(About)
        self.pushButtonChangeLog.setObjectName("pushButtonChangeLog")
        self.hboxlayout.addWidget(self.pushButtonChangeLog)

        self.pushButtonEmail = QtGui.QPushButton(About)
        self.pushButtonEmail.setObjectName("pushButtonEmail")
        self.hboxlayout.addWidget(self.pushButtonEmail)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.retranslateUi(About)
        QtCore.QObject.connect(self.pushButton,QtCore.SIGNAL("clicked()"),About.accept)
        QtCore.QObject.connect(self.pushButtonEmail,QtCore.SIGNAL("clicked()"),About.accept)
        QtCore.QMetaObject.connectSlotsByName(About)

    def retranslateUi(self, About):
        About.setWindowTitle(QtGui.QApplication.translate("About", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.textBrowser.setHtml(QtGui.QApplication.translate("About", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Bitstream Vera Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">About text</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("About", "ok", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonChangeLog.setText(QtGui.QApplication.translate("About", "view change log", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonEmail.setText(QtGui.QApplication.translate("About", "send diagnostics", None, QtGui.QApplication.UnicodeUTF8))

