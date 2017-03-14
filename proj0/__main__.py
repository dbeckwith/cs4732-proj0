#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import QApplication

from proj0.mainwindow import MainWindow


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser('proj0')
    args = parser.parse_args()

    app = QApplication([])

    mw = MainWindow()
    mw.show()

    sys.exit(app.exec_())
