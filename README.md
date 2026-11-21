# Python Text-to-Speech

A small command-line program that turns a UTF-8 text file into one MP3 using Google Text-to-Speech or Microsoft Edge neural voices.

It includes English and French phrase lists. The program reads the whole selected file and generates one audio file. It needs an internet connection while generating speech.

## Requirements

- Python 3.8 or newer
- Internet access while creating speech
- `ffmpeg` only when using Google TTS at a speed other than `1x`

## First-time setup on Ubuntu or Debian Linux

Open a terminal in this project directory. Install the package that lets Python create a virtual environment:

```bash
sudo apt update
sudo apt install python3-venv
```

If that command says the package is unavailable and Python reports a specific version, install the matching package instead. For example, a Python 3.14 installation uses:

```bash
sudo apt install python3.14-venv
```

Create this project's virtual environment, activate it, and install the required Python libraries:

```bash
python3 -m venv tts_env
source tts_env/bin/activate
python -m pip install -r requirements.txt
```

`(tts_env)` at the beginning of the terminal prompt means the environment is active. Run all following `python` commands while it is active.

To use Google TTS at a speed other than `1x`, install ffmpeg:

```bash
sudo apt install ffmpeg
```

### Recreate the environment

If `tts_env` was copied or moved from a different folder, recreate it. This deletes only the installed Python libraries in `tts_env`; it does not delete your text files or MP3 files.

```bash
deactivate
rm -r tts_env
python3 -m venv tts_env
source tts_env/bin/activate
python -m pip install -r requirements.txt
```

If `deactivate` says it is not found, skip that line and run the rest of the commands.

## Usage

Run the program from the project directory. Put the input text filename directly after `text_to_speech.py`; the program uses the same filename with `.mp3` as the output. For example, `my_french_text.txt` creates `my_french_text.mp3`.

### Google TTS: French

```bash
python text_to_speech.py --lang fr
```

This reads `phrases_fr.txt` and creates `phrases_fr.mp3`.

### Google TTS: English

```bash
python text_to_speech.py --lang en
```

This reads `phrases_en.txt` and creates `phrases_en.mp3`.

### Microsoft Edge neural voices

Use `--engine edge` for more natural-sounding online voices. The script selects a suitable default voice for English and French; it does not need `ffmpeg`, including when you use `--speed`.

```bash
# French: fr-FR-DeniseNeural
python text_to_speech.py --engine edge --lang fr

# English: en-US-AriaNeural
python text_to_speech.py --engine edge --lang en
```

Select another Microsoft voice with `--voice`:

```bash
python text_to_speech.py --engine edge --lang fr --voice fr-FR-HenriNeural
```

For a French male voice, this full command reads `phrases_fr.txt` and saves the result as `lesson_audio.mp3`:

```bash
python text_to_speech.py phrases_fr.txt --engine edge --lang fr --voice fr-FR-HenriNeural --output lesson_audio.mp3
```

For an English male voice, use `en-US-GuyNeural`:

```bash
python text_to_speech.py phrases_en.txt --engine edge --lang en --voice en-US-GuyNeural
```

View every available Edge voice with:

```bash
edge-tts --list-voices
```

### Choose an input file

```bash
python text_to_speech.py my_text.txt --engine edge --lang fr
```

This reads `my_text.txt` and creates `my_text.mp3`. The input file must be saved as UTF-8. The language value is a gTTS language code, such as `fr` for French or `en` for English.

To choose a different MP3 filename, use `--output`:

```bash
python text_to_speech.py my_text.txt --engine edge --lang fr --output french_audio.mp3
```

### Audio speed

Use `--speed` to set the playback rate. The supported range is `0.5` to `2.0`:

```bash
python text_to_speech.py --lang en --speed 1.0
python text_to_speech.py --lang en --speed 1.5
python text_to_speech.py --lang en --speed 2.0
```

`1.0` is normal speed, `1.5` is 50% faster, and `2.0` is twice as fast. With Google TTS, `--speed` values other than `1.0` require `ffmpeg`. Microsoft Edge TTS changes its speaking rate directly, so it does not need `ffmpeg`.

The `--slow` option asks gTTS to generate its slower speech option:

```bash
python text_to_speech.py --lang fr --slow
```

You can combine it with `--speed`; gTTS generates the slower version first, then ffmpeg applies the selected multiplier. Leave `--slow` off for normal gTTS speech.

## All options

```text
input_file      Optional input text filename; default output has the same name with .mp3
--input, -i     Alternative way to provide the input text filename
--output, -o    MP3 output path; default uses the input filename with .mp3
--lang, -l     gTTS language code (default: fr)
--engine        Speech engine: gtts (Google) or edge (Microsoft neural voices)
--voice          Microsoft Edge voice, used only with --engine edge
--speed        Playback rate from 0.5 to 2.0 (default: 1.0)
--slow         Use gTTS's slower speech option
```

Show the built-in help with:

```bash
python text_to_speech.py --help
```

## Uninstall

The project folder includes a local virtual environment named `tts_env`. To remove all Python packages installed in that environment, first deactivate it if it is active, then delete the environment folder.

On Linux or macOS:

```bash
# If tts_env is active, run: deactivate
rm -r tts_env
```

On Windows PowerShell:

```powershell
# If tts_env is active, run: deactivate
Remove-Item -Recurse -Force .\tts_env
```

Deleting the virtual environment removes its installed Python packages. It does not delete the project files or generated audio, and it does not uninstall `ffmpeg` if you installed that separately. If you only want to uninstall gTTS while keeping the environment, run `python -m pip uninstall gTTS` while that environment is active; packages that gTTS depends on may remain installed.

## Notes

- Generated audio is ignored by Git so large MP3 files are not accidentally committed. Generate it again locally when needed.
- Speech quality and supported languages depend on gTTS and Google's online text-to-speech service.
