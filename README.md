![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Google Gemini](https://img.shields.io/badge/google%20gemini-8E75B2?style=for-the-badge&logo=google%20gemini&logoColor=white)

# AI Assistant Overlay

AI Assistant Overlay is a professional, real-time desktop assistant for your daily productivity. It listens to your spoken questions (via microphone or system audio), sends them to Google Gemini, and displays suggested answers in a discreet, always-on-top overlay window.

## Features

- **Real-time Q&A:** Listens to your spoken questions and displays AI-generated answers instantly.
- **Professional Overlay:** Clean, borderless, semi-transparent window with modern fonts and colors.
- **Screen Share Safe:** Uses Windows APIs to hide the overlay from screen capture and screen sharing.
- **Movable & Resizable:** Drag to reposition; large, readable text for easy viewing.
- **Copy-Paste Support:** Select and copy any question or answer with right-click or keyboard shortcuts.
- **Conversation History:** Keeps track of previous Q&A for context.
- **Global Hotkey:** Instantly hide/show the overlay with `Ctrl+Shift+H`.
- **API Key Dialog:** Securely prompts for your Google Gemini API key at startup.

## Requirements

- Windows 10 or later
- Python 3.9+
- [google-genai](https://pypi.org/project/google-genai/)
- [speech_recognition](https://pypi.org/project/SpeechRecognition/)
- [pyaudio](https://pypi.org/project/PyAudio/)
- [keyboard](https://pypi.org/project/keyboard/)
- [requests](https://pypi.org/project/requests/)

Install dependencies:
```sh
pip install -r requirements.txt
```

## Setup

1. **Get a Google Gemini API Key:**  
   - Visit [Google AI Studio](https://aistudio.google.com/app/apikey) and create a free API key.

2. **Run the App:**
   ```sh
   python Assist.py
   ```
   - Paste your Gemini API key when prompted.

3. **Usage:**
   - Ask your questions aloud or use your system audio.
   - The overlay will display the transcribed question and Gemini's answer in real time.
   - Use the close button (×) or `Esc` to exit.
   - Use `Ctrl+Shift+H` to hide/show the overlay instantly.

## Tips for Best Results

- **Copy answers:**  
  Select text and right-click to copy, or use `Ctrl+C`.

## Security & Privacy

- The overlay uses Windows APIs to hide itself from screen sharing and screen capture, but this is not 100% foolproof for all software.
- Your API key is only used locally and never stored.

## Troubleshooting

- **PyAudio errors:**  
  Install with `pipwin install pyaudio` if you have trouble on Windows.
- **Overlay visible in screen share:**  
  Make sure you are on Windows 10+ and using supported screen sharing tools.
- **API errors:**  
  Double-check your Gemini API key and internet connection.

**Disclaimer:**  
This tool is for educational and personal productivity use only. Use responsibly and in accordance with your workplace policies.
