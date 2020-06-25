from PyQt5.QtWidgets import *
from GUIComponents import UploadPage, StatsPage

from CustonWrappers import PyCute


class MainStack(QStackedWidget):

    def __init__(self):

        super().__init__()

        self.upload_page = UploadPage.UploadPage(parent_widget=self)
        self.stats_page = StatsPage.StatsPage(parent_widget=self)

        self.page_count = 2
        self.curr_page_index = 0

        PyCute.add_to_layout(self, self.upload_page, self.stats_page)

        self.setWindowTitle("Stats Software")
        self.setGeometry(100, 100, 500, 700)

        self.show()

    def switch_page(self):

        self.curr_page_index = (self.curr_page_index + 1) % self.page_count
        self.setCurrentIndex(self.curr_page_index)
        self.stats_page.data_table = self.upload_page.data_table
