import ctypes
from ctypes import wintypes


sound_library = ctypes.windll.Winmm
PlaySoundA = sound_library.PlaySoundA
PlaySoundW = sound_library.PlaySoundW
mciSendStringA = sound_library.mciSendStringA
mciGetErrorStringA = sound_library.mciGetErrorStringA
