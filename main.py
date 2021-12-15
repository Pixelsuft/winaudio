import os
import random
import io
import winaudio


windows_sounds = winaudio.get_windows_sounds(ext_filter=('wav', ))
sound_path = windows_sounds.get('Windows Logon')
if sound_path:
    print(f'Playing wave {sound_path}...')
    winaudio.play_wave_sound(sound_path, winaudio.SND_SYNC)  # Wait Until Finish


try:
    mp3_url = 'https://audio.ngfiles.com/1006000/1006769_Clubstep-Djoxy-remix-DEMO.mp3'
    print(f'Playing {mp3_url}')
    import requests
    from pydub import AudioSegment
    mp3_buffer = io.BytesIO(
        requests.get(mp3_url).content
    )
    pydub_obj = AudioSegment.from_file(mp3_buffer, format='mp3')
    wave_buffer = io.BytesIO()
    pydub_obj.export(wave_buffer, format='wav')  # Convert To Wave
    wave_buffer.seek(0)  # Move Cursor To The Start Of File
    winaudio.play_wave_sound(wave_buffer, winaudio.SND_SYNC)
    wave_buffer.close()
except Exception as err_:
    print(f'Failed to play: {err_}')


mp3_dir_path = os.path.join(
    os.getcwd(),
    'example_audios'
)
mp3_path = os.path.join(
    mp3_dir_path,
    random.choice(os.listdir(mp3_dir_path))
)
mp3 = winaudio.AudioPlayer(mp3_path, sync=False)

print(f'Playing mp3: {mp3}')
mp3.force_play()

while mp3.is_playing():  # Wait until finish, same as "winaudio.AudioPlayer(mp3_path, sync=True)"
    pass

mp3.stop()
mp3.close()
