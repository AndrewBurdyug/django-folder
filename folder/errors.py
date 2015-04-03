class BadData(BaseException):
    def __init__(self, msg, data):
        BaseException.__init__(self)
        self.msg = msg
        self.data = data

    def __str__(self):
        return 'Bad %s: %s' % (self.msg, self.data)
