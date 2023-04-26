class Province(object):
    def __init__(self, title, desc):
        self.title = title
        self.desc = desc
    def text(self):
        return self.title + "," + \
            self.desc
