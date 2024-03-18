import spacy
import faiss
import numpy as np
from scipy.spatial.distance import cosine
from prepareData import df,names

class ProductSearch:
    def __init__(self, names):
        self.names = names
        self.df = df
        self.nlp = spacy.load("en_core_web_md")
        self.d = 300
        self.index = faiss.IndexFlatL2(self.d)
        self.embeddings = self.add_embeddings_to_index()

    def get_spacy_embedding(self, product_name):
        doc = self.nlp(product_name)
        embeddings = doc.vector
        return embeddings

    def add_embeddings_to_index(self):
        embeddings = []
        for product_name in self.names:
            embeddings.append(self.get_spacy_embedding(product_name.lower()))
        embeddings = np.array(embeddings)
        # L2 normalize the embeddings
        faiss.normalize_L2(embeddings)
        self.index.add(embeddings)
        return embeddings

    def get_closest_embeddings_and_rows(self, user_input, k=5):
        user_embedding = self.get_spacy_embedding(user_input)
        user_embedding = user_embedding.reshape(1, -1).astype(np.float32)
        faiss.normalize_L2(user_embedding)
        _, indices = self.index.search(user_embedding, k)
        closest_embeddings = self.embeddings[indices[0]]
        closest_rows = self.df.iloc[indices[0]]
        scores = [1 - cosine(user_embedding.flatten(), emb) for emb in closest_embeddings]
        closest_rows['score'] = scores
        closest_rows = closest_rows.sort_values(by='score', ascending=False)
        product_names = closest_rows['Product Name'].tolist()
        other_columns = {}
        for column in ['Category', 'Selling Price', 'Model Number',
                       'About Product', 'Product Specification', 'Technical Details',
                       'Shipping Weight', 'Product Dimensions', 'Image', 'Variants',
                       'Product Url', 'Is Amazon Seller']:
            other_columns[column] = closest_rows[column].tolist()
        other_columns['Score'] = closest_rows['score'].tolist()
        return product_names, other_columns

# Example usage:
product_search = ProductSearch(names)

