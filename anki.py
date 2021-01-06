import slob
import logging
from peewee import *
from bs4 import BeautifulSoup


# logger = logging.getLogger("peewee")
# logger.addHandler(logging.StreamHandler())
# logger.setLevel(logging.DEBUG)

database = SqliteDatabase(None)


class BaseModel(Model):
    class Meta:
        database = database


class ExtraField(TextField):
    sep = "\x1f"

    def db_value(self, value):
        return self.sep.join(value)

    def python_value(self, value):
        return value.split(self.sep)


class Notes(BaseModel):
    flds = ExtraField()
    sfld = TextField()

    class Meta:
        table_name = "notes"


database.init("B1_Wortliste_DTZ_Goethe.apkg_FILES/collection.anki2")


def get_IPA_from_Wiktionary(word):
    print(word)
    with slob.open("dewiktionary-20200420.slob") as r:
        values = slob.find(word, r, match_prefix=False)
        if values:
            try:
                _, blob_word = next(values)
                content = blob_word.content
                soup = BeautifulSoup(content, "html5lib")
            except Exception:
                return word
    try:
        ipa = soup.find(class_="ipa").get_text()
    except Exception:
        return word
    return word + f"({ipa})" if ipa else word


def get_main_word_with_ipa(front):
    parts = front.split(",")
    length_parts = len(parts)
    try:
        if length_parts == 1:
            return get_IPA_from_Wiktionary(parts[0])
        elif length_parts == 2:
            first_word = parts[0].split(" ")
            if len(first_word) == 1:
                parts[0] = get_IPA_from_Wiktionary(first_word[0])
            else:
                article, noun = first_word
                parts[0] = article + " " + get_IPA_from_Wiktionary(noun)
            return ",".join(parts)
        elif length_parts == 4:
            parts[0] = get_IPA_from_Wiktionary(parts[0])
            return ",".join(parts)
        else:
            return front
    except Exception:
        return front


def change_apkg(database_name=None):
    with database.atomic():
        all_content = Notes.select()
        for row in all_content:
            print(row.flds[0])
            front = row.flds[0]
            new_value = get_main_word_with_ipa(front)
            row.flds[0] = new_value
            row.sfld = new_value
            print(row.flds[0])
            row.save()

    print("All the ipa was added.")


change_apkg()
