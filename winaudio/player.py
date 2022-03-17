from .sound_mci import MCI
from .exceptions import *
from .flags import *


class AudioPlayer:
    def __init__(
            self,
            filename: str,
            alias: str = None,
            sync: bool = False,
            repeat: bool = False,
            buffer_size: int = 255,
            encoding: str = ENCODING
    ) -> None:
        super(AudioPlayer, self).__init__()
        self.fn = filename
        self.alias = alias or filename
        self.buffer_size = buffer_size
        self.encoding = encoding
        self.sync = sync
        self.repeat = repeat
        self.mci = MCI(
            buffer_size=self.buffer_size,
            encoding=self.encoding
        )
        self.wait_on_close = True
        self.length = 0
        self.load()

    def get_length(self) -> int:
        return int(self.get_var('length'))

    def load(self) -> None:
        self.mci.send(f'open "{self.fn}" alias "{self.alias}"')
        self.mci.send(f'set "{self.alias}" time format milliseconds')
        self.length = self.get_length()

    def play(self, from_ms: any = None, to_ms: any = None) -> None:
        command = f'play "{self.alias}"'
        if from_ms:
            command += f' from {from_ms}'
        if to_ms:
            command += f' to {to_ms}'
        if self.repeat:
            command += ' repeat'
        if self.sync:
            command += ' wait'
        self.mci.send(command)
    
    def get_var(self, var_name: str) -> str:
        return self.mci.send(f'status "{self.alias}" {var_name}')
    
    def set_var(self, var_name: str, var_content: any, use_q: bool = False) -> None:
        if use_q:
            self.mci.send(f'set "{self.alias}" {var_name} "{var_content}"')
        else:
            self.mci.send(f'set "{self.alias}" {var_name} {var_content}')

    def get_mode(self) -> str:
        return self.get_var('mode')

    def get_speed(self) -> float:
        return float(self.get_var('speed')) / 1000

    def set_speed(self, speed: float) -> None:
        return self.set_var('speed', round(speed * 1000))

    def get_volume(self) -> float:
        return float(self.get_var('volume')) / 1000

    def set_volume(self, volume: float) -> None:
        self.mci.send(f'setaudio "{self.alias}" volume to {round(volume * 1000)}')

    def get_position(self) -> int:
        return int(self.get_var('position'))

    def is_paused(self, current_mode: str = None) -> bool:
        return (current_mode or self.get_mode()) == 'paused'

    def is_stopped(self, current_mode: str = None) -> bool:
        return (current_mode or self.get_mode()) == 'stopped'

    def is_playing(self, current_mode: str = None) -> bool:
        return (current_mode or self.get_mode()) == 'playing'

    def pause(self) -> None:
        self.mci.send(f'pause "{self.alias}"')

    def resume(self) -> None:
        self.mci.send(f'resume "{self.alias}"')
    
    def wait_until_finish(self) -> None:
        while self.is_playing():
            pass

    def force_play(self, from_ms: any = None, to_ms: any = None) -> None:
        current_mode = self.get_mode()
        if self.is_playing(current_mode):
            return
        if self.is_stopped(current_mode):
            return self.play(from_ms, to_ms)
        if self.is_paused(current_mode):
            self.stop_no_seek()
            return self.play(from_ms, to_ms)

    def stop_no_seek(self) -> None:
        self.mci.send(f'stop "{self.alias}"')

    def stop(self) -> None:
        self.stop_no_seek()
        self.seek('start')

    def seek(self, to_ms: any) -> None:
        self.mci.send(f'seek "{self.alias}" to {to_ms}')

    def close(self) -> bool:
        try:
            self.mci.send(f'close "{self.alias}"')
            return True
        except PlayerMciError:
            return False

    def __str__(self, *args, **kwargs) -> str:
        return f'<AudioPlayer file="{self.fn}" length="{self.length}ms">'

    def __repr__(self, *args, **kwargs) -> str:
        return self.__str__(*args, **kwargs)

    def __del__(self) -> None:
        if self.wait_on_close and self.is_playing():
            wait_until_finish()
        self.close()
