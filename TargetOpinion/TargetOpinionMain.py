import sys
from PyQt5 import QtWidgets
from NLP.TargetOpinion.TargetOpinion.Interface.Interface import MainWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myshow = MainWindow()
    myshow.show()
    sys.exit(app.exec_())
