class BadFileSize(Exception):
    def __init__(self, filename, size, limit):
        self.filename = filename
        self.size = size
        self.limit = limit

    def __str__(self):
        return 'File %s too big, size: %d bytes, limit: %d bytes' % (
            self.filename, self.size, self.limit)


class TooMuchFiles(Exception):
    def __init__(self, total_files, limit):
        self.total_files = total_files
        self.limit = limit

    def __str__(self):
        return 'You have %d files, limit: %d' % (self.total_files, self.limit)
