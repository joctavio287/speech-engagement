import matplotlib.pyplot as plt
from pathlib import Path
from typing import Union
import matplotlib
import numpy as np
import subprocess
import random
import shutil

from pydub.generators import Sine
from pydub import AudioSegment
from scipy.io import wavfile
from scipy import signal
from gtts import gTTS
import ffmpeg

# Use non-interactive backend for server environments
matplotlib.use('Agg')  

def read_wav(
    file_path: Union[str, Path],
    return_sample_rate: bool = False
) -> Union[np.ndarray, tuple[int, np.ndarray]]:
    """
    Reads a WAV file and returns it as an array.
    
    Parameters
    ----------
        file_path: Union[str, Path]
            Path to the WAV file
        return_sample_rate: bool
            If True, returns a tuple (sample_rate, data)
    
    Returns
    -------
        np.ndarray or tuple[int, np.ndarray]: Audio data as a numpy array,
            or (sample_rate, data) if return_sample_rate is True
    """
    sample_rate, data = wavfile.read(file_path)
    if return_sample_rate:
        return sample_rate, data
    else:
        return data

def plot_audio_profile(
    audio_path: Union[str, Path],
    output_path: Union[str, Path, None] = None,
    attack_threshold: float = 0.1,
    plot_spectrum: bool = False,
    verbose: bool = False
) -> dict:
    """
    Plots the audio profile showing waveform, envelope, and attack characteristics.
    Useful for verifying that the attack is fast and clear.

    Parameters
    ----------
    audio_path : Union[str, Path]
        Path to the audio file to analyze.
    output_path : Union[str, Path, None], optional
        Path to save the plot image. If None, saves next to audio file.
    attack_threshold : float, optional
        Threshold (fraction of peak) to calculate attack time. Default is 0.1 (10%).
    plot_spectrum : bool, optional
        If True, adds a spectrogram plot to visualize formants. Default is False.
    verbose : bool, optional
        If True, prints detailed attack metrics. Default is False.

    Returns
    -------
    dict
        Dictionary with attack metrics:
            - attack_time_ms: Time from threshold to peak in milliseconds
            - peak_time_ms: Time to peak amplitude in milliseconds
            - peak_amplitude: Normalized peak amplitude
            - is_fast_attack: True if attack_time < 20ms (quick onset)
    """
    sample_rate, data = wavfile.read(audio_path)
    
    # Normalize data
    data = data.astype(np.float32)
    max_val = np.max(np.abs(data))
    if max_val == 0:
        # Audio is silent - return early with default metrics
        return {
            'attack_time_ms': 0.0,
            'peak_time_ms': 0.0,
            'peak_amplitude': 0.0,
            'is_fast_attack': True  # Silent audio has no attack delay
        }
    data_normalized = data / max_val
    
    # Calculate envelope using Hilbert transform
    analytic_signal = signal.hilbert(data_normalized)
    envelope = np.abs(analytic_signal)
    
    # Smooth envelope for clearer visualization
    window_size = max(1, int(sample_rate * 0.001))  # 1ms window
    envelope_smooth = np.convolve(envelope, np.ones(window_size)/window_size, mode='same')
    
    # Time axis in milliseconds
    time_ms = np.arange(len(data)) / sample_rate * 1000
    
    # Find last sample with amplitude > 1%
    silence_thresh = 0.01
    active_mask = np.abs(data_normalized) > silence_thresh*np.abs(data_normalized).max()
    if np.any(active_mask):
        first_active_idx = np.where(active_mask)[0][0]
        last_active_idx = np.where(active_mask)[0][-1]
        # Add 20ms buffer for context
        plot_end_idx = min(len(data), last_active_idx + int(0.02 * sample_rate))
        plot_duration_ms = plot_end_idx / sample_rate * 1000
        plot_start_idx = max(0, first_active_idx-int(0.02 * sample_rate))
        plot_start_ms = plot_start_idx / sample_rate * 1000
    else:
        plot_duration_ms = time_ms[-1]
    
    # Find attack characteristics
    peak_idx = np.argmax(np.abs(data_normalized))
    peak_time_ms = peak_idx / sample_rate * 1000
    peak_amplitude = np.max(np.abs(data_normalized))
    
    # Find when signal first crosses threshold (attack start)
    threshold_value = attack_threshold * peak_amplitude
    above_threshold = np.abs(data_normalized) >= threshold_value
    if np.any(above_threshold):
        attack_start_idx = np.argmax(above_threshold)
        attack_time_ms = (peak_idx - attack_start_idx) / sample_rate * 1000
    else:
        attack_start_idx = 0
        attack_time_ms = peak_time_ms
    
    # Determine if attack is "fast" (under 20ms is typical for clear onset)
    is_fast_attack = attack_time_ms < 20
    
    # Create the plot
    nrows = 3 if plot_spectrum else 2
    fig, axes = plt.subplots(nrows, 1, figsize=(12, 8))
    
    # Plot 1: Waveform with envelope
    ax1 = axes[0]
    ax1.plot(time_ms, data_normalized, 'b-', alpha=0.5, label='Waveform', linewidth=0.5)
    ax1.plot(time_ms, envelope_smooth, 'r-', label='Envelope', linewidth=1.5)
    ax1.axvline(x=peak_time_ms, color='g', linestyle='--', label=f'Peak ({peak_time_ms:.2f}ms)')
    ax1.axhline(y=threshold_value, color='orange', linestyle=':', 
                label=f'{attack_threshold*100:.0f}% threshold')
    if attack_start_idx < peak_idx:
        ax1.axvline(x=attack_start_idx / sample_rate * 1000, color='purple', 
                    linestyle='--', alpha=0.7, label=f'Attack start')
    ax1.set_xlim(plot_start_ms, plot_duration_ms)
    ax1.set_xlabel('Time (ms)')
    ax1.set_ylabel('Normalized Amplitude')
    ax1.set_title('Audio Profile: Waveform and Envelope')
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Zoomed attack region (first 50ms or to peak + 10ms)
    ax2 = axes[1]
    zoom_end = min(len(time_ms) - 1, int((peak_time_ms + 10) * sample_rate / 1000))
    zoom_end = max(zoom_end, int(0.05 * sample_rate))  # At least 50ms
    ax2.plot(time_ms[:zoom_end], data_normalized[:zoom_end], 'b-', alpha=0.5, 
             label='Waveform', linewidth=0.5)
    ax2.plot(time_ms[:zoom_end], envelope_smooth[:zoom_end], 'r-', 
             label='Envelope', linewidth=1.5)
    ax2.axvline(x=peak_time_ms, color='g', linestyle='--', label=f'Peak')
    ax2.axhline(y=threshold_value, color='orange', linestyle=':', 
                label=f'{attack_threshold*100:.0f}% threshold')
    if attack_start_idx < peak_idx and attack_start_idx < zoom_end:
        ax2.axvline(x=attack_start_idx / sample_rate * 1000, color='purple', 
                    linestyle='--', alpha=0.7, label='Attack start')
    ax2.set_xlabel('Time (ms)')
    ax2.set_ylabel('Normalized Amplitude')
    ax2.set_title(f'Attack time: {attack_time_ms:.2f}ms')
    ax2.legend(loc='upper right')
    ax2.grid(True, alpha=0.3)
    
    if plot_spectrum:
        ax3 = axes[2]
        Pxx, freqs, bins, im = ax3.specgram(
            data_normalized + np.random.randn(len(data_normalized)) * 1e-10,  # avoid log(0)
            NFFT=1024, 
            Fs=sample_rate, 
            noverlap=512, 
            cmap='inferno'
        )
        ax3.set_ylabel('Frequency (Hz)')
        ax3.set_xlabel('Time (s)')
        ax3.set_title('Formants')
        ax3.set_ylim(0, 8000) # Limit to relevant speech frequencies
        ax3.set_xlim(plot_start_ms / 1000, plot_duration_ms / 1000)
        fig.colorbar(im, ax=ax3, label='Intensity (dB)')

    plt.tight_layout()
    
    # Save the plot
    if output_path is None:
        output_path = Path(audio_path).with_suffix('.png')
    else:
        output_path = Path(output_path)
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    
    metrics = {
        'attack_time_ms': attack_time_ms,
        'peak_time_ms': peak_time_ms,
        'peak_amplitude': float(peak_amplitude),
        'is_fast_attack': is_fast_attack
    }
    if verbose:
        print(f"Attention probe attack analysis:")
        print(f"  - Attack time: {metrics['attack_time_ms']:.2f}ms")
        print(f"  - Peak time: {metrics['peak_time_ms']:.2f}ms")
        print(f"  - Fast attack: {'Yes ✓' if metrics['is_fast_attack'] else 'No ✗'}")
        print(f"  - Profile saved to: {output_path}")
    return metrics
    
def save_wav(
    file_path: Union[str, Path],
    sample_rate: int,
    data: np.ndarray
) -> None:
    """
    Saves a numpy array as a WAV file.
    
    Parameters
    ----------
        file_path: Union[str, Path]
            Path to save the WAV file
        sample_rate: int
            Sample rate of the audio
        data: np.ndarray
            Audio data as a numpy array
    
    Returns
    -------
        None
    """
    wavfile.write(file_path, sample_rate, data)
    
def get_sample_rate(
    file_path: Union[str, Path]
) -> int:
    """
    Get sample rate of a WAV file
    
    Parameters
    ----------
        file_path (str or Path): Path to the WAV file
    
    Returns
    -------
        int: Sample rate of the WAV file
        
    """
    return wavfile.read(file_path)[0]

def resample_audio(
    input_file: Union[str, Path], 
    output_file: Union[str, Path], 
    target_sample_rate: int = 48000
) -> None:
    """
    Resamples an audio file to a target sample rate.
    
    Parameters
    ----------
        input_file : Union[str, Path]
            Path to the input audio file.
        output_file : Union[str, Path]
            Path to save the resampled audio file.
        target_sample_rate : int
            Desired sample rate in Hz.
    
    Returns
    -------
        None
    """
    audio = AudioSegment.from_file(input_file)
    audio = audio.set_frame_rate(target_sample_rate)
    audio.export(output_file, format='wav')

def convert_to_wav(
    input_file: Union[str, Path], 
    output_file: Union[str, Path],
    start_time: Union[float, None] = None, 
    end_time: Union[float, None] = None, 
    stereo: bool = False,
    exists_ok: bool = True,
    verbose: bool = False
) -> None:
    """
    Converts an audio file to WAV format, optionally trimming it.

    Parameters
    ----------
    input_file : Union[str, Path]
        Path to the input audio file.
    output_file : Union[str, Path]
        Path to save the converted WAV file.
    start_time : Union[float, None], optional
        Start time in seconds to trim the audio, by default None
    end_time : Union[float, None], optional
        End time in seconds to trim the audio, by default None
    stereo : bool, optional
        If True, converts audio to stereo. Defaults to False (mono).
    exists_ok : bool, optional
        If False and output file exists, skip conversion. Defaults to True.
    
    Returns
    -------
        None
    """
    
    output_file = str(output_file)
    if not exists_ok and Path(output_file).exists():
        print(f'File {output_file} already exists. Skipping conversion.')
        return
    else:
        if verbose:
            print(f'Converting {input_file} to {output_file}...')
    kwargs = {}
    if start_time is not None:
        kwargs['ss'] = start_time
    if end_time is not None:
        kwargs['to'] = end_time
        
    assert end_time is None or start_time is None or end_time > start_time, \
        "end_time must be greater than start_time"
    (
        ffmpeg
        .input(input_file, **kwargs)
        .output(
            output_file,
            format='wav',
            acodec='pcm_s16le',  # 16-bit PCM
            ar=44100,            # 44.1 kHz
            ac=2 if stereo else 1  # stereo or mono
        )
        .overwrite_output()
        .run(quiet=not verbose, capture_stdout=not verbose, capture_stderr=not verbose)
    )

def scale_audio(
    input_file: Union[str, Path],
    output_file: Union[str, Path],
    delta_frames: int
) -> None:
    """
    Scales (time-stretches) an audio file by a given delta in seconds.

    Parameters
    ----------
    input_file : Union[str, Path]
        Path to the input audio file.
    output_file : Union[str, Path]
        Path to save the scaled audio file.
    delta_frames : int
        Number of milliseconds to stretch (positive) or compress (negative) the audio.
    
    Returns
    -------
        None
    """
    sample_rate, data = wavfile.read(input_file)
    original_frames = data.shape[0]
    original_dtype = data.dtype
    data = data.mean(axis=1)  if data.ndim != 1 else data
    target_frames = original_frames + delta_frames
    
    if delta_frames == 0:
        if input_file != output_file:
            shutil.copyfile(input_file, output_file)
        return
    else:
        data_float = data.astype(np.float32)
        original_idx = np.arange(original_frames, dtype=np.float32)
        target_idx = np.linspace(0, original_frames - 1, target_frames, dtype=np.float32)
        
        
        scaled = np.interp(target_idx, original_idx, data_float)
        
        if np.issubdtype(original_dtype, np.integer):
            dtype_info = np.iinfo(original_dtype)
            scaled = np.clip(
                np.round(scaled), dtype_info.min, dtype_info.max
            ).astype(original_dtype)
        else:
            scaled = scaled.astype(original_dtype)
        wavfile.write(output_file, sample_rate, scaled)

def calculate_energy(
    audio_data: np.ndarray
) -> float:
    """
    Calculate the energy of an audio signal.

    Parameters
    ----------
    audio_data : np.ndarray
        The input audio data.

    Returns
    -------
    float
        The energy of the audio signal in arbitrary units.
    """
    return np.sum(audio_data.astype(np.float32) ** 2) / len(audio_data)

def scale_audio_to_relative_db(
    audio_to_scale_path: Union[str, Path],
    reference_audio_path: Union[str, Path],
    target_db_diff: float
) -> None:
    """
    Scale an audio signal so that its energy is a specified dB difference
    relative to a reference audio signal. Also includes protection against
    saturation (both audios scaled down if needed).
    
    Parameters
    ----------
    audio_to_scale : Union[str, Path]
        The audio signal to be scaled.
    reference_audio : Union[str, Path]
        The reference audio signal.
    output_path : Union[str, Path]
        Path to save the scaled audio file.
    target_db_diff : float
        The desired difference in dB. 
        E.g., 20.0 will make the resulting audio 20dB louder than the reference.
        E.g., -6.0 will make the resulting audio 6dB quieter than the reference.
            
    Returns
    -------
        None
    """
    CEILING = .99

    # Calculate current energies
    sample_rate, audio_to_scale = read_wav(audio_to_scale_path, return_sample_rate=True)
    sample_rate_ref, reference_audio = read_wav(reference_audio_path, return_sample_rate=True)
    audio_to_scale = audio_to_scale.astype(np.float32)
    reference_audio = reference_audio.astype(np.float32)
    current_energy = calculate_energy(audio_to_scale)
    reference_energy = calculate_energy(reference_audio)
    
    # Validations to avoid division by zero
    if current_energy == 0 or reference_energy == 0:
        print("Warning: one of the audio signals has zero energy. Returning original audio.")

    # If target_db = 10 * log10(E_target / E_reference), then E_target / E_reference = 10^(target_db / 10)
    # Calculate the target energy
    required_ratio = 10 ** (target_db_diff / 10)
    target_energy = reference_energy * required_ratio
    
    # Calculate the scaling factor for Amplitude
    # Since Energy ~ Amplitude^2, the factor is sqrt(E_target / E_current)
    scaling_factor = np.sqrt(target_energy / current_energy)
    candidate_tgt = audio_to_scale * scaling_factor
    candidate_ref = reference_audio.copy()
    
    peak_tgt = np.max(np.abs(candidate_tgt))
    peak_ref = np.max(np.abs(candidate_ref))
    global_peak = max(peak_tgt, peak_ref)
    if global_peak > CEILING:
        correction_factor = CEILING / global_peak
        final_tgt = candidate_tgt * correction_factor
        final_ref = candidate_ref * correction_factor
    else:
        final_tgt = candidate_tgt
        final_ref = candidate_ref
    save_wav(file_path=audio_to_scale_path, sample_rate=sample_rate, data=final_tgt)
    save_wav(file_path=reference_audio_path, sample_rate=sample_rate_ref, data=final_ref)

def add_bips(
    input_file: Union[str, Path], 
    output_file: Union[str, Path], 
    num_bips: int = 5, 
    duration: float = .5,
    bip_frequency: int = 1000
) -> Union[str, Path]:
    """
    Adds bips (beeps) at the beginning and end of an audio file.

    Parameters
    ----------
    input_file : Union[str, Path]
        Path to the input audio file.
    output_file : Union[str, Path]
        Path to save the output audio file with bips.
    num_bips : int, optional
        Number of bips to add at the beginning and end, by default 5
    duration : float, optional
        Duration of each bip in seconds, by default .5
    bip_frequency : int, optional
        Frequency of the bip sound in Hz, by default 1000

    Returns
    -------
    Union[str, Path]
        Path to the output audio file with bips.
    """

    sample_rate = get_sample_rate(input_file)
    bip_segment = AudioSegment.silent(
        duration=duration * 1000, # duration in milliseconds
        frame_rate=sample_rate
    )

    # Add bips (sounds like an alarm) at the beginning and end
    for _ in range(num_bips):
        bip_segment += Sine(bip_frequency).to_audio_segment(duration=duration * 1000, volume=-20) 
        bip_segment += AudioSegment.silent(duration=duration * 1000)  # Silence between bips
    
    # Load the original audio file
    original_audio = AudioSegment.from_wav(input_file)

    # Concatenate the original audio with bips at the beginning and end
    new_audio = bip_segment + original_audio + bip_segment

    # Export the new audio file
    new_audio.export(output_file, format='wav')
    return output_file

def vocal_isolation(
    input_wav: Union[str, Path],
    output_wav: Union[str, Path], 
    vocals_only: bool = True
) -> None:
    """
    Uses Demucs to isolate vocals from a WAV file.
    Requires Demucs installed: pip install demucs
    
    Parameters
    ----------
        input_wav : Union[str, Path]
            Path to input WAV file.
        output_wav : Union[str, Path]
            Path to output WAV file.
        vocals_only : bool
            If True, saves only vocals. If False, saves accompaniment.
    
    Returns
    -------
        None
    """
    TEMP_DIR = "demucs_output"
    # Run Demucs (default model separates vocals, drums, bass, other)
    subprocess.run([
        "demucs",
        "--two-stems", "vocals" if vocals_only else "accompaniment",
        "-o", TEMP_DIR,
        input_wav
    ], check=True)

    # Demucs saves output as TEMP_DIR/htdemucs/input_wav_basename/vocals.wav or accompaniment.wav
    base = Path(input_wav).stem
    stem = "vocals" if vocals_only else "accompaniment"
    stem_path = Path(TEMP_DIR) / "htdemucs" / base / f"{stem}.wav"

    shutil.copy(stem_path, output_wav)
    shutil.rmtree(TEMP_DIR, ignore_errors=True)

def combine_audio_stereo(
    audio_left: Union[str, Path],
    audio_right: Union[str, Path],
    output_file: Union[str, Path]
) -> None:
    """
    Combines two mono audio files into a single stereo audio file.
    
    Parameters
    ----------
        audio_left : Union[str, Path]
            Path to the left channel audio file.
        audio_right : Union[str, Path]
            Path to the right channel audio file.
        output_file : Union[str, Path]
            Path to save the combined stereo audio file.
    
    Returns
    -------
        None
    """
    left = AudioSegment.from_file(audio_left).set_channels(1)
    right = AudioSegment.from_file(audio_right).set_channels(1)
        
    stereo_audio = AudioSegment.from_mono_audiosegments(
        left, 
        right
    )
    stereo_audio.export(output_file, format='wav')

def get_antialiasing_filter(
    original_sr: int, 
    target_sr: int, 
    cutoff_ratio: float=0.9, 
    gstop_db: float=53
)->np.ndarray:
    """
    Calculate FIR filter coefficients for anti-aliasing before downsampling.

    Parameters
    ----------
    original_sr: int
        Original sampling rate in Hz (e.g., 16000)
    target_sr: int
        Target sampling rate in Hz (e.g., 128)
    cutoff_ratio: float
        What percentage of the target Nyquist frequency to preserve.
            0.90 is safer for TRF than 0.99 (less ringing).
    gstop_db: float
        The stopband attenuation in dB.

    Returns
    -------
    np.ndarray
        The FIR filter coefficients.
    """
    nyquist_target = target_sr / 2.0
    f_pass = nyquist_target * cutoff_ratio
    f_stop = nyquist_target
    transition_width = f_stop - f_pass
    
    # Kaiser window is specifically defined for controlling ripple and transition width
    # Desire attenuation (ripple)
    # Upper bound for the deviation (in dB) of the magnitude of the filter's frequency response from that of the desired filter (not including frequencies in any transition intervals). That is, if w is the frequency expressed as a fraction of the Nyquist frequency, A(w) is the actual frequency response of the filter and D(w) is the desired frequency response, the design requirement is that:
    #         abs(A(w) - D(w))) < 10**(-ripple/20)
    # for 0 <= w <= 1 and w not in a transition interval.
    numtaps, beta = signal.kaiserord(
        ripple=gstop_db, # 
        width=transition_width / (0.5 * original_sr)
    )
    if numtaps % 2 == 0: numtaps += 1
    taps = signal.firwin(
        numtaps=numtaps, 
        cutoff=f_pass, 
        window=('kaiser', beta), 
        fs=original_sr
    )
    return taps

def custom_resample(
    array:np.ndarray, 
    original_sr:int, 
    target_sr:int,
    padtype:str='mean',
    axis:int=0
) -> np.ndarray:
    """
    Resample an array from original_sr to target_sr using polyphase filtering.
    
    Parameters
    ----------
    array : np.ndarray
        The input array to be resampled.
    original_sr : int
        The original sampling rate of the array.
    target_sr : int
        The target sampling rate for the resampled array.
    padtype : str, optional
        The type of padding to use. Default is 'mean'.
    axis : int, optional
        The axis along which to resample. Default is 0.
    
    Returns
    -------
    np.ndarray
        The resampled array.
    """
    # Calculate upsampling and downsampling factors by finding greatest common divisor
    gcd = np.gcd(int(original_sr), int(target_sr))
    up = int(target_sr // gcd)
    down = int(original_sr // gcd)
    
    if up == 1:
        window_param = taps = get_antialiasing_filter(
            original_sr=original_sr, 
            target_sr=target_sr,
            cutoff_ratio=0.9,
            gstop_db=53
        )
    else:
        window_param = ('kaiser', 5.0) 

    return signal.resample_poly(
        x=array, 
        up=up, 
        down=down, 
        axis=axis, 
        window=window_param, 
        padtype=padtype
    )

def create_attention_probe( # TODO tidy up
    output_attention_probe_path: Union[str, Path],
    duration_seconds: Union[float, None] = 0.1,
    stimulus_type: Union[str, int] = "VA",
    sr: int = 44100
) -> Path:
    """
    Creates an attention probe audio file (beep sound) using gTTS.
    
    Parameters
    ----------
    output_attention_probe_path : Union[str, Path]
        Path to save the generated attention probe audio file.
    duration_seconds : Union[float, None], optional
        Duration of the attention probe in seconds. Default is 0.1 seconds.
    stimulus_type : Union[str, None], optional
        Text to be converted to speech for the probe (if string). If integer, it represents a tone frequency in Hz. Default is "VA".
    sr : int, optional
        Sample rate of the generated audio file. Default is 44100 Hz.
    
    Returns
    -------
    Path
        Path to the generated attention probe audio file.
    """
    if isinstance(stimulus_type, str):
        tts = gTTS(text=stimulus_type, lang='es', slow=False)
        temp_mp3_path = Path(output_attention_probe_path).with_suffix('.mp3')
        tts.save(str(temp_mp3_path))
        convert_to_wav(
            input_file=temp_mp3_path,
            output_file=output_attention_probe_path,
            stereo=False,
            exists_ok=True
        )
        Path(temp_mp3_path).unlink(missing_ok=True)
        
        sr_data, data = wavfile.read(output_attention_probe_path)
        if duration_seconds is None:
            duration_seconds = len(data) / sr_data
            sr = sr_data
            print(f"Info: duration_seconds was None, set to {duration_seconds:.3f}s based on audio length. Also setting sr to {sr_data}Hz.")
        FADE_OUT_DURATION = 0.1 * duration_seconds 
        data = data.astype(np.float32)
        data_max = np.abs(data).max()
        data /= data_max
        
        peak_idx = np.argmax(np.abs(data))
        pre_peak_buffer_sec = 0.05  # 50ms antes del pico para agarrar la 'b'
        pre_peak_samples = int(pre_peak_buffer_sec * sr_data)
        start_idx = max(0, peak_idx - pre_peak_samples)
        target_samples_orig = int(duration_seconds * sr_data)
        end_idx = start_idx + target_samples_orig
        if end_idx > len(data):
            diff = end_idx - len(data)
            start_idx = max(0, start_idx - diff)
            end_idx = len(data)
        new_data = data[start_idx : end_idx]
        if len(new_data) < target_samples_orig:
            padding = np.zeros(target_samples_orig - len(new_data), dtype=np.float32)
            new_data = np.concatenate((new_data, padding))
        if len(new_data) > target_samples_orig:
            fade_samples = int(FADE_OUT_DURATION * sr_data)
            if fade_samples > 0:
                fade_curve = np.linspace(1.0, 0.0, fade_samples)
                new_data[-fade_samples:] *= fade_curve
        
        if sr_data != sr:
            num_samples_target = int(duration_seconds * sr)
            new_data = signal.resample(new_data, num_samples_target)
        wavfile.write(output_attention_probe_path, sr, (new_data * 32767).astype(np.int16))
        return Path(output_attention_probe_path)
    elif isinstance(stimulus_type, int):
        # Make tone beep
        bip_segment = AudioSegment.silent(
            duration=duration_seconds * 1000, # duration in milliseconds
            frame_rate=sr
        )
        bip_segment += Sine(1000).to_audio_segment(duration=duration_seconds * 1000, volume=-20) 
        bip_segment.export(output_attention_probe_path, format='wav')
        return Path(output_attention_probe_path)
    else:
        raise ValueError("stimulus_type must be either str or int.")
        

def scramble_audio(
    input_file: Union[str, Path],
    output_file: Union[str, Path],
    number_of_segments: int = 10,
) -> None:
    """
    Scrambles an audio file by dividing it into segments and shuffling them.

    Parameters
    ----------
    input_file : Union[str, Path]
        Path to the input audio file.
    output_file : Union[str, Path]
        Path to save the scrambled audio file.
    number_of_segments : int, optional
        Number of segments to divide the audio into before shuffling. Default is 10.
    
    Returns
    -------
        None
    """
    sample_rate, data = wavfile.read(input_file)
    segment_samples = data.shape[0] // number_of_segments
    
    segments = []
    for start in range(0, data.shape[0], segment_samples):
        end = min(start + segment_samples, data.shape[0])
        segments.append(data[start:end])
    random.shuffle(segments)
    scrambled_data = np.concatenate(segments)
    wavfile.write(output_file, sample_rate, scrambled_data)

def create_attention_track(
    duration_samples: int, 
    sr: int, 
    probe_audio_path: Union[str, Path]
) -> tuple[int, np.ndarray, np.ndarray]:
    """
    Generates left and right audio tracks with randomly placed attention probes (beeps).
    Follows parameters inspired by Sanders, L. D., Stevens, C., Coch, D., & Neville, H. J. (2006). 
    Selective auditory attention in 3-to 5-year-old children: An event-related potential study. 
    Neuropsychologia, 44(11), 2126-2138.
    
    Parameters
    ----------
    duration_samples : int
        Total duration of the audio tracks in samples.
    sr : int
        Sample rate of the audio tracks in Hz.
    probe_audio_path : Union[str, Path]
        Path to the probe audio file (beep sound).
        
    Returns
    -------
    tuple[int, np.ndarray, np.ndarray]
        A tuple containing:
            - Number of probes per channel (int)
            - Left audio track with probes (np.ndarray)
            - Right audio track with probes (np.ndarray)
    """
    # Sanders original parameters
    DELAY_SECONDS = 3.0  # initial delay before first probe
    ISI_OPTIONS = [0.2, 0.5, 1.0] # interstimulus intervals in seconds

    # Create empty arrays for left and right tracks
    track_l = np.zeros(duration_samples, dtype=np.float32)
    track_r = np.zeros(duration_samples, dtype=np.float32)
    
    # Load or generate the beep (If no file, generate a 100ms tone)
    sr_probe, probe_wav = wavfile.read(probe_audio_path)
    if sr_probe != sr:
        probe_wav = custom_resample(
            array=probe_wav, 
            original_sr=sr_probe, 
            target_sr=sr,
            padtype='mean',
            axis=0
        )
    probe_len = len(probe_wav)
    probe_duration = probe_len / sr
    
    # Estimate the even number of probes that can fit in the available time
    available_seconds = (duration_samples / sr) - DELAY_SECONDS
    avg_event_duration = probe_duration
    avg_event_duration += (sum(ISI_OPTIONS)/len(ISI_OPTIONS))
    n_probes = int(available_seconds / avg_event_duration)
    n_probes -= 1 if n_probes % 2 != 0 else 0  
    
    # Randomly assign probes to left or right channels
    sides = ['left'] * (n_probes // 2) + ['right'] * (n_probes // 2)
    random.shuffle(sides)
    
    # Random ISIs
    isis = [random.choice(ISI_OPTIONS) for _ in range(n_probes)]
    
    current_sample = int(DELAY_SECONDS * sr)
    idxs_l = []
    idxs_r = []
    for i in range(n_probes):
        if current_sample + probe_len >= duration_samples:
            break
        if sides[i] == 'left':
            track_l[current_sample:current_sample+probe_len] += probe_wav
            idxs_l.append(current_sample)
        else:
            track_r[current_sample:current_sample+probe_len] += probe_wav
            idxs_r.append(current_sample)
        # The ISI comes AFTER the current beep
        isi_samples = int(isis[i] * sr)
        current_sample += probe_len + isi_samples
    
    # Verify that both tracks have the same number of probes, else set 0 the ending probes of the longer one
    while len(idxs_l) != len(idxs_r):
        if len(idxs_l) > len(idxs_r):
            last_pos = idxs_l.pop() 
            track_l[last_pos : last_pos + probe_len] = 0 
        else:
            last_pos = idxs_r.pop()
            track_r[last_pos : last_pos + probe_len] = 0
    return n_probes//2, track_l, track_r