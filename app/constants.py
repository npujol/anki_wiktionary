OLD_ANKI_TEMPLATE = {
    "143453125187": {
        "id": 1434531251879,
        "name": "B1 Goethe",
        "type": 0,
        "mod": 1596295738,
        "usn": 387,
        "sortf": 0,
        "did": 1434531343983,
        "tmpls": [
            {
                "name": "Card 1",
                "ord": 0,
                "qfmt": '<div id="rubric">B1_Wortliste_DTZ_Goethe</div>\n'
                "<div style='font-family: Arial; font-size: "
                "70px;color:#FF80DD;'>{{Word}}</div>\n<hr>\n{{Sound}}"
                "<hr>\n<div style='font-family: Arial; font-size: 70px;"
                "color:#FF80DD;'>{{IPA}}</div>\n",
                "afmt": "<div style='font-family: Arial; color:#FF80DD;'>"
                "{{Word}} </div>\n<hr>\n{{English}}\n<hr>\n<div  "
                "style='font-family: Arial; color:#00aaaa; text-align:left;'>"
                "\nExamples: {{Example1}} {{Sound_1}} <hr>{{Example2}} "
                "{{Sound_2}} <hr>{{Example3}} {{Sound_3}}</div>\n<hr>\n",
                "bqfmt": "",
                "bafmt": "",
                "did": None,
                "bfont": "",
                "bsize": 0,
            }
        ],
        "flds": [
            {
                "name": "Word",
                "ord": 0,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
                "media": [],
            },
            {
                "name": "Sound",
                "ord": 1,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
                "media": [],
            },
            {
                "name": "IPA",
                "ord": 3,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
                "media": [],
            },
            {
                "name": "English",
                "ord": 4,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
                "media": [],
            },
            {
                "name": "Example1",
                "ord": 5,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
                "media": [],
            },
            {
                "name": "Example2",
                "ord": 6,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
                "media": [],
            },
            {
                "name": "Example3",
                "ord": 7,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
                "media": [],
            },
            {
                "name": "Sound1",
                "ord": 8,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
                "media": [],
            },
            {
                "name": "Sound2",
                "ord": 9,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
                "media": [],
            },
            {
                "name": "Sound3",
                "ord": 10,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
                "media": [],
            },
        ],
        "css": ".card {\n font-family: arial;\n font-size:150%;\n text-align:"
        " center;\n color: Black;\n background-color:black;\n}\n\n#rubric "
        "{\n  text-align: left;\n  padding: 4px;\n  padding-left: 10px;\n  "
        "padding-right: 10px;\n  margin-bottom: 10px;\n  background: "
        "#1d6695;\n  color: white;\n  font-weight: 500;\n}\n\n"
        "img{\n\tmax-width:100%;\n\theight:auto;\n          "
        "width:300px;\n          border-radius: 20px;\n}",
        "latexPre": "\\documentclass[12pt]{article}\n\\"
        "special{papersize=3in,5in}\n\\usepackage[utf8]{inputenc}"
        "\n\\usepackage{amssymb,amsmath}\n\\pagestyle{empty}"
        "\n\\setlength{\\parindent}{0in}\n\\begin{document}\n",
        "latexPost": "\\end{document}",
        "latexsvg": False,
        "req": [[0, "any", [0, 2, 7]]],
        "vers": [],
        "tags": [],
    },
    "1607592501447": {
        "id": 1607592501447,
        "name": "Basic",
        "type": 0,
        "mod": 0,
        "usn": 0,
        "sortf": 0,
        "did": 1,
        "tmpls": [
            {
                "name": "Card 1",
                "ord": 0,
                "qfmt": "{{Front}}",
                "afmt": "{{FrontSide}}\n\n<hr id=answer>\n\n{{Back}}",
                "bqfmt": "",
                "bafmt": "",
                "did": None,
                "bfont": "",
                "bsize": 0,
            }
        ],
        "flds": [
            {
                "name": "Front",
                "ord": 0,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
            },
            {
                "name": "Back",
                "ord": 1,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
            },
        ],
        "css": ".card {\n  font-family: arial;\n  font-size: 20px;\n "
        " text-align: center;\n  color: black;\n  background-color:"
        " white;\n}\n",
        "latexPre": "\\documentclass[12pt]{article}\n\\special"
        "{papersize=3in,5in}\n\\usepackage[utf8]{inputenc}\n\\"
        "usepackage{amssymb,amsmath}\n\\pagestyle{empty}\n\\setlength"
        "{\\parindent}{0in}\n\\begin{document}\n",
        "latexPost": "\\end{document}",
        "latexsvg": False,
        "req": [[0, "any", [0]]],
    },
    "1516347233607": {
        "id": 1516347233607,
        "name": "Basic (and reversed card)-7c609",
        "type": 0,
        "mod": 1581413740,
        "usn": 0,
        "sortf": 0,
        "did": 1516347471116,
        "tmpls": [
            {
                "name": "Card 1",
                "ord": 0,
                "qfmt": "{{base_d}}{{base_a}}\n\n\n\n",
                "afmt": "{{base_e}}<br>\n{{full_d}}{{base_a}}\n<div "
                'style="display:none">[sound:_1-minute-of-silence.mp3]'
                "</div>\n\n<hr id=answer>\n\n<div style='font-family: Arial; "
                "font-size: 16px;'>{{s1}}{{s1a}}{{hint:s1e}}</div><br>\n<div "
                "style='font-family: Arial; font-size: 16px;'>{{s2}}{{s2a}}"
                "{{hint:s2e}}</div><br>\n<div style='font-family: Arial; "
                "font-size: 16px;'>{{s3}}{{s3a}}{{hint:s3e}}</div><br>\n"
                "<div style='font-family: Arial; font-size: 16px;'>{{s4}}"
                "{{s4a}}{{hint:s4e}}</div>\n<div style='font-family: "
                "Arial; font-size: 16px;'>{{s5}}{{s5a}}{{hint:s5e}}</div>"
                "\n<div style='font-family: Arial; font-size: 16px;'>{{s6}}"
                "{{s6a}}{{hint:s6e}}</div>\n<div style='font-family: Arial;"
                " font-size: 16px;'>{{s7}}{{s7a}}{{hint:s7e}}</div>\n"
                "<div style='font-family: Arial; font-size: 16px;'>"
                "{{s8}}{{s8a}}{{hint:s8e}}</div>\n<div style='font-family:"
                " Arial; font-size: 16px;'>{{s9}}{{s9a}}{{hint:s9e}}</div>\n",
                "bqfmt": "",
                "bafmt": "",
                "did": None,
                "bfont": "",
                "bsize": 0,
            },
            {
                "name": "Card 2",
                "ord": 1,
                "qfmt": "{{base_e}}",
                "afmt": "{{full_d}}{{base_a}}<br>\n{{base_e}}\n<div "
                'style="display:none">[sound:_1-minute-of-silence.mp3]'
                "</div>\n\n<hr id=answer>\n\n<div style='font-family: Arial; "
                "font-size: 16px;'>{{s1e}}{{s1a}}{{hint:s1}}</div>\n<div "
                "style='font-family: Arial; font-size: 16px;'>{{s2e}}{{s2a}}"
                "{{hint:s2}}</div>\n<div style='font-family: Arial; "
                "font-size: 16px;'>{{s3e}}{{s3a}}{{hint:s3}}</div>\n<div "
                "style='font-family: Arial; font-size: 16px;'>{{s4e}}{{s4a}}"
                "{{hint:s4}}</div>\n<div style='font-family: Arial; "
                "font-size: 16px;'>{{s5e}}{{s5a}}{{hint:s5}}</div>\n<div "
                "style='font-family: Arial; font-size: 16px;'>{{s6e}}{{s6a}}"
                "{{hint:s6}}</div>\n<div style='font-family: Arial; "
                "font-size: 16px;'>{{s7e}}{{s7a}}{{hint:s7}}</div>\n"
                "<div style='font-family: Arial; font-size: 16px;'>"
                "{{s8e}}{{s8a}}{{hint:s8}}</div>\n"
                "<div style='font-family: Arial; font-size: 16px;'>"
                "{{s9e}}{{s9a}}{{hint:s9}}</div>",
                "bqfmt": "",
                "bafmt": "",
                "did": None,
                "bfont": "",
                "bsize": 0,
            },
        ],
        "flds": [
            {
                "name": "full_d",
                "ord": 0,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
                "media": [],
            },
            {
                "name": "base_e",
                "ord": 1,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
                "media": [],
            },
            {
                "name": "base_d",
                "ord": 2,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
                "media": [],
            },
            {
                "name": "artikel_d",
                "ord": 3,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
                "media": [],
            },
            {
                "name": "plural_d",
                "ord": 4,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
                "media": [],
            },
            {
                "name": "audio_text_d",
                "ord": 5,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
                "media": [],
            },
            {
                "name": "s1",
                "ord": 6,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
                "media": [],
            },
            {
                "name": "s1e",
                "ord": 7,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
                "media": [],
            },
            {
                "name": "s2",
                "ord": 8,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
                "media": [],
            },
            {
                "name": "s2e",
                "ord": 9,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
                "media": [],
            },
            {
                "name": "s3",
                "ord": 10,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
                "media": [],
            },
            {
                "name": "s3e",
                "ord": 11,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
                "media": [],
            },
            {
                "name": "s4",
                "ord": 12,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
                "media": [],
            },
            {
                "name": "s4e",
                "ord": 13,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
                "media": [],
            },
            {
                "name": "s5",
                "ord": 14,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
                "media": [],
            },
            {
                "name": "s5e",
                "ord": 15,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
                "media": [],
            },
            {
                "name": "s6",
                "ord": 16,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
                "media": [],
            },
            {
                "name": "s6e",
                "ord": 17,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
                "media": [],
            },
            {
                "name": "s7",
                "ord": 18,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
                "media": [],
            },
            {
                "name": "s7e",
                "ord": 19,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
                "media": [],
            },
            {
                "name": "s8",
                "ord": 20,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
                "media": [],
            },
            {
                "name": "s8e",
                "ord": 21,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
                "media": [],
            },
            {
                "name": "s9",
                "ord": 22,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
                "media": [],
            },
            {
                "name": "s9e",
                "ord": 23,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
                "media": [],
            },
            {
                "name": "original_order",
                "ord": 24,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
                "media": [],
            },
            {
                "name": "base_a",
                "ord": 25,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
                "media": [],
            },
            {
                "name": "s1a",
                "ord": 26,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
                "media": [],
            },
            {
                "name": "s2a",
                "ord": 27,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
                "media": [],
            },
            {
                "name": "s3a",
                "ord": 28,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
                "media": [],
            },
            {
                "name": "s4a",
                "ord": 29,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
                "media": [],
            },
            {
                "name": "s5a",
                "ord": 30,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
                "media": [],
            },
            {
                "name": "s6a",
                "ord": 31,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
                "media": [],
            },
            {
                "name": "s7a",
                "ord": 32,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
                "media": [],
            },
            {
                "name": "s8a",
                "ord": 33,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
                "media": [],
            },
            {
                "name": "s9a",
                "ord": 34,
                "sticky": False,
                "rtl": False,
                "font": "Arial",
                "size": 20,
                "media": [],
            },
        ],
        "css": ".card {\n font-family: arial;\n font-size: 20px;\n "
        "text-align: center;\n color: black;\n background-color: white;\n}\n",
        "latexPre": "\\documentclass[12pt]{article}\n\\"
        "special{papersize=3in,5in}\n\\usepackage[utf8]{inputenc}\n\\"
        "usepackage{amssymb,amsmath}\n\\pagestyle{empty}\n\\"
        "setlength{\\parindent}{0in}\n\\begin{document}\n",
        "latexPost": "\\end{document}",
        "latexsvg": False,
        "req": [[0, "any", [2, 25]], [1, "any", [1]]],
        "tags": [],
        "vers": [],
    },
}
