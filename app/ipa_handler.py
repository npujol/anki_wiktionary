from bs4 import BeautifulSoup
import slob


# TODO: Refactor to use more than one language
def get_german_IPA_from_Wiktionary(word):
    with slob.open("dewiktionary-20200420.slob") as r:
        values = slob.find(word, r, match_prefix=False)
        for _, blob_word in values:
            content = blob_word.content
            soup = BeautifulSoup(content, "html5lib")
            try:
                ipa = soup.find(class_="ipa").get_text()  # type: ignore
                return ipa
            except Exception:
                pass
    return ""


# TODO: Refactor using a Handler
def get_main_word_with_ipa(front):
    parts = front.split(",")
    length_parts = len(parts)
    try:
        if length_parts == 1:
            return get_german_IPA_from_Wiktionary(parts[0])
        elif length_parts == 2:
            first_word = parts[0].split(" ")
            if len(first_word) == 1:
                parts[0] = get_german_IPA_from_Wiktionary(first_word[0])
            else:
                _, noun = first_word
            return get_german_IPA_from_Wiktionary(noun)  # type: ignore
        elif length_parts == 4:
            return get_german_IPA_from_Wiktionary(parts[0])
        else:
            return ""
    except Exception:
        return ""
