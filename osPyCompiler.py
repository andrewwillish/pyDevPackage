from PyQt4 import QtCore, QtGui, uic
import os
import sys
import xml.etree.cElementTree as ET
import imp
import shutil

#Determining SCRIPT_ROOT
SCRIPT_ROOT = os.path.dirname(os.path.realpath(__file__)).replace('\\','/')

class crControllerUI(QtGui.QWidget):
    def __init__(self, *args):
        QtGui.QMainWindow.__init__(self, *args)
        self.main = uic.loadUi(SCRIPT_ROOT+'/osPyCompilerUI.ui')
        self.main.show()
        self.main.setFixedSize(260, 667)

        #check if config.xml
        if not os.path.isfile(SCRIPT_ROOT+'/config.xml'):
            root = ET.Element('root')

            writ = ET.SubElement(root, 'currentWorkPath')
            writ.text = ''
            targ = ET.SubElement(root, 'targetList')
            tree = ET.ElementTree(root)
            tree.write(SCRIPT_ROOT+'/config.xml')

        tree = ET.parse(SCRIPT_ROOT+'/config.xml')
        root = tree.getroot()

        #write work path
        self.main.workPathLineEdit.setText(str(root[0].text))

        #connect function
        self.main.workPathBrowseButton.clicked.connect(self.workPathFileDialog)
        self.main.addTargetButton.clicked.connect(self.addTarget)
        self.main.deleteTargetButton.clicked.connect(self.deleteTarget)
        self.main.dispatchButton.clicked.connect(self.dispatch)

        #refresh
        self.refreshSource()
        self.refreshTarget()
        return

    def dispatch(self):
        sourcePath = str(self.main.workPathLineEdit.text())
        filename = str(self.main.pySourceList.currentItem().text()).replace('.py', '')
        targetPath = str(self.main.targetList.currentItem().text())

        if sourcePath!= '' and filename is not None and targetPath is not None:
            #compile source
            imp.load_source(filename, sourcePath + '/' + filename + '.py')

            #dispatch to server
            if os.path.isfile(targetPath+'/'+filename+'.pyc'):
                repVar = QtGui.QMessageBox.question(None, 'osPyCompiler', \
                                                    'There is an identical script in the server. Overwrite?',\
                                                    QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                if repVar == 16384:
                    os.remove(targetPath+'/'+filename+'.pyc')
                    shutil.copy(sourcePath+'/'+filename+'.pyc', targetPath+'/'+filename+'.pyc')
                    QtGui.QMessageBox.information(None, 'osPyCompiler', \
                                                  'Script dispatched.', QtGui.QMessageBox.Ok)
            else:
                os.remove(targetPath+'/'+filename+'.pyc')
                shutil.copy(sourcePath+'/'+filename+'.pyc', targetPath+'/'+filename+'.pyc')
                QtGui.QMessageBox.information(None, 'osPyCompiler', \
                                              'Script dispatched.', QtGui.QMessageBox.Ok)
        return

    def deleteTarget(self):
        itemDel = self.main.targetList.currentItem()
        itemDel = str(itemDel.text())

        if not os.path.isfile(SCRIPT_ROOT+'/config.xml'):
            root = ET.Element('root')
        else:
            tree = ET.parse(SCRIPT_ROOT+'/config.xml')
            root = tree.getroot()

        for chk in root[1]:
            if str(chk.text) == str(itemDel):
                root[1].remove(chk)
        tree = ET.ElementTree(root)
        tree.write(SCRIPT_ROOT+'/config.xml')

        self.refreshTarget()
        return

    def refreshTarget(self):
        if not os.path.isfile(SCRIPT_ROOT+'/config.xml'):
            root = ET.Element('root')
        else:
            tree = ET.parse(SCRIPT_ROOT+'/config.xml')
            root = tree.getroot()

        self.main.targetList.clear()
        for chk in root[1]:
            self.main.targetList.addItem(str(chk.text))
        return

    def addTarget(self):
        targetPath = str(QtGui.QFileDialog.getExistingDirectory())
        print targetPath == ''
        if targetPath != '':
            #check if config.xml
            if not os.path.isfile(SCRIPT_ROOT+'/config.xml'):
                root = ET.Element('root')
            else:
                tree = ET.parse(SCRIPT_ROOT+'/config.xml')
                root = tree.getroot()

            ext = False
            for chk in root[1]:
                if str(chk.text) == targetPath: ext = True

            if not ext:
                writ = ET.SubElement(root[1], 'targetItem')
                writ.text = str(targetPath)

                tree = ET.ElementTree(root)
                tree.write(SCRIPT_ROOT+'/config.xml')
        self.refreshTarget()
        return

    def refreshSource(self):
        filePath = str(self.main.workPathLineEdit.text())
        self.main.pySourceList.clear()
        if os.path.isdir(filePath):
            for item in os.listdir(filePath):
                if item.endswith('.py'):
                    self.main.pySourceList.addItem(str(item))
        return

    def workPathFileDialog(self):
        filePath = QtGui.QFileDialog.getExistingDirectory()
        self.main.workPathLineEdit.setText(str(filePath))
        self.setWorkPath(workPath=str(filePath))
        return

    def setWorkPath(self, workPath=None):
        #check if config.xml
        if not os.path.isfile(SCRIPT_ROOT+'/config.xml'):
            root = ET.Element('root')
        else:
            tree = ET.parse(SCRIPT_ROOT+'/config.xml')
            root = tree.getroot()

        root[0].text = str(workPath)
        tree = ET.ElementTree(root)
        tree.write(SCRIPT_ROOT+'/config.xml')

        self.refreshSource()
        return

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = crControllerUI()
    sys.exit(app.exec_())