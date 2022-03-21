from bs4 import BeautifulSoup
from scrapingant_client import ScrapingAntClient
from html.parser import HTMLParser
last_is_printed = False
class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        global last_is_printed
        if tag == "img":
            for name, value in attrs:
               # If href is defined, print it.
               if name == "src" and value[0:12] == "https://test" and not last_is_printed:
                    print (name, "=", value)
                    last_is_printed = True


url = "https://www.launchmynft.io/collections/3p26iJMi3azuxQyrDWwziQ4y6uM4grbVtmgL33CohDwu/wIXhZYviMOG8Fg8LZRcK"

client = ScrapingAntClient(token='670e6757c7a14a70953c07a6b4611a24')

page_content = client.general_request(url).content

parser = MyHTMLParser()
parser.feed(page_content)

soup = BeautifulSoup(page_content, "html.parser")
st=soup.findAll("span")
last_is_printed_text = False
for i in st:
    if (i.get_text()[:2] == "2D") and not last_is_printed_text:
        print(i.get_text())
        last_is_printed_text = True
print(1)
