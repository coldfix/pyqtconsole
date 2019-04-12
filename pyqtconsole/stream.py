# -*- coding: utf-8 -*-
try:
    from queue import Queue
except ImportError:
    from Queue import Queue
from .qt import QtCore

class Stream(QtCore.QObject):
    write_event = QtCore.Signal(str)
    flush_event = QtCore.Signal(str)
    close_event = QtCore.Signal()

    def __init__(self):
        super(Stream, self).__init__()
        self._queue = Queue()

    def _reset_buffer(self):
        with self._queue.mutex:
            data = ''.join(self._queue.queue)
            self._queue.queue.clear()
            return data

    def _flush(self):
        data = self._reset_buffer()
        self._queue.put('')
        return data

    def readline(self, timeout = None):
        return self._queue.get(block=timeout != 0, timeout=timeout)

    def write(self, data):
        with self._queue.mutex:

            if '\n' in self._buffer:
                self._line_cond.notify()

            self.write_event.emit(data)

    def flush(self):
        data = self._flush()
        self.flush_event.emit(data)
        return data

    def close(self):
        self.close_event.emit()
