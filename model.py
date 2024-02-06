from peewee import BareField, IntegerField, SqliteDatabase, Model, TextField


database = SqliteDatabase("Deutsch/collection.anki21")


class UnknownField(object):
    def __init__(self, *_, **__):
        pass


class ExtraField(TextField):
    sep = "\x1f"

    def db_value(self, value: str):
        return self.sep.join(value)

    def python_value(self, value: str):
        return value.split(self.sep)


class BaseModel(Model):
    class Meta:
        database = database


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
    data = TextField()
    flags = IntegerField()
    flds = ExtraField()
    guid = TextField()
    mid = IntegerField()
    mod = IntegerField()
    sfld = IntegerField()
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


class SqliteStat4(BaseModel):
    idx = BareField(null=True)
    ndlt = BareField(null=True)
    neq = BareField(null=True)
    nlt = BareField(null=True)
    sample = BareField(null=True)
    tbl = BareField(null=True)

    class Meta:
        table_name = "sqlite_stat4"
        primary_key = False


def change_fields():
    with database.atomic():
        all_content = Notes.select()
        for row in all_content:
            fields = row.flds
            word, ipa = [fields[2]], [""]
            sound, english = [fields[25]], [fields[1]]
            ex1 = [fields[6] + "(" + fields[7] + ")"]
            ex2 = [fields[8] + "(" + fields[9] + ")"]
            ex3 = [fields[10] + "(" + fields[11] + ")"]
            s1, s2, s3 = [fields[26]], [fields[27]], [fields[28]]

            row.flds = word + ipa + sound + english + ex1 + ex2 + ex3 + s1 + s2 + s3  # noqa
            row.sfld = fields[2]
            print(row.flds)
            row.save()


def update_model():
    with database.atomic():
        all_content = Notes.select()
        for row in all_content:
            row.mid = "143453125187"
            row.save()


def change_fields_add_ipa():
    breakpoint()
    with database.atomic():
        all_content = Notes.select()
        for row in all_content:
            front = row.flds[0]
            row.flds[4] = front
            row.save()
            print(row.flds)

    print("All the ipa was added.")


change_fields_add_ipa()


def change_apkg(database_name: str = None):
    breakpoint()
    with database.atomic():
        breakpoint()
        all_content = Notes.select()
        for row in all_content:
            print(row.flds[0])
            front = row.flds[0]
            new_value = front
            row.flds[0] = new_value
            row.sfld = new_value
            print(row.flds[0])
            row.save()

    print("All the ipa was added.")


change_apkg()
