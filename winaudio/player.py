from .sound_mci import MCI
from .exceptions import *
from .flags import *


class AudioPlayer:
    def __init__(
            self,
            filename: str,
            alias: str = None,
            sync: bool = False,
            buffer_size: int = 255,
            encoding: str = ENCODING
    ) -> None:
        super(AudioPlayer, self).__init__()
        self.fn = filename
        self.alias = alias or filename
        self.buffer_size = buffer_size
        self.encoding = encoding
        self.sync = sync
        self.mci = MCI(
            buffer_size=self.buffer_size,
            encoding=self.encoding
        )
        self.length_ms = 0
        self.load()

    def get_length_ms(self) -> int:
        return int(self.mci.send(f'status "{self.alias}" length'))

    def load(self) -> None:
        self.mci.send(f'open "{self.fn}" alias "{self.alias}"')
        self.mci.send(f'set "{self.alias}" time format milliseconds')
        self.length_ms = self.get_length_ms()

    def play(self, from_ms: any = None, to_ms: any = None) -> None:
        command = f'play "{self.alias}"'
        if from_ms:
            command += f' from {from_ms}'
        if to_ms:
            command += f' to {to_ms}'
        if self.sync:
            command += ' wait'
        self.mci.send(command)

    def get_mode(self) -> str:
        return self.mci.send(f'status "{self.alias}" mode')

    def get_position(self) -> int:
        return int(self.mci.send(f'status "{self.alias}" position'))

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
        return f'<AudioPlayer file="{self.fn}" length="{self.length_ms}ms">'

    def __repr__(self, *args, **kwargs) -> str:
        return self.__str__(*args, **kwargs)

    def __del__(self) -> None:
        self.close()
