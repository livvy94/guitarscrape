#!/usr/bin/python3
from bs4 import BeautifulSoup
import requests


def save_text(result, URL):
    print(result)
    with open("chords.txt", "w") as file:
        file.write(result + "\r\n\r\nOriginal URL:\r\n" + URL)


def main():
    # Try these URLs out to test!
    # URL = "https://tabs.ultimate-guitar.com/tab/joni-mitchell/free-man-in-paris-chords-1476236"
    # URL = "https://www.e-chords.com/chords/fairport-convention/i-dont-know-where-i-stand"
    # URL = "https://www.azchords.com/f/fairportconvention-tabs-5093/farewellfarewell-tabs-302501.html"
    print("Please paste in the URL:")
    URL = input()

    if "http" not in URL:
        exit()

    result = ""
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, "html.parser")

    if "ultimate-guitar" in URL:
        div = soup.select('div[class=js-store]')
        result = str(div)
        # Isolate the chords. If they change the way the HTML is
        # structured, I'll have to find these indexes differently.
        start_index = result.find("backing_track_tip") + 100
        end_index = result.find("revision_id") - 19
        result = result[start_index:end_index]
        # Remove formatting codes
        result = result.replace("\&quot", "")
        result = result.replace("[ch]", "")
        result = result.replace("[/ch]", "")
        result = result.replace("\\r\\n", "\r\n")
        result = result.replace("[tab]", "")
        result = result.replace("[/tab]", "")
        save_text(result, URL)
    elif "e-chords" in URL:
        div = soup.select('div[class=coremain]')
        result = str(div)
        # Isolate the chords. Similarly, these index numbers
        # will be wrong if they change the way the site works.
        start_index = result.find("\"core\">") + 7
        end_index = result.find("/div") - 13
        result = result[start_index:end_index]
        # Remove formatting codes
        result = result.replace("<u>", "")
        result = result.replace("</u>", "")
        result = result.replace("<i>", "")
        result = result.replace("</i>", "")
        save_text(result, URL)
    elif "azchords" in URL:
        div = soup.select('pre[id=content]')
        result = str(div)
        # This one's pretty straightforward!
        start_index = 20
        end_index = -7
        result = result[start_index:end_index]
        save_text(result, URL)
    else:
        print("That website isn't supported yet!")
        print("Bug me on GitHub about it!")


main()
