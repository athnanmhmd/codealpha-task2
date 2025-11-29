import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class FAQChatbot:
    def __init__(self, filepath='data/faqs.json'):
        self.filepath = filepath
        self.questions = []
        self.answers = []
        self.vectorizer = TfidfVectorizer()
        self.load_data()
        self.fit_model()

    def load_data(self):
        with open(self.filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.questions = list(data.keys())
        self.answers = list(data.values())

    def fit_model(self):
        # Convert FAQ questions into vectors
        self.tfidf_matrix = self.vectorizer.fit_transform(self.questions)

    def get_answer(self, user_query):
        # Convert user question into vector
        user_vec = self.vectorizer.transform([user_query])
        similarities = cosine_similarity(user_vec, self.tfidf_matrix)
        index = similarities.argmax()

        return self.answers[index]