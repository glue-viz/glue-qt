# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'glue/qt/ui/custom_component_widget.ui'
#
# Created: Wed Jul 31 15:07:24 2013
#      by: pyside-uic 0.2.13 running on glue.external.qt 1.1.0
#
# WARNING! All changes made in this file will be lost!

from glue.external.qt import QtCore, QtGui

class Ui_CustomComponentWidget(object):
    def setupUi(self, CustomComponentWidget):
        CustomComponentWidget.setObjectName("CustomComponentWidget")
        CustomComponentWidget.resize(804, 585)
        self.horizontalLayout_4 = QtGui.QHBoxLayout(CustomComponentWidget)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtGui.QLabel(CustomComponentWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.component_list = QtGui.QListWidget(CustomComponentWidget)
        self.component_list.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        self.component_list.setObjectName("component_list")
        self.verticalLayout_2.addWidget(self.component_list)
        self.verticalLayout_2.setStretch(0, 5)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtGui.QLabel(CustomComponentWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.data_list = QtGui.QListWidget(CustomComponentWidget)
        self.data_list.setObjectName("data_list")
        self.verticalLayout.addWidget(self.data_list)
        self.verticalLayout.setStretch(0, 5)
        self.verticalLayout.setStretch(1, 1)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_3 = QtGui.QLabel(CustomComponentWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.expression = QtGui.QLineEdit(CustomComponentWidget)
        self.expression.setAlignment(QtCore.Qt.AlignCenter)
        self.expression.setObjectName("expression")
        self.verticalLayout_3.addWidget(self.expression)
        self.verticalLayout_5.addLayout(self.verticalLayout_3)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_4 = QtGui.QLabel(CustomComponentWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_4.addWidget(self.label_4)
        self.new_label = QtGui.QLineEdit(CustomComponentWidget)
        self.new_label.setObjectName("new_label")
        self.verticalLayout_4.addWidget(self.new_label)
        self.verticalLayout_4.setStretch(0, 5)
        self.verticalLayout_4.setStretch(1, 1)
        self.horizontalLayout_2.addLayout(self.verticalLayout_4)
        self.buttonBox = QtGui.QDialogButtonBox(CustomComponentWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout_2.addWidget(self.buttonBox)
        self.horizontalLayout_2.setStretch(0, 10)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        self.verticalLayout_5.setStretch(0, 5)
        self.verticalLayout_5.setStretch(1, 1)
        self.verticalLayout_5.setStretch(2, 1)
        self.horizontalLayout_4.addLayout(self.verticalLayout_5)

        self.retranslateUi(CustomComponentWidget)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), CustomComponentWidget.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), CustomComponentWidget.reject)
        QtCore.QMetaObject.connectSlotsByName(CustomComponentWidget)

    def retranslateUi(self, CustomComponentWidget):
        CustomComponentWidget.setWindowTitle(QtGui.QApplication.translate("CustomComponentWidget", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("CustomComponentWidget", "Available Components", None, QtGui.QApplication.UnicodeUTF8))
        self.component_list.setToolTip(QtGui.QApplication.translate("CustomComponentWidget", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Lucida Grande\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Available components to reference when defining a new component</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("CustomComponentWidget", "Add to", None, QtGui.QApplication.UnicodeUTF8))
        self.data_list.setToolTip(QtGui.QApplication.translate("CustomComponentWidget", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Lucida Grande\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Select one or more data sets to add the new component to</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("CustomComponentWidget", "Expression", None, QtGui.QApplication.UnicodeUTF8))
        self.expression.setToolTip(QtGui.QApplication.translate("CustomComponentWidget", "Define a new component. E.g. {component_a} - {component_b}", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("CustomComponentWidget", "Label for New Component", None, QtGui.QApplication.UnicodeUTF8))

