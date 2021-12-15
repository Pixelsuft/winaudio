import io
import os
from .flags import *
from .ctypes_binds import *
from .exceptions import *
from .wave_tools import *


os.environ['WINAUDIO_NO_WAVEPLAYERROR'] = str(True)  # Wtf why always true from play_wave_sound


def play_wave_from_filename(filename: str, flags: int = SND_ASYNC) -> bool:
    result = PlaySoundW(
        filename,
        NULL,
        flags
    )
    if result:
        if not bool(os.getenv('WINAUDIO_NO_WAVEPLAYERROR')):
            raise WavePlayError('Failed To Play Wave')
        return True
    return False


def play_wave_from_bytesio(bytes_obj: io.BytesIO, flags: int = SND_ASYNC) -> bool:
    result = PlaySoundA(
        bytes_obj.read(),
        NULL,
        flags | SND_MEMORY
    )
    if result:
        if not bool(os.getenv('WINAUDIO_NO_WAVEPLAYERROR')):
            raise WavePlayError('Failed To Play Wave')
        return True
    return False


def play_wave_from_bytes(bytes_obj: bytes, flags: int = SND_ASYNC) -> bool:
    result = PlaySoundA(
        bytes_obj,
        NULL,
        flags | SND_MEMORY
    )
    if result:
        if not bool(os.getenv('WINAUDIO_NO_WAVEPLAYERROR')):
            raise WavePlayError('Failed To Play Wave')
        return True
    return False


def play_wave_from_wave(wave_obj: wave.Wave_read, flags: int = SND_ASYNC) -> bool:
    result = PlaySoundA(
        wave_to_bytes(wave_obj),
        NULL,
        flags | SND_MEMORY
    )
    if result:
        if not bool(os.getenv('WINAUDIO_NO_WAVEPLAYERROR')):
            raise WavePlayError('Failed To Play Wave')
        return True
    return False


wave_play_types = {
    str: play_wave_from_filename,
    bytes: play_wave_from_bytes,
    wave.Wave_read: play_wave_from_wave,
    io.BytesIO: play_wave_from_bytesio
}


def play_wave_sound(play_object: any, flags: int = SND_ASYNC) -> bool:
    func_to_play = wave_play_types.get(type(play_object))
    if not func_to_play:
        if not bool(os.getenv('WINAUDIO_NO_NOFUNCTIONERROR')):
            raise ArgumentError(f'Failed To Find Function To Play: {type(play_object)}')
        return True
    return func_to_play(play_object, flags)
