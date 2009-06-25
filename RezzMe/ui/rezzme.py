# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rezzme.ui'
#
# Created: Thu Jun 25 17:14:31 2009
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_RezzMe(object):
    def setupUi(self, RezzMe):
        RezzMe.setObjectName("RezzMe")
        RezzMe.resize(524, 342)
        self.verticalLayout_3 = QtGui.QVBoxLayout(RezzMe)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tabWidget = QtGui.QTabWidget(RezzMe)
        font = QtGui.QFont()
        font.setFamily("Bitstream Vera Sans")
        self.tabWidget.setFont(font)
        self.tabWidget.setElideMode(QtCore.Qt.ElideLeft)
        self.tabWidget.setUsesScrollButtons(True)
        self.tabWidget.setObjectName("tabWidget")
        self.tabSimple = QtGui.QWidget()
        self.tabSimple.setGeometry(QtCore.QRect(0, 0, 502, 267))
        self.tabSimple.setObjectName("tabSimple")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tabSimple)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_7 = QtGui.QLabel(self.tabSimple)
        font = QtGui.QFont()
        font.setFamily("Bitstream Vera Sans")
        self.label_7.setFont(font)
        self.label_7.setWordWrap(True)
        self.label_7.setIndent(5)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_2.addWidget(self.label_7)
        self.labelAuthenticationName = QtGui.QLabel(self.tabSimple)
        font = QtGui.QFont()
        font.setFamily("Bitstream Vera Sans")
        font.setWeight(75)
        font.setBold(True)
        self.labelAuthenticationName.setFont(font)
        self.labelAuthenticationName.setObjectName("labelAuthenticationName")
        self.verticalLayout_2.addWidget(self.labelAuthenticationName)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.labelUser = QtGui.QLabel(self.tabSimple)
        font = QtGui.QFont()
        font.setFamily("Bitstream Vera Sans")
        self.labelUser.setFont(font)
        self.labelUser.setObjectName("labelUser")
        self.gridLayout.addWidget(self.labelUser, 0, 0, 1, 1)
        self.lineEditUser = QtGui.QLineEdit(self.tabSimple)
        font = QtGui.QFont()
        font.setFamily("Bitstream Vera Sans")
        self.lineEditUser.setFont(font)
        self.lineEditUser.setObjectName("lineEditUser")
        self.gridLayout.addWidget(self.lineEditUser, 0, 1, 1, 1)
        self.labelPassword = QtGui.QLabel(self.tabSimple)
        font = QtGui.QFont()
        font.setFamily("Bitstream Vera Sans")
        self.labelPassword.setFont(font)
        self.labelPassword.setObjectName("labelPassword")
        self.gridLayout.addWidget(self.labelPassword, 1, 0, 1, 1)
        self.lineEditPassword = QtGui.QLineEdit(self.tabSimple)
        font = QtGui.QFont()
        font.setFamily("Bitstream Vera Sans")
        self.lineEditPassword.setFont(font)
        self.lineEditPassword.setEchoMode(QtGui.QLineEdit.Password)
        self.lineEditPassword.setObjectName("lineEditPassword")
        self.gridLayout.addWidget(self.lineEditPassword, 1, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButtonOK = QtGui.QPushButton(self.tabSimple)
        font = QtGui.QFont()
        font.setFamily("Bitstream Vera Sans")
        self.pushButtonOK.setFont(font)
        self.pushButtonOK.setDefault(True)
        self.pushButtonOK.setObjectName("pushButtonOK")
        self.horizontalLayout_2.addWidget(self.pushButtonOK)
        self.pushButtonCancel = QtGui.QPushButton(self.tabSimple)
        font = QtGui.QFont()
        font.setFamily("Bitstream Vera Sans")
        self.pushButtonCancel.setFont(font)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayout_2.addWidget(self.pushButtonCancel)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_8 = QtGui.QLabel(self.tabSimple)
        font = QtGui.QFont()
        font.setFamily("Bitstream Vera Sans")
        self.label_8.setFont(font)
        self.label_8.setIndent(5)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout.addWidget(self.label_8)
        self.labelStatus = QtGui.QLabel(self.tabSimple)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelStatus.sizePolicy().hasHeightForWidth())
        self.labelStatus.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Bitstream Vera Sans")
        self.labelStatus.setFont(font)
        self.labelStatus.setObjectName("labelStatus")
        self.horizontalLayout.addWidget(self.labelStatus)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        spacerItem = QtGui.QSpacerItem(20, 57, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.tabWidget.addTab(self.tabSimple, "")
        self.tabExpert = QtGui.QWidget()
        self.tabExpert.setGeometry(QtCore.QRect(0, 0, 502, 267))
        self.tabExpert.setObjectName("tabExpert")
        self.verticalLayout = QtGui.QVBoxLayout(self.tabExpert)
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelUri = QtGui.QLabel(self.tabExpert)
        self.labelUri.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.labelUri.setObjectName("labelUri")
        self.verticalLayout.addWidget(self.labelUri)
        self.labelAuthenticationName2 = QtGui.QLabel(self.tabExpert)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.labelAuthenticationName2.setFont(font)
        self.labelAuthenticationName2.setObjectName("labelAuthenticationName2")
        self.verticalLayout.addWidget(self.labelAuthenticationName2)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.labelPassword2 = QtGui.QLabel(self.tabExpert)
        self.labelPassword2.setObjectName("labelPassword2")
        self.gridLayout_2.addWidget(self.labelPassword2, 1, 0, 1, 1)
        self.lineEditPassword2 = QtGui.QLineEdit(self.tabExpert)
        self.lineEditPassword2.setEchoMode(QtGui.QLineEdit.Password)
        self.lineEditPassword2.setObjectName("lineEditPassword2")
        self.gridLayout_2.addWidget(self.lineEditPassword2, 1, 1, 1, 1)
        self.labelUser2 = QtGui.QLabel(self.tabExpert)
        self.labelUser2.setObjectName("labelUser2")
        self.gridLayout_2.addWidget(self.labelUser2, 0, 0, 1, 1)
        self.lineEditUser2 = QtGui.QLineEdit(self.tabExpert)
        self.lineEditUser2.setObjectName("lineEditUser2")
        self.gridLayout_2.addWidget(self.lineEditUser2, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.checkBoxOverride = QtGui.QCheckBox(self.tabExpert)
        self.checkBoxOverride.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.checkBoxOverride.setObjectName("checkBoxOverride")
        self.horizontalLayout_7.addWidget(self.checkBoxOverride)
        self.checkBoxOutfit = QtGui.QCheckBox(self.tabExpert)
        self.checkBoxOutfit.setObjectName("checkBoxOutfit")
        self.horizontalLayout_7.addWidget(self.checkBoxOutfit)
        self.checkBoxPurgeCache = QtGui.QCheckBox(self.tabExpert)
        self.checkBoxPurgeCache.setObjectName("checkBoxPurgeCache")
        self.horizontalLayout_7.addWidget(self.checkBoxPurgeCache)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.checkBoxBookmark = QtGui.QCheckBox(self.tabExpert)
        self.checkBoxBookmark.setObjectName("checkBoxBookmark")
        self.horizontalLayout_4.addWidget(self.checkBoxBookmark)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtGui.QLabel(self.tabExpert)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.comboBoxClients = QtGui.QComboBox(self.tabExpert)
        self.comboBoxClients.setObjectName("comboBoxClients")
        self.horizontalLayout_3.addWidget(self.comboBoxClients)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.pushButtonOK2 = QtGui.QPushButton(self.tabExpert)
        self.pushButtonOK2.setDefault(True)
        self.pushButtonOK2.setObjectName("pushButtonOK2")
        self.horizontalLayout_5.addWidget(self.pushButtonOK2)
        self.pushButtonCancel2 = QtGui.QPushButton(self.tabExpert)
        self.pushButtonCancel2.setObjectName("pushButtonCancel2")
        self.horizontalLayout_5.addWidget(self.pushButtonCancel2)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_9 = QtGui.QLabel(self.tabExpert)
        self.label_9.setIndent(5)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_6.addWidget(self.label_9)
        self.labelStatus2 = QtGui.QLabel(self.tabExpert)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelStatus2.sizePolicy().hasHeightForWidth())
        self.labelStatus2.setSizePolicy(sizePolicy)
        self.labelStatus2.setObjectName("labelStatus2")
        self.horizontalLayout_6.addWidget(self.labelStatus2)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.tabWidget.addTab(self.tabExpert, "")
        self.verticalLayout_3.addWidget(self.tabWidget)
        spacerItem2 = QtGui.QSpacerItem(20, 15, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem2)
        self.labelVersion = QtGui.QLabel(RezzMe)
        font = QtGui.QFont()
        font.setFamily("Bitstream Vera Sans")
        font.setPointSize(8)
        self.labelVersion.setFont(font)
        self.labelVersion.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelVersion.setObjectName("labelVersion")
        self.verticalLayout_3.addWidget(self.labelVersion)
        self.labelUser.setBuddy(self.lineEditUser)
        self.labelPassword.setBuddy(self.lineEditPassword)
        self.labelPassword2.setBuddy(self.lineEditPassword2)
        self.labelUser2.setBuddy(self.lineEditUser2)
        self.label_3.setBuddy(self.comboBoxClients)

        self.retranslateUi(RezzMe)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QObject.connect(self.pushButtonCancel, QtCore.SIGNAL("clicked()"), RezzMe.reject)
        QtCore.QObject.connect(self.pushButtonCancel2, QtCore.SIGNAL("clicked()"), RezzMe.reject)
        QtCore.QMetaObject.connectSlotsByName(RezzMe)
        RezzMe.setTabOrder(self.tabWidget, self.lineEditUser)
        RezzMe.setTabOrder(self.lineEditUser, self.lineEditPassword)
        RezzMe.setTabOrder(self.lineEditPassword, self.pushButtonOK)
        RezzMe.setTabOrder(self.pushButtonOK, self.pushButtonCancel)
        RezzMe.setTabOrder(self.pushButtonCancel, self.lineEditUser2)
        RezzMe.setTabOrder(self.lineEditUser2, self.lineEditPassword2)
        RezzMe.setTabOrder(self.lineEditPassword2, self.checkBoxOverride)
        RezzMe.setTabOrder(self.checkBoxOverride, self.checkBoxBookmark)
        RezzMe.setTabOrder(self.checkBoxBookmark, self.comboBoxClients)
        RezzMe.setTabOrder(self.comboBoxClients, self.pushButtonOK2)
        RezzMe.setTabOrder(self.pushButtonOK2, self.pushButtonCancel2)

    def retranslateUi(self, RezzMe):
        RezzMe.setWindowTitle(QtGui.QApplication.translate("RezzMe", "RezzMe:// Launcher", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("RezzMe", "You seem to have clicked or selected a rezzme:// URI — please enter your credentials below:", None, QtGui.QApplication.UnicodeUTF8))
        self.labelAuthenticationName.setText(QtGui.QApplication.translate("RezzMe", "Grid Authentication", None, QtGui.QApplication.UnicodeUTF8))
        self.labelUser.setText(QtGui.QApplication.translate("RezzMe", "&user ID:", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditUser.setToolTip(QtGui.QApplication.translate("RezzMe", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Bitstream Vera Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">%(userid)s</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelPassword.setText(QtGui.QApplication.translate("RezzMe", "&password:", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditPassword.setToolTip(QtGui.QApplication.translate("RezzMe", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Bitstream Vera Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">%(password)s</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
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
        self.label_8.setText(QtGui.QApplication.translate("RezzMe", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Bitstream Vera Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Status:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelStatus.setText(QtGui.QApplication.translate("RezzMe", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSimple), QtGui.QApplication.translate("RezzMe", "&Go in-world", None, QtGui.QApplication.UnicodeUTF8))
        self.labelUri.setToolTip(QtGui.QApplication.translate("RezzMe", "grid name: %(gridname)s\n"
"grid tag: %(gridnick)s", None, QtGui.QApplication.UnicodeUTF8))
        self.labelUri.setText(QtGui.QApplication.translate("RezzMe", "rezzme://cool.opensim.foo.com:9000/CoolPlaza/128/17/23", None, QtGui.QApplication.UnicodeUTF8))
        self.labelAuthenticationName2.setText(QtGui.QApplication.translate("RezzMe", "Grid authentication", None, QtGui.QApplication.UnicodeUTF8))
        self.labelPassword2.setText(QtGui.QApplication.translate("RezzMe", "&password:", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditPassword2.setToolTip(QtGui.QApplication.translate("RezzMe", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Bitstream Vera Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">%(password)s</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelUser2.setText(QtGui.QApplication.translate("RezzMe", "&user ID:", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxOverride.setToolTip(QtGui.QApplication.translate("RezzMe", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Bitstream Vera Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">select this option if you want to use a different avatar name.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxOverride.setText(QtGui.QApplication.translate("RezzMe", "use a &different avatar", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxOutfit.setToolTip(QtGui.QApplication.translate("RezzMe", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Bitstream Vera Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">select this option if you want to select a new outfit for your avatar via the web interface.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxOutfit.setText(QtGui.QApplication.translate("RezzMe", "let me choose a new &outfit", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxPurgeCache.setToolTip(QtGui.QApplication.translate("RezzMe", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Bitstream Vera Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">select this option if you want to purge your client\'s cache before going in-world.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxPurgeCache.setText(QtGui.QApplication.translate("RezzMe", "pu&rge cache", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxBookmark.setToolTip(QtGui.QApplication.translate("RezzMe", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Bitstream Vera Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">if you want to bookmark this place, click here before going in-world</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxBookmark.setText(QtGui.QApplication.translate("RezzMe", "&bookmark this place", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("RezzMe", "&virtual client to use:", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxClients.setToolTip(QtGui.QApplication.translate("RezzMe", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Bitstream Vera Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">select a specific virtual world client here (or add a new one even)</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonOK2.setToolTip(QtGui.QApplication.translate("RezzMe", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Bitstream Vera Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">click here to start the virtual world client (e.g., the secondlife(tm) client)</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonOK2.setText(QtGui.QApplication.translate("RezzMe", "go &in-world", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonCancel2.setToolTip(QtGui.QApplication.translate("RezzMe", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Bitstream Vera Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">click here to cancel</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonCancel2.setText(QtGui.QApplication.translate("RezzMe", "&cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("RezzMe", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Bitstream Vera Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Status:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelStatus2.setText(QtGui.QApplication.translate("RezzMe", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabExpert), QtGui.QApplication.translate("RezzMe", "&Advanced", None, QtGui.QApplication.UnicodeUTF8))
        self.labelVersion.setToolTip(QtGui.QApplication.translate("RezzMe", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Bitstream Vera Sans\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">%(name)s %(version)s</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">author: %(author)s</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">publisher: %(publisher)s</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">license: %(license)s</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">web site: %(url)s</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelVersion.setText(QtGui.QApplication.translate("RezzMe", "vX.Y", None, QtGui.QApplication.UnicodeUTF8))

