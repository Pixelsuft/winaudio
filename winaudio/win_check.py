import os
import sys
import ctypes


def is_windows() -> bool:
    return bool(hasattr(ctypes, 'windll'))


if not is_windows():
    raise OSError(f'WinAudio Can\'t Be Runned Under {sys.platform} ({os.name})')
