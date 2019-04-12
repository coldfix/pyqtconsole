# -*- coding: utf-8 -*-
from threading import Lock
from .qt import QtCore

class Stream(QtCore.QEventLoop):
    write_event = QtCore.Signal(str)
    flush_event = QtCore.Signal(str)
    close_event = QtCore.Signal()

    def __init__(self):
        super(Stream, self).__init__()
        self._buffer = ''
        self._mutex = Lock()
        self.write_event.connect(self.exit)

    def readline(self, block=True):
        while True:
            with self._mutex:
                if '\n' in self._buffer:
                    data, self._buffer = self._buffer.split('\n', 1)
                    return data
                elif not block:
                    return ''
            self.exec_()

    def write(self, data):
        with self._mutex:
            self._buffer += data
        self.write_event.emit(data)

    def flush(self):
        with self._mutex:
            data = self._buffer
            self._buffer = ''
        self.flush_event.emit(data)
        return data

    def close(self):
        self.close_event.emit()
