import os
import torch

device = torch.device("cpu")
torch.set_num_threads(6)
local_file = "model.pt"

if not os.path.isfile(local_file):
    torch.hub.download_url_to_file(
        "https://models.silero.ai/models/tts/ru/v4_ru.pt", local_file
    )

model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
model.to(device)

with open("response.txt", "r") as file:
    # Читаем содержимое файла и сохраняем его в переменной
    gpt_text = file.read()

with open("citation.txt", "r") as file:
    # Читаем содержимое файла и сохраняем его в переменной
    parser_citation = file.read()

with open("author.txt", "r") as file:
    # Читаем содержимое файла и сохраняем его в переменной
    parser_author = file.read()

text = f"{parser_citation}. Автор {parser_author}. Привет! Сегодня ты узнаешь, какой смысл заложен в этой цитате. {gpt_text}. Подписывайся, чтобы больше узнать о цитатах. А сегодня ты узнал такую цитату"

sample_rate = 48000
speaker = "baya"
put_accent = True
put_yo = True

audio_paths = model.save_wav(text=text, speaker=speaker, sample_rate=sample_rate)

os.rename("test.wav", "voice.wav")

print("Аудио успешно записано.")
