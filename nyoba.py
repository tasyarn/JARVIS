
import pygame
import speech_recognition as srec
from gtts import gTTS
from pygame import mixer
import wikipediaapi
import pywhatkit as kit

# Initialize APIs
mixer.init()
RECORDING_PATH = "audio/recording.wav"

def speech_to_text():
    recognizer = srec.Recognizer()
    with srec.Microphone() as source:
        print('Mendengarkan...')
        audio = recognizer.listen(source, phrase_time_limit=5)
        try:
            print('Selesai mendengarkan...')
            text = recognizer.recognize_google(audio, language='id-ID')
            print(f'Pengguna mengatakan: {text}')
            return text
        except srec.UnknownValueError:
            print('Google Speech Recognition tidak dapat memahami audio.')
            return None
        except srec.RequestError as e:
            print(f'RequestError dari Google Speech Recognition: {e}')
            return None

def get_wikipedia_info(query: str):
    """Mengambil informasi dari Wikipedia berdasarkan kueri yang diberikan."""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    wiki_wiki = wikipediaapi.Wikipedia('id', headers=headers)
    page_py = wiki_wiki.page(query)
    if page_py.exists():
        return page_py.summary[:300]  # Sesuaikan panjang ringkasan sesuai kebutuhan
    else:
        return "Tidak ada informasi yang ditemukan di Wikipedia."

def text_to_speech(text, output_path="audio/response.wav"):
    """Mengonversi teks menjadi ucapan menggunakan gTTS."""
    tts = gTTS(text=text, lang='id', slow=False)
    tts.save(output_path)

def main():
    while True:
        # Merekam audio
        user_input = speech_to_text()

        if user_input:
            # Menghentikan program jika mendeteksi perintah "terima kasih"
            if "terima kasih" in user_input.lower():
                print("Program dihentikan.")
                break

            # Memberikan jawaban jika ditanya "siapa"
            if "nama kamu siapa" in user_input.lower():
                response = "Saya Soro Sound of Robot, Artificial Intelligent yang berbasis voice recognition untuk mencari informasi yang ada di tokopedia"
                text_to_speech(response)
                audio_response_path = "audio/response.wav"
                sound = mixer.Sound(audio_response_path)
                sound.play()
                pygame.time.wait(int(sound.get_length() * 1000))
                continue

            # Mencari informasi tentang topik tertentu
            elif "cari tentang" in user_input.lower():
                topik = user_input.lower().replace("cari tentang", "").strip()
                kit.search(topik)
                text_to_speech(f"Mencari informasi tentang {topik}")
                audio_response_path = "audio/response.wav"
                sound = mixer.Sound(audio_response_path)
                sound.play()
                pygame.time.wait(int(sound.get_length() * 1000))
                continue

            # Membuka website tertentu
            elif "buka website" in user_input.lower():
                website = user_input.lower().replace("buka website", "").strip()
                kit.search(website)
                text_to_speech(f"Membuka website {website}")
                audio_response_path = "audio/response.wav"
                sound = mixer.Sound(audio_response_path)
                sound.play()
                pygame.time.wait(int(sound.get_length() * 1000))
                continue

            # Mendapatkan informasi dari Wikipedia
            wikipedia_info = get_wikipedia_info(user_input)

            # Mengonversi respons Wikipedia menjadi audio menggunakan gTTS
            text_to_speech(wikipedia_info)
            audio_response_path = "audio/response.wav"

            # Memutar respons audio dari gTTS
            print("Berbicara...")
            sound = mixer.Sound(audio_response_path)
            sound.play()
            pygame.time.wait(int(sound.get_length() * 1000))

if __name__ == "__main__":
    main()
