class OneSegmentBorderException(Exception):
    def __init__(self, s1, s2):
        super().__init__(
            "Border must contains more than 2 segments, but was {} {}"
                .format(s1, s2))


class NotClosedBorderError(Exception):
    def __init__(self, i, s1, s2):
        super().__init__(
            "Border is not connected on number {}, segments:{} {}"
                .format(i, s1, s2))


class NotEnoughColorsInPalette(Exception):
    def __init__(self, need, was):
        super().__init__('Need {} colors, but was {}'.format(need, was))
