# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'glue/qt/ui/data_connector.ui'
#
# Created: Wed Jul 31 15:07:24 2013
#      by: pyside-uic 0.2.13 running on glue.external.qt 1.1.0
#
# WARNING! All changes made in this file will be lost!

from glue.external.qt import QtCore, QtGui

class Ui_DataConnector(object):
    def setupUi(self, DataConnector):
        DataConnector.setObjectName("DataConnector")
        DataConnector.resize(856, 670)
        self.verticalLayout_7 = QtGui.QVBoxLayout(DataConnector)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.left_label = QtGui.QLabel(DataConnector)
        self.left_label.setAlignment(QtCore.Qt.AlignCenter)
        self.left_label.setObjectName("left_label")
        self.verticalLayout.addWidget(self.left_label)
        self.left_combo = QtGui.QComboBox(DataConnector)
        self.left_combo.setObjectName("left_combo")
        self.verticalLayout.addWidget(self.left_combo)
        self.left_list = QtGui.QListWidget(DataConnector)
        self.left_list.setObjectName("left_list")
        self.verticalLayout.addWidget(self.left_list)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.right_label = QtGui.QLabel(DataConnector)
        self.right_label.setAlignment(QtCore.Qt.AlignCenter)
        self.right_label.setObjectName("right_label")
        self.verticalLayout_2.addWidget(self.right_label)
        self.right_combo = QtGui.QComboBox(DataConnector)
        self.right_combo.setObjectName("right_combo")
        self.verticalLayout_2.addWidget(self.right_combo)
        self.right_list = QtGui.QListWidget(DataConnector)
        self.right_list.setObjectName("right_list")
        self.verticalLayout_2.addWidget(self.right_list)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.glue_button = QtGui.QPushButton(DataConnector)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.glue_button.sizePolicy().hasHeightForWidth())
        self.glue_button.setSizePolicy(sizePolicy)
        self.glue_button.setObjectName("glue_button")
        self.horizontalLayout_5.addWidget(self.glue_button)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem1)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6.addLayout(self.verticalLayout_4)
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.link_label = QtGui.QLabel(DataConnector)
        self.link_label.setAlignment(QtCore.Qt.AlignCenter)
        self.link_label.setObjectName("link_label")
        self.verticalLayout_3.addWidget(self.link_label)
        self.link_list = QtGui.QListWidget(DataConnector)
        self.link_list.setObjectName("link_list")
        self.verticalLayout_3.addWidget(self.link_list)
        self.verticalLayout_5.addLayout(self.verticalLayout_3)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.un_glue_button = QtGui.QPushButton(DataConnector)
        self.un_glue_button.setObjectName("un_glue_button")
        self.horizontalLayout_3.addWidget(self.un_glue_button)
        self.verticalLayout_5.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_6.addLayout(self.verticalLayout_5)
        self.verticalLayout_6.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ok = QtGui.QPushButton(DataConnector)
        self.ok.setObjectName("ok")
        self.horizontalLayout.addWidget(self.ok)
        self.cancel = QtGui.QPushButton(DataConnector)
        self.cancel.setObjectName("cancel")
        self.horizontalLayout.addWidget(self.cancel)
        self.horizontalLayout_4.addLayout(self.horizontalLayout)
        self.verticalLayout_6.addLayout(self.horizontalLayout_4)
        self.verticalLayout_7.addLayout(self.verticalLayout_6)

        self.retranslateUi(DataConnector)
        QtCore.QMetaObject.connectSlotsByName(DataConnector)

    def retranslateUi(self, DataConnector):
        DataConnector.setWindowTitle(QtGui.QApplication.translate("DataConnector", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.left_label.setText(QtGui.QApplication.translate("DataConnector", "Data Set 1", None, QtGui.QApplication.UnicodeUTF8))
        self.left_combo.setToolTip(QtGui.QApplication.translate("DataConnector", "Select data", None, QtGui.QApplication.UnicodeUTF8))
        self.left_list.setToolTip(QtGui.QApplication.translate("DataConnector", "Select an item to link", None, QtGui.QApplication.UnicodeUTF8))
        self.right_label.setText(QtGui.QApplication.translate("DataConnector", "Data Set 2", None, QtGui.QApplication.UnicodeUTF8))
        self.right_combo.setToolTip(QtGui.QApplication.translate("DataConnector", "Select data", None, QtGui.QApplication.UnicodeUTF8))
        self.right_list.setToolTip(QtGui.QApplication.translate("DataConnector", "Select an item to link", None, QtGui.QApplication.UnicodeUTF8))
        self.glue_button.setToolTip(QtGui.QApplication.translate("DataConnector", "Establish a connection between these two attributes", None, QtGui.QApplication.UnicodeUTF8))
        self.glue_button.setText(QtGui.QApplication.translate("DataConnector", "Glue", None, QtGui.QApplication.UnicodeUTF8))
        self.link_label.setText(QtGui.QApplication.translate("DataConnector", "Links", None, QtGui.QApplication.UnicodeUTF8))
        self.link_list.setToolTip(QtGui.QApplication.translate("DataConnector", "Select to remove links", None, QtGui.QApplication.UnicodeUTF8))
        self.un_glue_button.setToolTip(QtGui.QApplication.translate("DataConnector", "Remove the selected connection", None, QtGui.QApplication.UnicodeUTF8))
        self.un_glue_button.setText(QtGui.QApplication.translate("DataConnector", "Un-Glue", None, QtGui.QApplication.UnicodeUTF8))
        self.ok.setToolTip(QtGui.QApplication.translate("DataConnector", "Accept proposed connections", None, QtGui.QApplication.UnicodeUTF8))
        self.ok.setText(QtGui.QApplication.translate("DataConnector", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.cancel.setToolTip(QtGui.QApplication.translate("DataConnector", "Discard proposed connections", None, QtGui.QApplication.UnicodeUTF8))
        self.cancel.setText(QtGui.QApplication.translate("DataConnector", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

