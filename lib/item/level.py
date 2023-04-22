class Level(object):
    def __init__(self, title, desc):
        self.title = title
        desc = ','.join(desc)
        self.desc = desc
    def text(self):
        return self.title + "," + \
            self.desc
