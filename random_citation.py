from bs4 import BeautifulSoup
import requests
import lxml
import g4f
import os

# Парсинг цитаты дня с Викицитатника


def parser(url: str):
    res = requests.get(url=url)
    soup = BeautifulSoup(res.text, "lxml")
    citation = soup.find("span", class_="author").previous_sibling.text
    author = soup.find("span", class_="author").text
    return citation, author


parser_citation, parser_author = parser("https://randstuff.ru/saying/")

print(f"{parser_citation}\n{parser_author}")

with open("citation.txt", "w") as f:
    f.write(parser_citation)

with open("author.txt", "w") as f:
    f.write(parser_author)


with open("author.txt", "r") as file:
    text = file.read()

# Проверяем, есть ли тире в начале текста
if text.startswith("—"):
    # Удаляем тире
    text = text[1:]

# Записываем обновленный текст обратно в файл
with open("author.txt", "w") as file:
    file.write(text)

# Объяснение цитаты с помощью ИИ


def ask_gpt(prompt: str):
    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    with open("response.txt", "w") as f:
        for message in response:
            print(message, flush=True, end="", file=f)
    print("Ответ от ИИ успешно записан.")


if __name__ == "__main__":
    ask_gpt(
        f'Представь, что ты великий философ. Ничего лишнего не говори, просто Объясни простыми словами смысл цитаты: "{parser_citation}" автора {parser_author}'
    )
