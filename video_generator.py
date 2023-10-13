from PIL import Image
import subprocess
from pydub import AudioSegment
from pydub.playback import play
from pysndfx import AudioEffectsChain
import cv2
import numpy as np

from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont

####################################################################################################
# Обрезка изображения
####################################################################################################

# Открываем изображение
image = Image.open("background.jpg")

# Задаем желаемое соотношение сторон (9:16)
desired_aspect_ratio = 9 / 16

# Рассчитываем новые размеры и координаты для обрезки
width, height = image.size
new_width = int(min(width, height * desired_aspect_ratio))
new_height = int(min(height, width / desired_aspect_ratio))
left = (width - new_width) / 2
top = (height - new_height) / 2
right = left + new_width
bottom = top + new_height

# Обрезаем изображение и сохраняем
cropped_image = image.crop((left, top, right, bottom))
cropped_image.save("background_cropped.jpg")

####################################################################################################
# Объединение аудио голоса с фоновой музыкой
####################################################################################################

# Загрузка аудиофайлов
voice = AudioSegment.from_wav("voice.wav")
background = AudioSegment.from_mp3("background.mp3")

# Выравнивание продолжительности
voice_duration = len(voice)
background = background[:voice_duration]

# Уменьшение громкости фонового аудио
background = background - 20  # Уменьшаем громкость фонового аудио

# Смешивание аудио
final_audio = voice.overlay(background)

# Сохранение результата
final_audio.export("voice_with_background.wav", format="wav")


####################################################################################################
# Объединение фонового изображения с голос с фоновой музыкой
####################################################################################################

# Укажите путь к вашей картинке и аудиозаписи
image_path = "background_cropped.jpg"
audio_path = "voice_with_background.wav"
output_video_path = "output_video_without_text.mp4"

# Команда FFmpeg для создания видео
ffmpeg_cmd = [
    "ffmpeg",
    "-loop",
    "1",  # Зациклить изображение
    "-i",
    image_path,  # Входное изображение
    "-i",
    audio_path,  # Входное аудио
    "-c:v",
    "libx264",  # Кодек видео
    "-tune",
    "stillimage",  # Оптимизация для изображения
    "-c:a",
    "aac",  # Кодек аудио
    "-strict",
    "experimental",  # Поддержка AAC
    "-b:a",
    "192k",  # Битрейт аудио
    "-shortest",  # Сделать видео длиной аудиозаписи
    output_video_path,  # Выходное видео
]

# Вызов команды FFmpeg
subprocess.run(ffmpeg_cmd, check=True)

print(f"Видео успешно создано: {output_video_path}")

####################################################################################################
# Добавление текста на видео
####################################################################################################

import os
import textwrap

# Чтение текста из файла
with open("citation.txt", "r") as file:
    text = file.read()

# Чтение имени автора из файла
with open("author.txt", "r") as file:
    author = file.read()

# Разбиение текста на строки по 40 символов
lines = textwrap.wrap(text, width=35)

# Добавление подписи автора под цитатой
lines.append("\n" + author)

# Объединение строк с переносом строки
text = "\n".join(lines)

# Путь к файлу шрифта
fontfile = "arial.ttf"

# Команда FFmpeg для добавления текста на видео
command = f"ffmpeg -i output_video_without_text.mp4 -vf \"drawtext=fontfile={fontfile}: text='{text}': x=(w-text_w)/2: y=(h-text_h)/2: fontsize=30: fontcolor=white: borderw=3: bordercolor=black\" output_video_with_text.mp4"

# Выполнение команды
os.system(command)
