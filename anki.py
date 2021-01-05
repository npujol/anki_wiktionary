import slob
from bs4 import BeautifulSoup


def get_IPA_from_Wiktionary(word):
    with slob.open("dewiktionary-20200420.slob") as r:
        values = slob.find(word, r, match_prefix=False)
        _, blob_word = next(values)

        content = blob_word.content
        soup = BeautifulSoup(content, "html5lib")

    ipa = soup.find(class_="ipa")
    return ipa


get_IPA_from_Wiktionary("Liebe")