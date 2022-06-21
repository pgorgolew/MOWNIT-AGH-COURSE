from collections import defaultdict
from nltk.stem import WordNetLemmatizer
from scipy import sparse
from gensim.parsing.preprocessing import remove_stopwords
import os
import nltk
import re
import math
import pickle
import numpy as np

nltk.download('wordnet', download_dir=os.path.join(os.getcwd(), 'venv', 'nltk_data'))
nltk.download('omw-1.4', download_dir=os.path.join(os.getcwd(), 'venv', 'nltk_data'))

DATA_DIR = os.path.join('app', 'logic', 'data')
ARTICLES = os.path.join(DATA_DIR, 'articles_dict_dump_of_len_2890')
ALL_ARTICLES_TITLES_PATH = os.path.join(DATA_DIR, 'parser_all_articles_titles_with_2890_articles')
ALL_UNIQUE_WORDS_PATH = os.path.join(DATA_DIR, 'parser_all_unique_words_with_2890_articles')
IDS_BY_UNIQUE_WORDS_PATH = os.path.join(DATA_DIR, 'parser_ids_by_unique_word_with_2890_articles')
TERM_BY_DOCUMENT_PATH = os.path.join(DATA_DIR, 'parser_term_by_document_with_2890_articles')


def article_result(number: int, title: str, probability: float, url: str) -> dict:
    return {
        'number': number,
        'title': title,
        'probability': f'{round(probability * 100, 2)} %',
        'url': url
    }


def find(input: str, articles_count: int):
    print(os.getcwd())
    parser = ArticlesParser(pickle.load(open(ARTICLES, "rb")))
    parser.all_articles_titles = pickle.load(open(ALL_ARTICLES_TITLES_PATH, "rb"))
    parser.all_unique_words = pickle.load(open(ALL_UNIQUE_WORDS_PATH, "rb"))
    parser.ids_by_unique_word = pickle.load(open(IDS_BY_UNIQUE_WORDS_PATH, "rb"))
    parser.term_by_document = pickle.load(open(TERM_BY_DOCUMENT_PATH, "rb"))
    return parser.find_articles(input, articles_count)


# COPIED FROM JUPYTER
class ArticlesParser:
    def __init__(self, articles: dict[str, dict[str, str]]):
        self.articles = articles
        self.parsed_articles = dict()
        self.ids_by_unique_word = None  # Dict[word: str, id: int]
        self.term_by_document = None  # sparse_matrix
        self.all_unique_words = None  # List[str]
        self.all_articles_titles = None  # List[str]
        self.all_words_data = defaultdict(lambda: 0)
        self.lemmatizer = WordNetLemmatizer()
        self.Ak_matrix = None

    def parse_artciles_and_prepare_term_by_document(self):
        print("STARTED")
        self.parse_articles()
        print("AFTER ARTICLE PARSING")
        self.create_bags_of_words()
        print("AFTER CREATING BAGS")
        self.create_term_by_document_matrix()
        print("AFTER CREATING DOCUMENT BY TERM")
        self.multiply_term_by_document_by_IDF()
        print("AFTER MULTIPLYING BY IDF")
        self.normalize_vectors()
        print("AFTER NORMALIZATION")
        self.get_Ak_from_term_by_document()
        print("AFTER ALL")

    def normalize_vectors(self):
        for i in range(len(self.all_articles_titles)):
            vector = self.term_by_document.getcol(i)
            vector_norm = self.get_norm_from_vector(vector)
            self.term_by_document[:, i] /= vector_norm

    def parse_content(self, content: str, is_article=True):
        content = content.lower()
        content = re.sub(r'[^\w\s]', '', content)
        content = re.sub('[0-9]', '', content)
        content = re.sub(' {2} +', ' ', content)
        content = remove_stopwords(content)

        words_data = defaultdict(lambda: 0)
        words_count = 0
        for word in content.split():
            lemmatized_word = self.lemmatizer.lemmatize(word, pos='v')
            words_data[lemmatized_word] += 1
            if is_article:
                self.all_words_data[lemmatized_word] += 1
            words_count += 1

        return dict(words_data=words_data, words_count=words_count)

    def parse_articles(self):
        self.all_articles_titles = list(self.articles.keys())
        for article in self.all_articles_titles:
            self.parsed_articles[article] = dict()
            self.parsed_articles[article]['content_data'] = self.parse_content(self.articles[article]['content'])

        self.all_unique_words = list(self.all_words_data.keys())
        self.ids_by_unique_word = {self.all_unique_words[i]: i for i in range(len(self.all_unique_words))}

    def create_bags_of_words(self):
        for article in self.all_articles_titles:
            self.parsed_articles[article]['bag_of_words'] = \
                self.create_bag_of_words(self.parsed_articles[article]['content_data'])

    def create_bag_of_words(self, content_data):
        article_unique_words = content_data['words_data'].keys()
        vector = sparse.dok_matrix(np.zeros((len(self.ids_by_unique_word), 1)))
        for word in article_unique_words:  # TODO maybe jakiś numpy mapping or coś
            vector[self.ids_by_unique_word[word], 0] = content_data['words_data'][word]

        vector /= content_data['words_count']
        return sparse.csr_matrix(vector)

    def create_term_by_document_matrix(self):
        amount_of_articles = len(self.all_articles_titles)
        amount_of_words = len(self.all_unique_words)
        self.term_by_document = sparse.lil_matrix((amount_of_words, amount_of_articles))

        for i in range(amount_of_articles):
            self.term_by_document[:, i] = self.parsed_articles[self.all_articles_titles[i]]['bag_of_words']

    def multiply_term_by_document_by_IDF(self):
        articles_count = len(self.all_articles_titles)
        self.term_by_document = sparse.csr_matrix(self.term_by_document)
        for word in self.all_unique_words:
            articles_with_word = self.calculate_articles_with_word(word)
            idf = math.log(articles_count / articles_with_word)
            id_of_word = self.ids_by_unique_word[word]
            self.term_by_document[id_of_word] *= idf

    def calculate_articles_with_word(self, word: str):
        return sum(1 for article in self.parsed_articles.values() if word in article['content_data'].words_data)

    @staticmethod
    def get_norm_from_vector(vector):
        return math.sqrt(vector.power(2).sum())

    def find_articles(self, query, artciles_num_to_return, Ak_matrix=False):
        if Ak_matrix:
            matrix = self.Ak_matrix
        else:
            matrix = self.term_by_document

        query_words_data = self.parse_content(content=query, is_article=False)
        vector = self.create_bag_of_words(query_words_data)
        vector_norm = self.get_norm_from_vector(vector)

        probabilities = []
        for i in range(len(self.all_articles_titles)):
            article = matrix.getcol(i)
            product = (vector.T @ article)[0, 0]  # just getting first val
            divider = vector_norm * self.get_norm_from_vector(article)
            document_cosinus = product / divider
            probabilities.append((document_cosinus, i))

        probabilities.sort(key=lambda t: t[0], reverse=True)

        result = list()
        place = 1
        print(f"Articles found for guery: {query}")
        for probability, index in probabilities[:artciles_num_to_return]:
            article = self.all_articles_titles[index]
            print(f"\tARTICLE: {article}\t\tPROBABILITY: {probability}\t\tURL: {self.articles[article]['url']}")
            result.append(article_result(place, article, probability, self.articles[article]['url']))
            place += 1

        return result

    def get_Ak_from_term_by_document(self, k=200):
        u, s, vt = sparse.linalg.svds(self.term_by_document, k=k)
        print("AFTER SVD")
        u = sparse.csr_matrix(u)
        s = sparse.diags(s)
        vt = sparse.csr_matrix(vt)
        self.Ak_matrix = u @ s @ vt
