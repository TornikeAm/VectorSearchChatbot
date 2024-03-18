import pandas as pd
import re
import spacy
import warnings
warnings.simplefilter('ignore')
nlp = spacy.load("en_core_web_md")

class PrepareData:
    def __init__(self):
        self.df = pd.read_csv("./sample_10k.csv")

    def clean_sentence(self, sentence):
        stopwords_pattern = r'\b(?:{})\b'.format('|'.join(nlp.Defaults.stop_words))
        numbers_pattern = r'\b\d+\b'
        punctuation_pattern = r'[^\w\s]'
        other_symbols_pattern = r'[^a-zA-Z\s]'
        combined_pattern = f'({stopwords_pattern}|{numbers_pattern}|{punctuation_pattern}|{other_symbols_pattern})'

        cleaned_sentence = re.sub(combined_pattern, '', sentence.lower())
        return cleaned_sentence

    def preprocess_df(self):
        self.df.drop(["Brand Name","Asin","Upc Ean Code","List Price","Quantity","Stock","Product Details","Dimensions","Color","Ingredients","Sku","Direction To Use","Size Quantity Variant","Product Description"], axis=1, inplace=True)
        self.df["Model Number"].fillna("Not Specified", inplace=True)
        self.df["About Product"].fillna("No Product Description", inplace=True)
        self.df["Selling Price"] = self.df["Selling Price"].str.replace(r'[^\d.]', '', regex=True)
        self.df["Selling Price"] = pd.to_numeric(self.df["Selling Price"], errors="coerce")
        self.df["Selling Price"].fillna(self.df["Selling Price"].mean(), inplace=True)
        self.df["Model Number"].fillna("Not Specified Model Number", inplace=True)
        self.df["Product Specification"].fillna("No product Specification", inplace=True)
        self.df["Technical Details"].fillna("No Technical Details", inplace=True)
        self.df["Shipping Weight"].fillna("Shipping Weight Is not Specified", inplace=True)
        self.df["Product Dimensions"].fillna("Product Dimensions are not Specified", inplace=True)
        self.df["Variants"].fillna("No Other Variants", inplace=True)
        return self.df

    def clean_names(self):
        names = []
        for sentence in self.df["Product Name"]:
            sentence = self.clean_sentence(sentence)
            names.append(sentence)
        return names

prepare = PrepareData()
df = prepare.preprocess_df()
names = prepare.clean_names()
