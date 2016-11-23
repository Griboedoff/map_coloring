from Exceptions.notClosedBorderError import NotClosedBorderError


class Country:
    def __init__(self, segments):
        self.segments = self._check_segments(segments)
        self._segments_set = set(segments)
        self.color = None
        self.incident_countries = set()

    @property
    def points(self):
        return [s.end for s in self.segments]

    def __contains__(self, item):
        return item in self._segments_set

    def is_neighbour(self, country):
        return country in self.incident_countries

    def _check_segments(self, segments):
        if segments[-1].end != segments[0].start:
            raise NotClosedBorderError(0, segments[0], segments[-1])

        for i in range(len(segments) - 1):
            if segments[i].end != segments[i + 1].start:
                raise NotClosedBorderError(i, segments[i], segments[i + 1])
        return segments

    def __str__(self):
        return ' | '.join(map(str, self.segments))