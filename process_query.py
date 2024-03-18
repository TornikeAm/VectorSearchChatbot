import spacy
import re

nlp = spacy.load("en_core_web_md")

def process_query(query):
    doc = nlp(query)
    keywords = [token.text for token in doc if not token.is_stop and not token.is_punct]
    entities = [ent.text for ent in doc.ents]
    keywords_str = " ".join(keywords)
    return keywords_str, entities


def clean_sentence(sentence):
    doc = nlp(sentence)
    cleaned_tokens = [token.text for token in doc if not token.is_stop and not token.is_punct]
    cleaned_sentence = " ".join(cleaned_tokens)
    return cleaned_sentence
