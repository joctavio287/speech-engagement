"""
Preprocess audiobook stimuli by performing the following steps
1. Convert to WAV
2. Cut to specific time intervals
3. Isolate vocals
4. Resample to 48 kHz
5. Generate a bip sound file
"""
from pathlib import Path

from utils.audio_helpers import (
    vocal_isolation,
    resample_audio,
    convert_to_wav,
    AudioSegment,
    Sine
)
AUDIO_DIR = Path(r'audiobook_stimuli\cuentos_casciari')
OUTPUT_DIR = Path(r'audiobook_stimuli\stimuli_audiobook')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CUT_TIMES = { # s
    '25_canelones': (5, 281.9), # total 277 s -> 4.6 min
    'lugones': (4.9, 306.5), # total 301.6 s -> 5.0 min
    'kafka': (5.5, 321), # total 315.5 s -> 5.3 min
}
SAMPLE_RATE = 48000  # Hz
NUMBER_OF_BIPS = 1
BIP_FREQ = 1000  # Hz
BIP_DUR = 500   # ms
BIP_VOL = -20  # dB

audio_books = sorted(
    list(AUDIO_DIR.glob("*.m4a")) + list(AUDIO_DIR.glob("*.mp3"))
)
for j, book in enumerate(audio_books):
    output_file = OUTPUT_DIR / f'audio{j+1:02d}.wav'
    start_time, end_time = CUT_TIMES.get(book.stem, (0, None))
    convert_to_wav(book, output_file, start_time, end_time)
    vocal_isolation(output_file, output_file)
    resample_audio(output_file, output_file, target_sample_rate=SAMPLE_RATE)
    print(f'Processed {output_file.name}')


# Create a new audio being a bip of .5 second
bip_file = OUTPUT_DIR / 'bip.wav'
bip_tone = (
    Sine(BIP_FREQ)
    .to_audio_segment(duration=BIP_DUR, volume=BIP_VOL)
    .set_frame_rate(SAMPLE_RATE)
)
silence = AudioSegment.silent(duration=BIP_DUR, frame_rate=SAMPLE_RATE)
bip_segment = bip_tone + silence
for _ in range(NUMBER_OF_BIPS - 1):
    bip_segment += bip_tone + silence
bip_segment = bip_segment.set_frame_rate(SAMPLE_RATE)
bip_segment.export(bip_file, format='wav')