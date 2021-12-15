import os
from .flags import *
from .ctypes_binds import *
from .exceptions import *


class MCI:
    def __init__(self, buffer_size: int = 255, encoding: str = ENCODING) -> None:
        super(MCI, self).__init__()
        self.mci = mciSendStringA
        self.error = mciGetErrorStringA
        self.buffer_size = buffer_size
        self.encoding = encoding

    def try_send(self, command: str):
        buffer = ctypes.c_buffer(self.buffer_size)
        error_code = self.mci(command.encode(self.encoding), buffer, self.buffer_size - 1, 0)
        return error_code, (
            self.get_error(error_code) if error_code else buffer.value.decode(self.encoding, errors='replace')
        )

    def get_error(self, error: int):
        buffer = ctypes.c_buffer(self.buffer_size)
        self.error(error, buffer, self.buffer_size - 1)
        return buffer.value.decode(self.encoding, errors='replace')

    def send(self, command: str):
        error, buffer = self.try_send(command)
        if error:
            if not bool(os.getenv('WINAUDIO_NO_PLAYSOUNDMCIERROR')):
                raise PlayerMciError(buffer)
            return buffer
        return buffer
