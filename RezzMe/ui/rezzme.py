# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rezzme.ui'
#
# Created: Wed Sep 17 16:26:59 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_RezzMe(object):
    def setupUi(self, RezzMe):
        RezzMe.setObjectName("RezzMe")
        RezzMe.resize(QtCore.QSize(QtCore.QRect(0,0,588,448).size()).expandedTo(RezzMe.minimumSizeHint()))

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(RezzMe.sizePolicy().hasHeightForWidth())
        RezzMe.setSizePolicy(sizePolicy)

        font = QtGui.QFont()
        font.setFamily("Bitstream Vera Sans")
        RezzMe.setFont(font)

        self.vboxlayout = QtGui.QVBoxLayout(RezzMe)
        self.vboxlayout.setObjectName("vboxlayout")

        self.label = QtGui.QLabel(RezzMe)
        self.label.setWordWrap(True)
        self.label.setIndent(5)
        self.label.setObjectName("label")
        self.vboxlayout.addWidget(self.label)

        self.line = QtGui.QFrame(RezzMe)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.vboxlayout.addWidget(self.line)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")

        self.label_8 = QtGui.QLabel(RezzMe)
        self.label_8.setIndent(5)
        self.label_8.setObjectName("label_8")
        self.hboxlayout.addWidget(self.label_8)

        self.labelStatus = QtGui.QLabel(RezzMe)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelStatus.sizePolicy().hasHeightForWidth())
        self.labelStatus.setSizePolicy(sizePolicy)
        self.labelStatus.setObjectName("labelStatus")
        self.hboxlayout.addWidget(self.labelStatus)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.line_2 = QtGui.QFrame(RezzMe)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.vboxlayout.addWidget(self.line_2)

        self.label_10 = QtGui.QLabel(RezzMe)
        self.label_10.setIndent(5)
        self.label_10.setObjectName("label_10")
        self.vboxlayout.addWidget(self.label_10)

        self.gridlayout = QtGui.QGridLayout()
        self.gridlayout.setObjectName("gridlayout")

        self.label_2 = QtGui.QLabel(RezzMe)
        self.label_2.setIndent(5)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,0,0,1,1)

        self.labelUri = QtGui.QLabel(RezzMe)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelUri.sizePolicy().hasHeightForWidth())
        self.labelUri.setSizePolicy(sizePolicy)
        self.labelUri.setObjectName("labelUri")
        self.gridlayout.addWidget(self.labelUri,0,1,1,1)

        self.label_4 = QtGui.QLabel(RezzMe)
        self.label_4.setIndent(5)
        self.label_4.setObjectName("label_4")
        self.gridlayout.addWidget(self.label_4,1,0,1,1)

        self.labelGridName = QtGui.QLabel(RezzMe)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelGridName.sizePolicy().hasHeightForWidth())
        self.labelGridName.setSizePolicy(sizePolicy)
        self.labelGridName.setObjectName("labelGridName")
        self.gridlayout.addWidget(self.labelGridName,1,1,1,1)

        self.label_6 = QtGui.QLabel(RezzMe)
        self.label_6.setIndent(5)
        self.label_6.setObjectName("label_6")
        self.gridlayout.addWidget(self.label_6,2,0,1,1)

        self.labelRegion = QtGui.QLabel(RezzMe)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelRegion.sizePolicy().hasHeightForWidth())
        self.labelRegion.setSizePolicy(sizePolicy)
        self.labelRegion.setObjectName("labelRegion")
        self.gridlayout.addWidget(self.labelRegion,2,1,1,1)
        self.vboxlayout.addLayout(self.gridlayout)

        self.line_3 = QtGui.QFrame(RezzMe)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.vboxlayout.addWidget(self.line_3)

        self.stackedWidget = QtGui.QStackedWidget(RezzMe)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setObjectName("stackedWidget")

        self.free = QtGui.QWidget()
        self.free.setGeometry(QtCore.QRect(0,0,570,122))
        self.free.setObjectName("free")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.free)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.labelCredentialsTitle = QtGui.QLabel(self.free)
        self.labelCredentialsTitle.setIndent(5)
        self.labelCredentialsTitle.setObjectName("labelCredentialsTitle")
        self.vboxlayout1.addWidget(self.labelCredentialsTitle)

        self.gridlayout1 = QtGui.QGridLayout()
        self.gridlayout1.setObjectName("gridlayout1")

        self.labelName = QtGui.QLabel(self.free)
        self.labelName.setIndent(5)
        self.labelName.setObjectName("labelName")
        self.gridlayout1.addWidget(self.labelName,0,0,1,1)

        self.lineEditAvatarName = QtGui.QLineEdit(self.free)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditAvatarName.sizePolicy().hasHeightForWidth())
        self.lineEditAvatarName.setSizePolicy(sizePolicy)
        self.lineEditAvatarName.setMinimumSize(QtCore.QSize(200,0))
        self.lineEditAvatarName.setObjectName("lineEditAvatarName")
        self.gridlayout1.addWidget(self.lineEditAvatarName,0,1,2,1)

        self.labelPassword = QtGui.QLabel(self.free)
        self.labelPassword.setIndent(5)
        self.labelPassword.setObjectName("labelPassword")
        self.gridlayout1.addWidget(self.labelPassword,1,0,2,1)

        self.lineEditAvatarPassword = QtGui.QLineEdit(self.free)
        self.lineEditAvatarPassword.setEchoMode(QtGui.QLineEdit.Password)
        self.lineEditAvatarPassword.setObjectName("lineEditAvatarPassword")
        self.gridlayout1.addWidget(self.lineEditAvatarPassword,2,1,1,1)

        self.pushButtonOverride = QtGui.QPushButton(self.free)
        self.pushButtonOverride.setEnabled(False)
        self.pushButtonOverride.setObjectName("pushButtonOverride")
        self.gridlayout1.addWidget(self.pushButtonOverride,3,1,1,1)
        self.vboxlayout1.addLayout(self.gridlayout1)
        self.stackedWidget.addWidget(self.free)

        self.bound = QtGui.QWidget()
        self.bound.setGeometry(QtCore.QRect(0,0,570,122))
        self.bound.setObjectName("bound")

        self.vboxlayout2 = QtGui.QVBoxLayout(self.bound)
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.labelAuthenticationName = QtGui.QLabel(self.bound)
        self.labelAuthenticationName.setObjectName("labelAuthenticationName")
        self.vboxlayout2.addWidget(self.labelAuthenticationName)

        self.gridlayout2 = QtGui.QGridLayout()
        self.gridlayout2.setObjectName("gridlayout2")

        self.labelUserID = QtGui.QLabel(self.bound)
        self.labelUserID.setObjectName("labelUserID")
        self.gridlayout2.addWidget(self.labelUserID,0,0,1,1)

        self.lineEditUserID = QtGui.QLineEdit(self.bound)
        self.lineEditUserID.setObjectName("lineEditUserID")
        self.gridlayout2.addWidget(self.lineEditUserID,0,1,1,1)

        self.label_5 = QtGui.QLabel(self.bound)
        self.label_5.setObjectName("label_5")
        self.gridlayout2.addWidget(self.label_5,1,0,1,1)

        self.lineEditUserPassword = QtGui.QLineEdit(self.bound)
        self.lineEditUserPassword.setEchoMode(QtGui.QLineEdit.Password)
        self.lineEditUserPassword.setObjectName("lineEditUserPassword")
        self.gridlayout2.addWidget(self.lineEditUserPassword,1,1,1,1)

        self.pushButtonOverrideProvided = QtGui.QPushButton(self.bound)
        self.pushButtonOverrideProvided.setObjectName("pushButtonOverrideProvided")
        self.gridlayout2.addWidget(self.pushButtonOverrideProvided,2,1,1,1)
        self.vboxlayout2.addLayout(self.gridlayout2)
        self.stackedWidget.addWidget(self.bound)
        self.vboxlayout.addWidget(self.stackedWidget)

        self.line_5 = QtGui.QFrame(RezzMe)
        self.line_5.setFrameShape(QtGui.QFrame.HLine)
        self.line_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.vboxlayout.addWidget(self.line_5)

        self.checkBoxBookmark = QtGui.QCheckBox(RezzMe)
        self.checkBoxBookmark.setObjectName("checkBoxBookmark")
        self.vboxlayout.addWidget(self.checkBoxBookmark)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.pushButtonOK = QtGui.QPushButton(RezzMe)
        self.pushButtonOK.setDefault(True)
        self.pushButtonOK.setObjectName("pushButtonOK")
        self.hboxlayout1.addWidget(self.pushButtonOK)

        self.pushButtonCancel = QtGui.QPushButton(RezzMe)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.hboxlayout1.addWidget(self.pushButtonCancel)
        self.vboxlayout.addLayout(self.hboxlayout1)

        self.labelVersion = QtGui.QLabel(RezzMe)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.labelVersion.setFont(font)
        self.labelVersion.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelVersion.setObjectName("labelVersion")
        self.vboxlayout.addWidget(self.labelVersion)

        spacerItem = QtGui.QSpacerItem(20,0,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem)
        self.labelName.setBuddy(self.lineEditAvatarName)
        self.labelPassword.setBuddy(self.lineEditAvatarPassword)
        self.labelUserID.setBuddy(self.lineEditUserID)
        self.label_5.setBuddy(self.lineEditUserPassword)

        self.retranslateUi(RezzMe)
        self.stackedWidget.setCurrentIndex(1)
        QtCore.QObject.connect(self.pushButtonCancel,QtCore.SIGNAL("clicked()"),RezzMe.reject)
        QtCore.QMetaObject.connectSlotsByName(RezzMe)
        RezzMe.setTabOrder(self.lineEditAvatarName,self.lineEditAvatarPassword)
        RezzMe.setTabOrder(self.lineEditAvatarPassword,self.pushButtonOverride)
        RezzMe.setTabOrder(self.pushButtonOverride,self.lineEditUserID)
        RezzMe.setTabOrder(self.lineEditUserID,self.lineEditUserPassword)
        RezzMe.setTabOrder(self.lineEditUserPassword,self.pushButtonOverrideProvided)
        RezzMe.setTabOrder(self.pushButtonOverrideProvided,self.checkBoxBookmark)
        RezzMe.setTabOrder(self.checkBoxBookmark,self.pushButtonOK)
        RezzMe.setTabOrder(self.pushButtonOK,self.pushButtonCancel)

    def retranslateUi(self, RezzMe):
        RezzMe.setWindowTitle(QtGui.QApplication.translate("RezzMe", "rezzme:// launcher", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("RezzMe", "You seem to have clicked or selected a rezzme:// URI — please enter your credentials below:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("RezzMe", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Bitstream Vera Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Status:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelStatus.setText(QtGui.QApplication.translate("RezzMe", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("RezzMe", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'DejaVu Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Virtual world details</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("RezzMe", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Bitstream Vera Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">URI:</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelUri.setToolTip(QtGui.QApplication.translate("RezzMe", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Bitstream Vera Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">the rezzme:// of the virtual world</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelUri.setText(QtGui.QApplication.translate("RezzMe", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("RezzMe", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Bitstream Vera Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Grid name:</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelGridName.setToolTip(QtGui.QApplication.translate("RezzMe", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Bitstream Vera Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">the grid name of the virtual world</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelGridName.setText(QtGui.QApplication.translate("RezzMe", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("RezzMe", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Bitstream Vera Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Region:</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelRegion.setToolTip(QtGui.QApplication.translate("RezzMe", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Bitstream Vera Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">region in the virtual world (optional)</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelRegion.setText(QtGui.QApplication.translate("RezzMe", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.labelCredentialsTitle.setText(QtGui.QApplication.translate("RezzMe", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'DejaVu Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Avatar name &amp; password</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelName.setText(QtGui.QApplication.translate("RezzMe", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Bitstream Vera Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Avatar &amp;name:</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditAvatarName.setToolTip(QtGui.QApplication.translate("RezzMe", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Bitstream Vera Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">%(name-tooltip)s</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelPassword.setText(QtGui.QApplication.translate("RezzMe", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Bitstream Vera Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">&amp;Password:</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditAvatarPassword.setToolTip(QtGui.QApplication.translate("RezzMe", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Bitstream Vera Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">%(password-tooltip)s</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonOverride.setToolTip(QtGui.QApplication.translate("RezzMe", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Bitstream Vera Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">%(override-tooltip)s</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonOverride.setText(QtGui.QApplication.translate("RezzMe", "use &grid supplied avatar", None, QtGui.QApplication.UnicodeUTF8))
        self.labelAuthenticationName.setText(QtGui.QApplication.translate("RezzMe", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Bitstream Vera Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Gravitchco Grid Authentication:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelUserID.setText(QtGui.QApplication.translate("RezzMe", "&User ID:", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditUserID.setToolTip(QtGui.QApplication.translate("RezzMe", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Bitstream Vera Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">%(userid-tooltip)s</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("RezzMe", "&Password:", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditUserPassword.setToolTip(QtGui.QApplication.translate("RezzMe", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Bitstream Vera Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">%(userpassword-tooltip)s</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonOverrideProvided.setToolTip(QtGui.QApplication.translate("RezzMe", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Bitstream Vera Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">click here to override the grid assigned avatar</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonOverrideProvided.setText(QtGui.QApplication.translate("RezzMe", "use a &different avatar name", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxBookmark.setToolTip(QtGui.QApplication.translate("RezzMe", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Bitstream Vera Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">if you want to bookmark this place, click here before going in-world</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxBookmark.setText(QtGui.QApplication.translate("RezzMe", "&Bookmark this place", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonOK.setToolTip(QtGui.QApplication.translate("RezzMe", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Bitstream Vera Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">click here to start the virtual world client (e.g., the secondlife(tm) client)</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonOK.setText(QtGui.QApplication.translate("RezzMe", "go &in-world", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonCancel.setToolTip(QtGui.QApplication.translate("RezzMe", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Bitstream Vera Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">click here to cancel</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonCancel.setText(QtGui.QApplication.translate("RezzMe", "&cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.labelVersion.setText(QtGui.QApplication.translate("RezzMe", "vX.Y", None, QtGui.QApplication.UnicodeUTF8))

