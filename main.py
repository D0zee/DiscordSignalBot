import discord
from bs4 import BeautifulSoup
from scrapingant_client import ScrapingAntClient
from html.parser import HTMLParser
import time

client = discord.Client()
last_is_printed = False

image = "None_"


class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        global last_is_printed
        if tag == "img":
            for name, value in attrs:
                if name == "src" and value[0:12] == "https://test" and not last_is_printed:
                    global image
                    image = value
                    last_is_printed = True


def solve():
    global result_text
    global image
    url = "https://www.launchmynft.io/collections/3p26iJMi3azuxQyrDWwziQ4y6uM4grbVtmgL33CohDwu/wIXhZYviMOG8Fg8LZRcK"

    parser_image = ScrapingAntClient(token='670e6757c7a14a70953c07a6b4611a24')

    page_content = parser_image.general_request(url).content

    parser = MyHTMLParser()
    parser.feed(page_content)

    soup = BeautifulSoup(page_content, "html.parser")
    st = soup.findAll("span")
    last_is_printed_text = False
    for i in st:
        if (i.get_text()[:2] == "2D") and not last_is_printed_text:
            result_text = i.get_text()
            last_is_printed_text = True
    return [result_text, image]


delay = 60
text_from_bot = "last nft was minted:"


@client.event
async def on_message(message):
    global text_from_bot

    if message.content.startswith('!change_text'):
        text_from_bot = message.content[13:]

    if message.content.startswith('!run'):
        global last_text
        last_text = ""
        while True:
            result = solve()
            # print(result[0], result[1])
            if last_text == "" or (result[0] != last_text):
                last_text = result[0]
                await message.channel.send(text_from_bot)
                await message.channel.send(result[0])
                await message.channel.send(result[1])
            time.sleep(delay)


client.run("Token")
