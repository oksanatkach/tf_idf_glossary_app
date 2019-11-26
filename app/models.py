from app import app
import os

DOWNLOAD_FOLDER = app.config['DOWNLOAD_FOLDER']
UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']


class Session:
    def __init__(self):
        self.gen = None
        self.top = []
        self.discarded = []

    def init_gen(self, gen):
        self.gen = gen

    def get_top_n(self, n):
        counter = 0
        while counter < n:
            self.top.append(next(self.gen)[0])
            counter += 1
        return self.top

    def update_discarded(self, term):
        self.top.remove(term)
        self.discarded.append(term)

    def get_discarded(self):
        return self.discarded

    def get_next(self):
        return next(self.gen)[0]

    def update_top(self, term):
        self.top.append(term)

    def get_top(self):
        return self.top

    def clean_session(self):
        self.gen = None
        self.top = []
        self.discarded = []
        for download_file in os.listdir(DOWNLOAD_FOLDER):
            os.remove(os.path.join(DOWNLOAD_FOLDER, download_file))
        # for upload_file in os.listdir(UPLOAD_FOLDER):
        #     os.remove(os.path.join(UPLOAD_FOLDER, upload_file))


if __name__ == '__main__':
    for download_file in os.listdir(DOWNLOAD_FOLDER):
        os.remove(os.path.join(DOWNLOAD_FOLDER, download_file))
