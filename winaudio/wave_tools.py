import wave
import io


def wave_to_bytes(wave_obj: wave.Wave_read) -> bytes:
    buffer = io.BytesIO()
    wave_out: wave.Wave_write = wave.open(buffer, 'wb')
    wave_out.setnchannels(wave_obj.getnchannels())
    wave_out.setsampwidth(wave_obj.getsampwidth())
    wave_out.setframerate(wave_obj.getframerate())
    pos = wave_obj.tell()
    wave_out.writeframes(wave_obj.readframes(wave_obj.getnframes() - pos))
    wave_out.close()
    buffer.seek(0)
    result = buffer.read()
    buffer.close()
    return result


def bytes_to_wave(bytes_obj: bytes) -> wave.Wave_read:
    return wave.open(io.BytesIO(bytes_obj), 'rb')
