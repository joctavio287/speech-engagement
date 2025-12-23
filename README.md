# speech-engagement

This repository contains code and materials for experiments and analyses related to **speech engagement**.  
It includes utilities and scripts to prepare speech/audio stimuli (e.g., audiobooks), generate experiment-ready assets, and support downstream behavioral/experimental workflows.

## Goals / intent

- Prepare and standardize speech stimuli for engagement experiments (consistent format, duration, sample rate).
- Generate experiment metadata (CSV) linking stimuli to questionnaire items and conditions.
- Keep preprocessing and analysis code together so experiments are reproducible.

## Repository highlights

- `preprocess_audiobooks.py`: end-to-end preprocessing pipeline for audiobook stimuli:
  1. Convert source audio to WAV
  2. Cut to specified time intervals
  3. (Optional/implemented) isolate vocals
  4. Resample to 48 kHz
  5. Generate a short “bip” cue sound
  6. Produce experiment CSVs with stimulus/question mappings

- `utils/audio_helpers.py` (imported by the script): audio helper functions used for conversion, isolation, and resampling.
  - If you’re modifying preprocessing behavior, start here and in `preprocess_audiobooks.py`.

## Expected data layout

The preprocessing script currently assumes these paths (relative to the repo root):

- Source audio directory:
  - `audiobook_stimuli/cuentos_casciari/` containing `.m4a` and/or `.mp3`
- Questionnaire mapping:
  - `audiobook_stimuli/questionary.csv`
    - Must contain an `audiobook` column that matches the stem (filename without extension) of the source audio files.
- Outputs:
  - Processed stimuli written to `audiobook_stimuli/stimuli_audiobook/` (e.g., `audio01.wav`, `audio02.wav`, …, plus `bip.wav`)
  - Experiment CSVs written to:
    - `unengaged_audiobook_experiment/AudioBookLoop.csv`
    - `engaged_audiobook_experiment/AudioBookLoop.csv`

## Running the audiobook preprocessing

From the repo root:

```bash
python preprocess_audiobooks.py
```

### Notes
- Cut times are defined in `CUT_TIMES` inside `preprocess_audiobooks.py` and keyed by the **source filename stem**.
- Output sample rate is set to **48 kHz** (`SAMPLE_RATE = 48000`).
- The generated `bip.wav` is a sine tone cue (frequency/duration/volume configurable in the script).

## Dependencies

At minimum:
- Python 3.x
- `pandas`
- Audio stack used by `utils.audio_helpers` (commonly: `pydub`, `ffmpeg`, and any source-separation dependency if vocal isolation is enabled)

If you get decoding errors, ensure `ffmpeg` is installed and available on PATH.

## Reproducibility

- The current script uses fixed relative paths and writes deterministic output filenames (`audio01.wav`, `audio02.wav`, ...).
- For portability, consider parameterizing paths via CLI args or a config file (not yet implemented here).

## License / data

This repo may depend on external audio/questionnaire data that is not included. Ensure you have the rights to use any audio content you process.
