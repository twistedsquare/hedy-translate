#! /usr/local/bin/python3
# Pre-requisite: Python 3
# Pre-requisite: pip3 install google-cloud-translate==2.0.1
# Pre-requisite: pip3 install pyyaml

hedy_path = "../hedy"

# Adapted from https://cloud.google.com/translate/docs/basic/translating-text#translate_translate_text-python
def translate_text(source, target, text):
    """Translates text into the target language.

    Source and target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    import six
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target, source_language=source)

    print(u"Text: {}".format(result["input"]))
    print(u"Translation: {}".format(result["translatedText"]))
    #print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))
    return result["translatedText"]

# Adapted from https://pyyaml.org/wiki/PyYAMLDocumentation
def load_file(path):
    import yaml
    with open(path) as file:
        return yaml.safe_load(file)

def translate_hedy_lang(source, source_dict, target):
    """source_dict is a map from canonical keyword to manual translation    
    """
    # We translate the file forwards into target language:
    r = {}
    for key, source_keyword in source_dict.items():
        target_keyword = translate_text(source, target, source_keyword)
        r[key] = target_keyword
    return r

from os import listdir
from os.path import isfile, join
# From https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory 
#  and https://stackoverflow.com/questions/19142042/python-regex-to-get-everything-until-the-first-dot-in-a-string
found_langs = [f[0:f.find('.')] for f in listdir(hedy_path + "/content/keywords") if f.endswith(".yaml")]

manual = {l:load_file(hedy_path + "/content/keywords/" + l + ".yaml") for l in found_langs}
forward = {}
backward = {}

for lang in found_langs:
    # Google Translate doesn't allow translating en->en so don't ask for it:
    if lang != "en":
        # Translate "forward" from english into that language:
        forward[lang] = translate_hedy_lang("en", manual["en"], lang)
        # And "backward" from that language into english:
        backward[lang] = translate_hedy_lang(lang, manual[lang], "en")

# Generate CSVs.  Each original keyword is a row in the file, and for each language we add three columns:
# the manual translation, the forward translation, and the backward translation
canon = manual["en"].keys()

# From https://docs.python.org/3/library/csv.html
import csv
with open('translations.csv', 'w', newline='') as csvfile:
    w = csv.writer(csvfile)
    # From https://stackoverflow.com/questions/952914/how-do-i-make-a-flat-list-out-of-a-list-of-lists
    def flatten(l):
        return [item for sublist in l for item in sublist]
    w.writerow(["Canonical"] + flatten([[l + " Manual", l + " Forward", l + " Backward"] for l in found_langs]))
    for k in canon:
        row = [k]
        for l in found_langs:
            if lang != "en":
                row.append(manual[l].get(k, ''))
                row.append(forward.get(l, {}).get(k, ''))
                row.append(backward.get(l, {}).get(k, ''))
        w.writerow(row)

