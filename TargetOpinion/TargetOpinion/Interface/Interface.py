#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '评价对象和评价词程序界面'
__author__ = '皮'
__time__ = '12/29/2015-029'

"""
import os
import configparser
from PyQt5 import QtCore, QtGui, QtWidgets
from .InterfaceOrigin import Ui_MainWindow
from ..Algorithm.Analysis import analysis
from ..GlobalOptions import GlobalOptions

QtCore.QTextCodec.setCodecForLocale(QtCore.QTextCodec.codecForName("UTF-8"))
FILE_REALPATH = os.path.split(os.path.realpath(__file__))[0]
CONFIG_FILE_PATH = os.path.join(FILE_REALPATH, FILE_REALPATH, GlobalOptions.CONFIG_FILE_PATH)


class MainWindow(Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        # QtWidgets.QMainWindow.__init__(self)
        super(MainWindow, self).__init__()

        self.judgeConfigFile()
        """全局变量"""
        # 剪切板
        self.clipboard = QtWidgets.QApplication.clipboard()
        # 是否重置
        self.reset = False
        # 配置文件
        self.config = configparser.ConfigParser()
        self.config.read(CONFIG_FILE_PATH)

        self.setupUi(self)
        self.setupUI()

        self.createActions()
        self.createStatusBar()
        self.createMenubars()
        self.CreateFileBrowser()
        self.CreateAnalysis()

        self.readSettings()
        self.setCurrentFile('')

    def setupUI(self):
        '''
        继续用代码设置界面
        '''
        self.setWindowTitle(GlobalOptions.WINDOW_TITLE)
        self.setWindowIcon(QtGui.QIcon(os.path.join(FILE_REALPATH, FILE_REALPATH, "Images/analysor.png")))

        # UI输入输出变量名设置
        self.text_input = self.text_input
        self.text_output = self.table_output

        # self.read_file_button.setIcon(QtGui.QIcon(os.path.join(FILE_REALPATH,  "Images/yellow_spot.png")))

    # 读取配置文件配置显示及文本显示
    def readSettings(self):
        text = self.text_input
        # 宽度 高度
        width = getConfig(self.config, "Display", "width", "1000")
        height = getConfig(self.config, "Display", "height", "600")
        size = QtCore.QSize(int(width), int(height))

        # 屏幕位置
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        pos_x = getConfig(self.config, "Display", "X", (screen.width() - 1000) // 2)
        pos_y = getConfig(self.config, "Display", "y", (screen.height() - 600) // 2)
        pos = QtCore.QPoint(int(pos_x), int(pos_y))

        # 是否显示工具栏
        # toolbar = getConfig(self.config, "Display", "toolbar", "True")

        # 是否自动换行
        wrapMode = getConfig(self.config, "TextEdit", "wrapmode", "True")

        # 字体
        fontFamile = getConfig(self.config, "TextEdit", "font", "Consolas")
        fontSize = getConfig(self.config, "TextEdit", "size", '14')
        fonts = QtGui.QFont(fontFamile, int(fontSize))

        if "True" == wrapMode:
            self.autoWrapAction.setIcon(QtGui.QIcon(os.path.join(FILE_REALPATH, FILE_REALPATH, "Images/check.png")))
            wrapMode = QtWidgets.QTextEdit.WidgetWidth
        else:
            self.autoWrapAction.setIcon(QtGui.QIcon(os.path.join(FILE_REALPATH, FILE_REALPATH, "Images/check_no.png")))
            wrapMode = QtWidgets.QTextEdit.NoWrap

        self.resize(size)
        self.move(pos)
        self.text_input.setLineWrapMode(wrapMode)
        text.setFont(fonts)

    def writeSettings(self):
        text = self.text_input
        # 宽度、高度
        writeConfig(self.config, "Display", "height", str(self.size().height()))
        writeConfig(self.config, "Display", "width", str(self.size().width()))
        # 位置
        writeConfig(self.config, "Display", "X", str(self.pos().x()))
        writeConfig(self.config, "Display", "y", str(self.pos().y()))
        # 自动换行
        writeConfig(self.config, "TextEdit", "wrapmode",
                    str(text.lineWrapMode() == QtWidgets.QPlainTextEdit.WidgetWidth))
        # 字体
        writeConfig(self.config, "TextEdit", "font", text.font().family())
        # 大小
        writeConfig(self.config, "TextEdit", "size", str(text.font().pointSize()))

        # 回写
        self.config.write(open(CONFIG_FILE_PATH, "w"))

    def resetSettings(self):
        # 宽度、高度
        writeConfig(self.config, "Display", "width", "667")
        writeConfig(self.config, "Display", "height", "534")
        # 位置(x = 538, y = 87)
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        writeConfig(self.config, "Display", "X", str((screen.width() - 1000) // 2))
        writeConfig(self.config, "Display", "y", str((screen.height() - 600) // 2))
        # 工具栏
        writeConfig(self.config, "Display", "toolbar", "True")
        # 自动换行
        writeConfig(self.config, "TextEdit", "wrapmode", "True")
        # 字体(SimSun)
        writeConfig(self.config, "TextEdit", "font", "Consolas")
        # 大小(9)
        writeConfig(self.config, "TextEdit", "size", "14")

        # 回写
        self.config.write(open(CONFIG_FILE_PATH, "w"))

        QtWidgets.QMessageBox.information(self, "Analysor.exe", "重置配置成功，请重启！")
        self.reset = True
        self.close()

    def judgeConfigFile(self):
        if not os.path.exists(CONFIG_FILE_PATH):
            f = open(CONFIG_FILE_PATH, mode="w", encoding="UTF-8")
            f.close()

    # 事件触发处理
    def createActions(self):
        self.openAction = QtWidgets.QAction(QtGui.QIcon(os.path.join(FILE_REALPATH, 'Images/open.png')), "&打开...", self,
                                            shortcut=QtGui.QKeySequence.Open, statusTip="打开文件",
                                            triggered=self.openFileEvent)

        self.saveAction = QtWidgets.QAction(QtGui.QIcon(os.path.join(FILE_REALPATH, 'Images/save.png')), "&保存", self,
                                            shortcut=QtGui.QKeySequence.Save, statusTip="保存文件", triggered=self.save)

        self.saveAsAction = QtWidgets.QAction(QtGui.QIcon(os.path.join(FILE_REALPATH, 'Images/save.png')), "另存为...",
                                              self, shortcut=QtGui.QKeySequence.SaveAs, statusTip="另存文件",
                                              triggered=self.saveAs)

        self.exitAction = QtWidgets.QAction(QtGui.QIcon(os.path.join(FILE_REALPATH, 'Images/exit.png')), "退出", self,
                                            shortcut="Ctrl+Q", statusTip="退出程序", triggered=self.close)
        self.resetAction = QtWidgets.QAction(QtGui.QIcon(os.path.join(FILE_REALPATH, "Images/reset.png")), "重置", self,
                                             statusTip="重置所有属性", triggered=self.resetSettings)
        self.autoWrapAction = QtWidgets.QAction(QtGui.QIcon(os.path.join(FILE_REALPATH, "Images/check.png")), "自动换行",
                                                self, statusTip="设置自动换行", triggered=self.setWrap)

    def createStatusBar(self):
        self.statusBar().showMessage("Already!")

    def createMenubars(self):
        file = self.menuBar().addMenu("File")
        file.addAction(self.openAction)
        file.addAction(self.saveAction)
        file.addAction(self.saveAsAction)
        file.addSeparator()
        file.addAction(self.exitAction)

        style = self.menuBar().addMenu("Format")
        style.addAction(self.autoWrapAction)
        style.addAction(self.resetAction)

    def CreateFileBrowser(self):
        self.read_file_button.clicked.connect(self.openFileEvent)
        self.save_file_button.clicked.connect(self.save)

    def Analysis(self):
        '''
        分析text_input中的内容，并将其分析结果输出到text_output中
        '''
        # self.text_output.setDocument(QtGui.QTextDocument(analysis(self, self.text_input.toPlainText())))
        # self.list_output.addItems(analysis(self, self.text_input.toPlainText()))

        self.table_output.setSortingEnabled(False)
        __sortingEnabled = self.table_output.isSortingEnabled()
        self.table_output.setSortingEnabled(__sortingEnabled)

        # item = self.table_output.horizontalHeaderItem(0)
        # item.setText(_translate("MainWindow", "sen"))
        # item = self.table_output.horizontalHeaderItem(1)
        # item.setText(_translate("MainWindow", "opinion"))
        # item = self.table_output.verticalHeaderItem(id)
        # item.setText(_translate("MainWindow", str(id)))

        sen_list, result_list, sen_opinion_list = analysis(self, self.text_input.toPlainText())
        self.table_output.setRowCount(len(sen_list))
        self.table_output.setColumnCount(3)
        for id, (sen, result, sen_opinion) in enumerate(zip(sen_list, result_list, sen_opinion_list)):
            item = QtWidgets.QTableWidgetItem()
            self.table_output.setItem(id, 0, item)
            item.setText(sen)
            item = QtWidgets.QTableWidgetItem()
            self.table_output.setItem(id, 1, item)
            item.setText(result)
            item = QtWidgets.QTableWidgetItem()
            self.table_output.setItem(id, 2, item)
            item.setText(sen_opinion)

    def CreateAnalysis(self):
        self.analysis_button.clicked.connect(self.Analysis)

    def openFileEvent(self):
        # if self.maybeSave():        # 如果先前被打开的文件已被修改，需要提示
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self)
        file = QtCore.QFile(fileName)
        if not file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
            QtWidgets.QMessageBox.warning(self, "analysis",
                                          "file %s can't be readed:\n%s." % (fileName, file.errorString()))
            return

        inf = QtCore.QTextStream(file)
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        self.text_input.setPlainText(inf.readAll())
        QtWidgets.QApplication.restoreOverrideCursor()

        # self.setCurrentFile(fileName)
        self.statusBar().showMessage("file readed successfully", 2000)

    # 文件保存
    def setCurrentFile(self, fileName):
        self.curFile = fileName
        self.setWindowModified(False)

    def save(self):
        if self.curFile:
            return self.saveFile(self.curFile)
        else:
            return self.saveAs()

    def saveAs(self):
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self)
        if fileName:
            return self.saveFile(fileName)

        return False

    def saveFile(self, fileName):
        '''
        将分析结果保存到文件中
        '''
        file = QtCore.QFile(fileName)
        if not file.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QtWidgets.QMessageBox.warning(self, "Analysis",
                                          "file %scan't not be written:\n%s." % (fileName, file.errorString()))
            return False

        outf = QtCore.QTextStream(file)
        # QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        result_content = [[self.table_output.item(row, col).text() for col in range(self.table_output.columnCount())]
                          for row in range(self.table_output.rowCount())]
        str = '\n'.join(['\t'.join(i) for i in result_content])
        outf << str

        self.setCurrentFile(fileName)
        self.statusBar().showMessage("file written successfully", 2000)
        return True

    def saveFile_Error(self, fileName):
        file = QtCore.QFile(fileName)
        if not file.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QtWidgets.QMessageBox.warning(self, "Analysis",
                                          "file %scan't not be written:\n%s." % (fileName, file.errorString()))
            return False

        outf = QtCore.QTextStream(file)
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        # outf << self.text_output.contentsRect()
        outf << self.text_output  # 怎么直接将tWidgets.QTableWidget保存为txt????
        QtWidgets.QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName)
        self.statusBar().showMessage("file written successfully", 2000)
        return True

    # 结束事件
    def closeEvent(self, event):
        if not self.reset:
            self.writeSettings()
        event.accept()

    # 设置界面效果
    def setWrap(self):
        text = self.text_input
        mode = text.lineWrapMode()
        if 1 == mode:
            # 自动换行
            text.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
            self.autoWrapAction.setIcon(QtGui.QIcon(os.path.join(FILE_REALPATH, "Images/check_no.png")))
        else:
            # 不自动换行
            text.setLineWrapMode(QtWidgets.QTextEdit.WidgetWidth)
            self.autoWrapAction.setIcon(QtGui.QIcon(os.path.join(FILE_REALPATH, "Images/check.png")))


def getConfig(config, selection, option, default=""):
    if config is None:
        # print("config is none!!!")
        return default
    else:
        try:
            return config.get(selection, option)
        except:
            # print("config %s/%s setting error!!!" % (selection, option))
            return default


def writeConfig(config, selection, option, value):
    if not config.has_section(selection):
        config.add_section(selection)

    config.set(selection, option, value)


class MyWindow(MainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        # self.setupUi(self)
