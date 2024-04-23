import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from bs4 import BeautifulSoup
import os

class Indexer:
    def __init__(self):
        self.tfidf_vectorizer = TfidfVectorizer()
        self.index = None

    def add_document_from_html_file(self, filepath):
        if os.path.isfile(filepath):
            html_content = self.get_html_content(filepath)
            if html_content:
                soup = BeautifulSoup(html_content, 'html.parser')
                text = soup.get_text()
                if self.index is None:
                    self.index = self.tfidf_vectorizer.fit_transform([text])
                else:
                    self.index = self.index + self.tfidf_vectorizer.transform([text])
        else:
            print(f"File not found: {filepath}")

    def query(self, query, k=5):
        if self.index is None:
            return None
    
        query_vector = self.tfidf_vectorizer.transform([query])
        cosine_similarities = cosine_similarity(query_vector, self.index)
        indices = cosine_similarities.argsort()[0][-k:][::-1] 
        tfidf_scores = [cosine_similarities[0][index] for index in indices] 
        
        print("Similar Documents (using Cosine Similarity):")
        for i, index in enumerate(indices):
            print(f"Document {index}: TF-IDF Score = {tfidf_scores[i]:.4f}, Cosine Similarity Score = {cosine_similarities[0][index]:.4f}")

    def get_html_content(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(f"File not found: {filepath}")
            return None

def main():
    try:
        print("Script execution started.")
        html_file_path = r'D:\cs429 PROJECT\Scrapy\postscrape\combined_posts.html'
        index = Indexer()
        index.add_document_from_html_file(html_file_path)
        print("HTML document added to the index.")
        query = input("Enter your query: ")
        index.query(query)

        print("Script execution completed.")

    except FileNotFoundError as e:
        print(f"Error: {e}. Make sure the HTML file exists.")

if __name__ == "__main__":
    main()
