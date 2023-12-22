import os
os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'
import sys
from window_login import LoginWindow
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':

    # if nothing in db, fill in with the necessary info.
    
    app = QApplication(sys.argv)
    ex = LoginWindow()
    sys.exit(app.exec_())