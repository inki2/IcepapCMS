#!/usr/bin/env python


import sys
try:
    from PyQt5 import QtGui
except ImportError as e:
    from PyQt4 import QtGui
from ui_icepapcms import OscillaWindow


def main(host, port):
    app = QtGui.QApplication(sys.argv)
    oscilla_window = OscillaWindow(host, port)
    oscilla_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    if len(sys.argv) == 3:
        main(sys.argv[1], int(sys.argv[2]))
    else:
        print('Usage: oscilla <host> <port>')
        print('Example: oscilla w-kitslab-icepap-11 5000')
