from bs4 import BeautifulSoup
import requests
import lxml
import os
import subprocess


def parser(url: str):
    res = requests.get(url=url)
    soup = BeautifulSoup(res.text, "lxml")
    image = soup.find("img").get("src")
    return image


new_image = parser("https://www.calculatormix.com/generators/random-image/")

new_image_link = f"https://www.calculatormix.com{new_image}"

print(f"Link for download image: {new_image_link}")

subprocess.run(["wget", f"{new_image_link}", "-O", "background.jpg"])
