from bisect import bisect_left


class Log(object):

    def __init__(self):
        self.records = []
        self.linenos = Partition()
        self.positions = Partition()

    def __len__(self):
        return len(self.records)

    def __getitem__(self, index):
        return self.records[index]

    def __setitem__(self, index, record):
        self.records[index] = record
        self.linenos[index] = record.num_lines
        self.positions[index] = len(record.text)

    def __delitem__(self, index):
        del self.records[index]
        del self.linenos[index]
        del self.positions[index]

    def append(self, record):
        self.records.append(record)
        self.linenos.append(record.num_lines)
        self.positions.append(len(record.text))

    def insert(self, index, record):
        self.records.insert(index, record)
        self.linenos.insert(index, record.num_lines)
        self.positions.insert(index, len(record.text))


class Partition(object):

    def __init__(self):
        self._locs = [0]

    def __len__(self):
        """Number of chunks in the partition."""
        return len(self._locs) - 1

    def __getitem__(self, index):
        """Get chunk size of the n'th chunk."""
        index = self._check_index(index)
        return self._locs[index + 1] - self._locs[index]

    def __setitem__(self, index, size):
        """Set the chunk size of the n'th chunk."""
        index = self._check_index(index)
        self._update_locs(index + 1, size - self._locs[index])

    def __delitem__(self, index):
        """Remove the n'th chunk."""
        index = self._check_index(index)
        size = self._locs.pop(index)
        self._update_locs(index, -size)

    def append(self, size):
        """Append a chunk with the given ``size``."""
        self._locs.append(self._locs[-1] + size)

    def insert(self, index, size):
        """Insert a chunk with the given ``size`` at ``index``."""
        index = self._check_index(index)
        self._locs.insert(index, self._locs[index])
        self._update_locs(index + 1, size)

    def find_loc(self, loc):
        """Find the index of the chunk that contains the given position."""
        return bisect_left(self._locs, loc)

    def first(self, index):
        """Get the starting location of the n'th chunk."""
        index = self._check_index(index)
        return self._locs[index]

    def last(self, index):
        """Get the stop location of the n'th chunk."""
        index = self._check_index(index)
        return self._locs[index + 1] - 1

    def _check_index(self, index):
        """Check and sanitize index, turn negative number into positive index."""
        assert isinstance(index, int)
        if index < -len(self) or index >= len(self):
            raise IndexError(
                "list index {} out of range in list of size {}"
                .format(index, len(self)))
        if index < 0:
            index += len(self)
        return index

    def _update_locs(self, start_index, added_lines):
        """Update locations starting from ``start_index``."""
        for i in range(start_index, len(self._locs)):
            self._locs[i] += added_lines
