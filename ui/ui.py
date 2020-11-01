# -*- coding: utf-8 -*-
from kw.kw import *

import sys
from PyQt5.QtWidgets import *

class UI_class():
    def __init__(self):
        print('-' * 25)
        print('UI Class')
        print('-' * 25)

        self.app = QApplication(sys.argv)

        self.kw = KW_class()

        self.app.exec_()