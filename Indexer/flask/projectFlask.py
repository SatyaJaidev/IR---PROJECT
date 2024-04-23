from flask import Flask, request, jsonify, render_template
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

class DocumentSearch:
    def __init__(self, data_file_path):
        self.data_file_path = data_file_path
        self.documents, self.doc_pairs = self._retrieve_documents()

        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.vectorizer.fit_transform(self.documents)

    def _retrieve_documents(self):
        documents = []
        doc_pairs = []
        with open(self.data_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data:
                title = item.get('title', '')
                url = item.get('url', '')
                content = item.get('content', '')
                text = f"Title: {title}\nurl: {url}\ncontent: {content}"
                documents.append(text)
                doc_pairs.append((self.data_file_path, text))
        return documents, doc_pairs

    def search(self, query):
        query_vector = self.vectorizer.transform([query])
        cosine_sims = cosine_similarity(query_vector, self.tfidf_matrix)
        scores = list(cosine_sims[0])
        sorted_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
        result = []
        for i in sorted_indices:
            if scores[i] > 0:
                result.append((self.doc_pairs[i][1], scores[i]))
        return result

data_path =  r'D:\cs429 PROJECT\Scrapy\postscrape\postscrape\spiders\output.json'
search_engine = DocumentSearch(data_path)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return jsonify({'message': 'Favicon not found'}), 404

@app.route('/query', methods=['POST'])
def process_query():
    data = request.form
    if 'query' not in data:
        return jsonify({'error': 'Query is missing'}), 400

    query = data['query']

    results = search_engine.search(query)

    if not results:
        return jsonify({'message': 'Results not found'})

    formatted_results = []
    k = 5
    for i, (document, score) in enumerate(results):
        if i >= k:
            break
        formatted_result = {
            'cosine_similarity_score': score
        }
        formatted_results.append(formatted_result)

    return jsonify({'results': formatted_results})

if __name__ == '__main__':
    app.run(debug=True)
    
