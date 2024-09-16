import genanki


def main() -> None:
    my_model = genanki.Model(
        model_id=1607392319,
        name="Simple Model",
        fields=[
            {"name": "Question"},
            {"name": "Answer"},
            {"name": "MyMedia"},  # ADD THIS
        ],
        templates=[
            {
                "name": "Card 1",
                "qfmt": "{{Question}}<br>{{MyMedia}}",  # AND THIS
                "afmt": '{{FrontSide}}<hr id="answer">{{Answer}}',
            },
        ],
    )

    my_note = genanki.Note(
        model=my_model,
        fields=["Capital of Argentina", "Buenos Aires", "sound.mp3"],
    )

    my_deck = genanki.Deck(deck_id=2059400110, name="Country Capitals")
    my_deck.add_note(note=my_note)

    my_package = genanki.Package(deck_or_decks=my_deck)
    my_package.write_to_file(file="output.apkg")
    my_package.media_files = ["sound.mp3", "images/image.jpg"]


if __name__ == "__main__":
    main()
