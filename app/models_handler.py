import json

from peewee import BareField, IntegerField, Model, TextField
from peewee import SqliteDatabase

from .constants import OLD_ANKI_TEMPLATE
from .ipa_handler import get_main_word_with_ipa


database = SqliteDatabase(None)

database.init("Deutsch/collection.anki2")


class BaseModel(Model):
    class Meta:
        database = database


class ExtraField(TextField):
    sep = "\x1f"

    def db_value(self, value: str):
        return self.sep.join(value)

    def python_value(self, value: str):
        return value.split(self.sep)


class Cards(BaseModel):
    data = TextField()
    did = IntegerField()
    due = IntegerField()
    factor = IntegerField()
    flags = IntegerField()
    ivl = IntegerField()
    lapses = IntegerField()
    left = IntegerField()
    mod = IntegerField()
    nid = IntegerField(index=True)
    odid = IntegerField()
    odue = IntegerField()
    ord = IntegerField()
    queue = IntegerField()
    reps = IntegerField()
    type = IntegerField()
    usn = IntegerField(index=True)

    class Meta:
        table_name = "cards"
        indexes = ((("did", "queue", "due"), False),)


class Col(BaseModel):
    conf = TextField()
    crt = IntegerField()
    dconf = TextField()
    decks = TextField()
    dty = IntegerField()
    ls = IntegerField()
    mod = IntegerField()
    models = TextField()
    scm = IntegerField()
    tags = TextField()
    usn = IntegerField()
    ver = IntegerField()

    class Meta:
        table_name = "col"


class Graves(BaseModel):
    oid = IntegerField()
    type = IntegerField()
    usn = IntegerField()

    class Meta:
        table_name = "graves"
        primary_key = False


class Notes(BaseModel):
    csum = IntegerField(index=True)
    flds = ExtraField()
    sfld = TextField()
    data = TextField()
    flags = IntegerField()
    guid = TextField()
    mid = IntegerField()
    mod = IntegerField()
    tags = TextField()
    usn = IntegerField(index=True)

    class Meta:
        table_name = "notes"


class Revlog(BaseModel):
    cid = IntegerField(index=True)
    ease = IntegerField()
    factor = IntegerField()
    ivl = IntegerField()
    last_ivl = IntegerField(column_name="lastIvl")
    time = IntegerField()
    type = IntegerField()
    usn = IntegerField(index=True)

    class Meta:
        table_name = "revlog"


class SqliteStat1(BaseModel):
    idx = BareField(null=True)
    stat = BareField(null=True)
    tbl = BareField(null=True)

    class Meta:
        table_name = "sqlite_stat1"
        primary_key = False


def change_fields():
    with database.atomic():
        all_content = Notes.select()
        for row in all_content:
            fields = row.flds
            word, ipa = [fields[2]], [get_main_word_with_ipa(fields[2])]
            sound, english = [fields[25]], [fields[1]]
            ex1 = [fields[6] + "(" + fields[7] + ")"]
            ex2 = [fields[8] + "(" + fields[9] + ")"]
            ex3 = [fields[10] + "(" + fields[11] + ")"]
            s1, s2, s3 = [fields[26]], [fields[27]], [fields[28]]

            row.flds = word + ipa + sound + english + ex1 + ex2 + ex3 + s1 + s2 + s3  # noqa
            row.sfld = fields[2]
            print(row.flds)
            row.save()


def add_model():
    with database.atomic():
        col_1 = Col.select()[0]
        col_1.models = json.dumps(OLD_ANKI_TEMPLATE)
        col_1.save()


def update_model():
    with database.atomic():
        all_content = Notes.select()
        for row in all_content:
            row.mid = "143453125187"
            row.save()


def change_fields_add_ipa():
    with database.atomic():
        all_content = Notes.select()
        for row in all_content:
            front = row.flds[0]
            row.flds[4] = get_main_word_with_ipa(front)
            row.save()
            print(row.flds)

    print("All the ipa was added.")


change_fields_add_ipa()
