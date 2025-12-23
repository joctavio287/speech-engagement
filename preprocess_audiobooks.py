"""
Preprocess audiobook stimuli by performing the following steps
1. Convert to WAV
2. Cut to specific time intervals
3. Isolate vocals
4. Resample to 48 kHz
5. Generate a bip sound file
6. Create a CSV file with stimulus information
"""
from pathlib import Path
import pandas as pd

from utils.audio_helpers import (
    scale_audio_to_relative_db,
    vocal_isolation,
    resample_audio,
    convert_to_wav,
    AudioSegment,
    Sine
)
QUESTIONARY_CSV = Path(r'audiobook_stimuli\questionary.csv')
AUDIOBOOKLOOP_UNENGAGED = Path(r"unengaged_audiobook_experiment\AudioBookLoop.csv")
AUDIOBOOKLOOP_ENGAGED = Path(r"engaged_audiobook_experiment\AudioBookLoop.csv")
FAKE_AUDIO = Path(r'audiobook_stimuli\stimuli_audiobook\prueba.wav')

# AUDIO_DIR = Path(r'audiobook_stimuli\cuentos_casciari')
CUT_TIMES = { # s
    '25_canelones': (5, 281.9), # total 277 s -> 4.6 min
    'lugones': (4.9, 306.5), # total 301.6 s -> 5.0 min
    'kafka': (5.5, 321), # total 315.5 s -> 5.3 min
}
AUDIO_DIR = Path(r'audiobook_stimuli\cuentos_dicotica')
OUTPUT_DIR = Path(r'audiobook_stimuli\stimuli_audiobook')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SAMPLE_RATE = 48000  # Hz
NUMBER_OF_BIPS = 1
BIP_FREQ = 1000  # Hz
BIP_DUR = 500   # ms
BIP_VOL = -20  # dB

audio_books = sorted(
    list(AUDIO_DIR.glob("*.m4a")) + list(AUDIO_DIR.glob("*.mp3"))
)
output_file_associations = {}
for j, book in enumerate(audio_books):
    output_file = OUTPUT_DIR / book.stem
    if book.stem in CUT_TIMES:
        vocal_isolation(output_file, output_file)
    start_time, end_time = CUT_TIMES.get(book.stem, (0, None))
    convert_to_wav(book, output_file, start_time, end_time)
    resample_audio(output_file, output_file, target_sample_rate=SAMPLE_RATE)
    if j == 0:
        ref_to_scale_to = output_file
    else:
        scale_audio_to_relative_db(
            audio_to_scale_path=output_file,
            reference_audio_path=ref_to_scale_to,
            target_db_diff=0
        )
    print(f'Processed {output_file.name}')
    output_file_associations[book.stem] = output_file

# Create a new audio being a bip of .5 second
bip_tone = (
    Sine(BIP_FREQ)
    .to_audio_segment(duration=BIP_DUR, volume=BIP_VOL)
    .set_frame_rate(SAMPLE_RATE)
)
silence = AudioSegment.silent(
    duration=BIP_DUR, frame_rate=SAMPLE_RATE
)
bip_segment = bip_tone + silence
for _ in range(NUMBER_OF_BIPS - 1):
    bip_segment += bip_tone + silence
bip_segment = bip_segment.set_frame_rate(SAMPLE_RATE)
bip_segment.export(
    OUTPUT_DIR / 'bip.wav', format='wav'
)

# Create .csv file with stimulus information
questionary_df = pd.read_csv(
    QUESTIONARY_CSV, sep=',', header=0
)
stimuli_info_unengaged = []
stimuli_info_engaged = []

for k, (bookname, audiobook_questionary) in enumerate(questionary_df.groupby('audiobook')):
    for n_question, row in audiobook_questionary.iterrows():
        data = {}
        for key in row.keys():
            data[key] = row[key]
        data['audio_filename'] = str(
            Path('..') / output_file_associations[bookname]
        )
        if k<2:
            stimuli_info_unengaged.append(data)
        else:
            stimuli_info_engaged.append(data)
df_unengaged = pd.DataFrame(stimuli_info_unengaged)
df_unengaged.to_csv(AUDIOBOOKLOOP_UNENGAGED, index=False)    
df_engaged = pd.DataFrame(stimuli_info_engaged)
df_engaged.to_csv(AUDIOBOOKLOOP_ENGAGED, index=False)

# Same with fake audio to test the experiment structure
stimuli_info_unengaged = []
stimuli_info_engaged = []
for k, (bookname, audiobook_questionary) in enumerate(questionary_df.groupby('audiobook')):
    for n_question, row in audiobook_questionary.iterrows():
        data = {}
        for key in row.keys():
            data[key] = row[key]
        data['audio_filename'] = str(
            Path('..') / FAKE_AUDIO
        )
        if k<2:
            stimuli_info_unengaged.append(data)
        else:
            stimuli_info_engaged.append(data)
df_unengaged = pd.DataFrame(stimuli_info_unengaged)
df_engaged = pd.DataFrame(stimuli_info_engaged)
df_unengaged.to_csv(AUDIOBOOKLOOP_UNENGAGED.with_stem('AudioBookLoop_pruebas'), index=False)    
df_engaged.to_csv(AUDIOBOOKLOOP_ENGAGED.with_stem('AudioBookLoop_pruebas'), index=False)