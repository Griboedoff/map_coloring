class NotClosedBorderError(Exception):
    def __init__(self, i, s1, s2):
        super(NotClosedBorderError, self).__init__(
            "Border is not connected on number {}, segments:{} {}"
                .format(i, s1, s2))
