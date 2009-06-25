# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'edit.ui'
#
# Created: Thu Jun 25 18:52:41 2009
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_RezzMeTrayEdit(object):
    def setupUi(self, RezzMeTrayEdit):
        RezzMeTrayEdit.setObjectName("RezzMeTrayEdit")
        RezzMeTrayEdit.resize(QtCore.QSize(QtCore.QRect(0,0,591,326).size()).expandedTo(RezzMeTrayEdit.minimumSizeHint()))

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(RezzMeTrayEdit.sizePolicy().hasHeightForWidth())
        RezzMeTrayEdit.setSizePolicy(sizePolicy)

        self.vboxlayout = QtGui.QVBoxLayout(RezzMeTrayEdit)
        self.vboxlayout.setObjectName("vboxlayout")

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")

        self.checkBoxEditBookmark = QtGui.QCheckBox(RezzMeTrayEdit)

        font = QtGui.QFont()
        font.setFamily("Bitstream Vera Sans")
        self.checkBoxEditBookmark.setFont(font)
        self.checkBoxEditBookmark.setObjectName("checkBoxEditBookmark")
        self.hboxlayout.addWidget(self.checkBoxEditBookmark)

        self.comboBoxBookmarks = QtGui.QComboBox(RezzMeTrayEdit)
        self.comboBoxBookmarks.setEnabled(False)

        font = QtGui.QFont()
        font.setFamily("Bitstream Vera Sans")
        self.comboBoxBookmarks.setFont(font)
        self.comboBoxBookmarks.setObjectName("comboBoxBookmarks")
        self.hboxlayout.addWidget(self.comboBoxBookmarks)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.line = QtGui.QFrame(RezzMeTrayEdit)

        font = QtGui.QFont()
        font.setFamily("Bitstream Vera Sans")
        self.line.setFont(font)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.vboxlayout.addWidget(self.line)

        self.gridlayout = QtGui.QGridLayout()
        self.gridlayout.setObjectName("gridlayout")

        self.label = QtGui.QLabel(RezzMeTrayEdit)

        font = QtGui.QFont()
        font.setFamily("Bitstream Vera Sans")
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,0,0,1,1)

        self.lineEditGridHost = QtGui.QLineEdit(RezzMeTrayEdit)

        font = QtGui.QFont()
        font.setFamily("Bitstream Vera Sans")
        self.lineEditGridHost.setFont(font)
        self.lineEditGridHost.setObjectName("lineEditGridHost")
        self.gridlayout.addWidget(self.lineEditGridHost,0,1,1,3)

        self.label_2 = QtGui.QLabel(RezzMeTrayEdit)

        font = QtGui.QFont()
        font.setFamily("Bitstream Vera Sans")
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,1,0,1,1)

        self.label_3 = QtGui.QLabel(RezzMeTrayEdit)

        font = QtGui.QFont()
        font.setFamily("Bitstream Vera Sans")
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridlayout.addWidget(self.label_3,3,0,1,1)

        self.lineEditX = QtGui.QLineEdit(RezzMeTrayEdit)
        self.lineEditX.setEnabled(True)

        font = QtGui.QFont()
        font.setFamily("Bitstream Vera Sans")
        self.lineEditX.setFont(font)
        self.lineEditX.setObjectName("lineEditX")
        self.gridlayout.addWidget(self.lineEditX,3,1,1,1)

        self.lineEditY = QtGui.QLineEdit(RezzMeTrayEdit)
        self.lineEditY.setEnabled(True)

        font = QtGui.QFont()
        font.setFamily("Bitstream Vera Sans")
        self.lineEditY.setFont(font)
        self.lineEditY.setObjectName("lineEditY")
        self.gridlayout.addWidget(self.lineEditY,3,2,1,1)

        self.lineEditZ = QtGui.QLineEdit(RezzMeTrayEdit)
        self.lineEditZ.setEnabled(True)

        font = QtGui.QFont()
        font.setFamily("Bitstream Vera Sans")
        self.lineEditZ.setFont(font)
        self.lineEditZ.setObjectName("lineEditZ")
        self.gridlayout.addWidget(self.lineEditZ,3,3,1,1)

        self.label_4 = QtGui.QLabel(RezzMeTrayEdit)

        font = QtGui.QFont()
        font.setFamily("Bitstream Vera Sans")
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridlayout.addWidget(self.label_4,4,0,1,1)

        self.lineEditAvatarName = QtGui.QLineEdit(RezzMeTrayEdit)

        font = QtGui.QFont()
        font.setFamily("Bitstream Vera Sans")
        self.lineEditAvatarName.setFont(font)
        self.lineEditAvatarName.setObjectName("lineEditAvatarName")
        self.gridlayout.addWidget(self.lineEditAvatarName,4,1,1,3)

        self.label_5 = QtGui.QLabel(RezzMeTrayEdit)

        font = QtGui.QFont()
        font.setFamily("Bitstream Vera Sans")
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridlayout.addWidget(self.label_5,5,0,1,1)

        self.labelRezzMe = QtGui.QLabel(RezzMeTrayEdit)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelRezzMe.sizePolicy().hasHeightForWidth())
        self.labelRezzMe.setSizePolicy(sizePolicy)

        font = QtGui.QFont()
        font.setFamily("Bitstream Vera Sans")
        self.labelRezzMe.setFont(font)
        self.labelRezzMe.setObjectName("labelRezzMe")
        self.gridlayout.addWidget(self.labelRezzMe,5,1,1,3)

        self.lineEditRegion = QtGui.QLineEdit(RezzMeTrayEdit)

        font = QtGui.QFont()
        font.setFamily("Bitstream Vera Sans")
        self.lineEditRegion.setFont(font)
        self.lineEditRegion.setObjectName("lineEditRegion")
        self.gridlayout.addWidget(self.lineEditRegion,1,1,1,3)

        self.label_6 = QtGui.QLabel(RezzMeTrayEdit)

        font = QtGui.QFont()
        font.setFamily("Bitstream Vera Sans")
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridlayout.addWidget(self.label_6,8,0,1,1)

        self.lineEditTag = QtGui.QLineEdit(RezzMeTrayEdit)

        font = QtGui.QFont()
        font.setFamily("Bitstream Vera Sans")
        self.lineEditTag.setFont(font)
        self.lineEditTag.setObjectName("lineEditTag")
        self.gridlayout.addWidget(self.lineEditTag,8,1,1,3)

        self.line_2 = QtGui.QFrame(RezzMeTrayEdit)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridlayout.addWidget(self.line_2,7,0,1,4)
        self.vboxlayout.addLayout(self.gridlayout)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setObjectName("hboxlayout1")
        self.vboxlayout.addLayout(self.hboxlayout1)

        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setObjectName("hboxlayout2")

        self.pushButtonAdd = QtGui.QPushButton(RezzMeTrayEdit)

        font = QtGui.QFont()
        font.setFamily("Bitstream Vera Sans")
        self.pushButtonAdd.setFont(font)
        self.pushButtonAdd.setDefault(True)
        self.pushButtonAdd.setObjectName("pushButtonAdd")
        self.hboxlayout2.addWidget(self.pushButtonAdd)

        self.pushButtonChange = QtGui.QPushButton(RezzMeTrayEdit)
        self.pushButtonChange.setEnabled(False)

        font = QtGui.QFont()
        font.setFamily("Bitstream Vera Sans")
        self.pushButtonChange.setFont(font)
        self.pushButtonChange.setObjectName("pushButtonChange")
        self.hboxlayout2.addWidget(self.pushButtonChange)

        self.pushButtonDelete = QtGui.QPushButton(RezzMeTrayEdit)
        self.pushButtonDelete.setEnabled(False)

        font = QtGui.QFont()
        font.setFamily("Bitstream Vera Sans")
        self.pushButtonDelete.setFont(font)
        self.pushButtonDelete.setObjectName("pushButtonDelete")
        self.hboxlayout2.addWidget(self.pushButtonDelete)

        self.pushButtonCancel = QtGui.QPushButton(RezzMeTrayEdit)

        font = QtGui.QFont()
        font.setFamily("Bitstream Vera Sans")
        self.pushButtonCancel.setFont(font)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.hboxlayout2.addWidget(self.pushButtonCancel)
        self.vboxlayout.addLayout(self.hboxlayout2)

        self.hboxlayout3 = QtGui.QHBoxLayout()
        self.hboxlayout3.setObjectName("hboxlayout3")

        self.label_7 = QtGui.QLabel(RezzMeTrayEdit)
        self.label_7.setObjectName("label_7")
        self.hboxlayout3.addWidget(self.label_7)

        self.labelStatus = QtGui.QLabel(RezzMeTrayEdit)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelStatus.sizePolicy().hasHeightForWidth())
        self.labelStatus.setSizePolicy(sizePolicy)
        self.labelStatus.setObjectName("labelStatus")
        self.hboxlayout3.addWidget(self.labelStatus)
        self.vboxlayout.addLayout(self.hboxlayout3)

        spacerItem = QtGui.QSpacerItem(536,13,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem)
        self.label.setBuddy(self.lineEditGridHost)
        self.label_2.setBuddy(self.lineEditRegion)
        self.label_3.setBuddy(self.lineEditX)
        self.label_4.setBuddy(self.lineEditAvatarName)
        self.label_6.setBuddy(self.lineEditTag)

        self.retranslateUi(RezzMeTrayEdit)
        QtCore.QObject.connect(self.checkBoxEditBookmark,QtCore.SIGNAL("toggled(bool)"),self.comboBoxBookmarks.setEnabled)
        QtCore.QObject.connect(self.pushButtonCancel,QtCore.SIGNAL("clicked()"),RezzMeTrayEdit.close)
        QtCore.QObject.connect(self.checkBoxEditBookmark,QtCore.SIGNAL("toggled(bool)"),self.pushButtonChange.setEnabled)
        QtCore.QObject.connect(self.checkBoxEditBookmark,QtCore.SIGNAL("toggled(bool)"),self.pushButtonDelete.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(RezzMeTrayEdit)
        RezzMeTrayEdit.setTabOrder(self.checkBoxEditBookmark,self.comboBoxBookmarks)
        RezzMeTrayEdit.setTabOrder(self.comboBoxBookmarks,self.lineEditGridHost)
        RezzMeTrayEdit.setTabOrder(self.lineEditGridHost,self.lineEditRegion)
        RezzMeTrayEdit.setTabOrder(self.lineEditRegion,self.lineEditX)
        RezzMeTrayEdit.setTabOrder(self.lineEditX,self.lineEditY)
        RezzMeTrayEdit.setTabOrder(self.lineEditY,self.lineEditZ)
        RezzMeTrayEdit.setTabOrder(self.lineEditZ,self.lineEditAvatarName)
        RezzMeTrayEdit.setTabOrder(self.lineEditAvatarName,self.lineEditTag)
        RezzMeTrayEdit.setTabOrder(self.lineEditTag,self.pushButtonAdd)
        RezzMeTrayEdit.setTabOrder(self.pushButtonAdd,self.pushButtonChange)
        RezzMeTrayEdit.setTabOrder(self.pushButtonChange,self.pushButtonDelete)
        RezzMeTrayEdit.setTabOrder(self.pushButtonDelete,self.pushButtonCancel)

    def retranslateUi(self, RezzMeTrayEdit):
        RezzMeTrayEdit.setWindowTitle(QtGui.QApplication.translate("RezzMeTrayEdit", "Edit rezzme:// bookmarks", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxEditBookmark.setToolTip(QtGui.QApplication.translate("RezzMeTrayEdit", "click here to edit existing bookmarks", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxEditBookmark.setText(QtGui.QApplication.translate("RezzMeTrayEdit", "&Edit existing bookmark", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxBookmarks.setToolTip(QtGui.QApplication.translate("RezzMeTrayEdit", "select the bookmark you want to edit from this list", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxBookmarks.addItem(QtGui.QApplication.translate("RezzMeTrayEdit", "rezzme://opensim.blafoo.com:9000/", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxBookmarks.addItem(QtGui.QApplication.translate("RezzMeTrayEdit", "rezzme://agni.secondlife.com:4711/", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("RezzMeTrayEdit", "&Grid host", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditGridHost.setToolTip(QtGui.QApplication.translate("RezzMeTrayEdit", "enter the address and port number of the grid host here (e.g., opensim.supergrid.com:9000)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("RezzMeTrayEdit", "&Region/Island", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("RezzMeTrayEdit", "&X/Y/Z", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditX.setToolTip(QtGui.QApplication.translate("RezzMeTrayEdit", "optional: enter the X coordinate here", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditX.setInputMask(QtGui.QApplication.translate("RezzMeTrayEdit", "000; ", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditY.setToolTip(QtGui.QApplication.translate("RezzMeTrayEdit", "optional: enter the Y coordinate here", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditY.setInputMask(QtGui.QApplication.translate("RezzMeTrayEdit", "000; ", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditZ.setToolTip(QtGui.QApplication.translate("RezzMeTrayEdit", "optional: enter the Z coordinate here", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditZ.setInputMask(QtGui.QApplication.translate("RezzMeTrayEdit", "000; ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("RezzMeTrayEdit", "Avatar &name", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditAvatarName.setToolTip(QtGui.QApplication.translate("RezzMeTrayEdit", "optional: enter the name of the avatar you want to use here", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("RezzMeTrayEdit", "rezzme://", None, QtGui.QApplication.UnicodeUTF8))
        self.labelRezzMe.setText(QtGui.QApplication.translate("RezzMeTrayEdit", "rezzme://....", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditRegion.setToolTip(QtGui.QApplication.translate("RezzMeTrayEdit", "optional field: enter the region or island name here", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("RezzMeTrayEdit", "D&isplay", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditTag.setToolTip(QtGui.QApplication.translate("RezzMeTrayEdit", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Bitstream Vera Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">you can give this rezzme:// URI a description; for example, \"experimental collab space\".</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonAdd.setToolTip(QtGui.QApplication.translate("RezzMeTrayEdit", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'DejaVu Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">click here to add the rezzme:// URI as a <span style=\" font-weight:600;\">new bookmark</span>.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonAdd.setText(QtGui.QApplication.translate("RezzMeTrayEdit", "&Add", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonChange.setToolTip(QtGui.QApplication.translate("RezzMeTrayEdit", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'DejaVu Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">click here to accept the <span style=\" font-weight:600;\">change</span> to the <span style=\" font-weight:600;\">existing bookmark.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonChange.setText(QtGui.QApplication.translate("RezzMeTrayEdit", "Chan&ge", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonDelete.setToolTip(QtGui.QApplication.translate("RezzMeTrayEdit", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'DejaVu Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">click here to <span style=\" font-weight:600;\">delete the existing bookmark.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonDelete.setText(QtGui.QApplication.translate("RezzMeTrayEdit", "&Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonCancel.setToolTip(QtGui.QApplication.translate("RezzMeTrayEdit", "click here to leave without changing or adding anything.", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonCancel.setText(QtGui.QApplication.translate("RezzMeTrayEdit", "D&one", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("RezzMeTrayEdit", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'DejaVu Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Status:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelStatus.setText(QtGui.QApplication.translate("RezzMeTrayEdit", "StatusLabel", None, QtGui.QApplication.UnicodeUTF8))

