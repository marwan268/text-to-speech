# Python Text-to-Speech

A small command-line program that turns a UTF-8 text file into one MP3 using [gTTS](https://pypi.org/project/gTTS/) (Google Text-to-Speech).

It includes English and French phrase lists. The program reads the whole selected file and generates one audio file. It needs an internet connection while generating speech.

## Requirements

- Python 3.8 or newer
- The Python package in `requirements.txt`
- `ffmpeg` for changing the generated audio speed to anything other than `1x`

## Setup

Open a terminal in this project directory and install the Python dependency:

```bash
python -m pip install -r requirements.txt
```

On Windows, use `py -m pip install -r requirements.txt` if `python` is not the Python launcher on your system.

To use speeds other than `1x`, install `ffmpeg` and make sure the `ffmpeg` command is available in your terminal's `PATH`.

## Usage

Run the program from the project directory. If you do not provide paths, it picks `phrases_<language>.txt` as the input and writes `all_phrases_<language>.mp3`.

### French

```bash
python text_to_speech.py --lang fr
```

This reads `phrases_fr.txt` and creates `all_phrases_fr.mp3`.

### English

```bash
python text_to_speech.py --lang en
```

This reads `phrases_en.txt` and creates `all_phrases_en.mp3`.

### Choose another input or output file

```bash
python text_to_speech.py --lang fr --input my_text.txt --output french_audio.mp3
```

The input file must be saved as UTF-8. The language value is a gTTS language code, such as `fr` for French or `en` for English.

### Audio speed

Use `--speed` to set the playback rate. The supported range is `0.5` to `2.0`:

```bash
python text_to_speech.py --lang en --speed 1.0
python text_to_speech.py --lang en --speed 1.5
python text_to_speech.py --lang en --speed 2.0
```

`1.0` is normal speed, `1.5` is 50% faster, and `2.0` is twice as fast. `--speed` values other than `1.0` require `ffmpeg`.

The `--slow` option asks gTTS to generate its slower speech option:

```bash
python text_to_speech.py --lang fr --slow
```

You can combine it with `--speed`; gTTS generates the slower version first, then ffmpeg applies the selected multiplier. Leave `--slow` off for normal gTTS speech.

## All options

```text
--input, -i    UTF-8 text file (default: phrases_<lang>.txt)
--output, -o   MP3 output path (default: all_phrases_<lang>.mp3)
--lang, -l     gTTS language code (default: fr)
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
