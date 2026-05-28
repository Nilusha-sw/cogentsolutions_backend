import re
import string
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

for resource in ("punkt", "stopwords", "wordnet", "omw-1.4"):
    try:
        nltk.data.find(f"corpora/{resource}")
    except LookupError:
        nltk.download(resource, quiet=True)

_stop_words = set(stopwords.words("english"))
_lemmatizer = WordNetLemmatizer()


def preprocess(text: str) -> str:
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    tokens = text.split()
    tokens = [_lemmatizer.lemmatize(w) for w in tokens if w not in _stop_words]
    return " ".join(tokens)


def parse_agenda(filepath: str) -> list[dict]:
    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()

    blocks = re.split(r"\[SESSION_\d+\]", raw)[1:]

    sessions = []

    for i, block in enumerate(blocks, start=1):

        def _get(pattern: str) -> str:
            m = re.search(pattern, block)
            return m.group(1).strip() if m else ""

        sessions.append({
            "id": i,
            "time": _get(r"Time:\s*(.+)"),
            "title": _get(r"Title:\s*(.+)"),
            "speaker": _get(r"Speaker:\s*(.+)"),
            "keywords": _get(r"Focus Keywords:\s*(.+)"),
            "description": _get(r"Description:\s*(.+)"),
        })

    return sessions


class SessionMatcher:

    SIMILARITY_THRESHOLD = 0.05

    def __init__(self, agenda_path: str = "agenda.txt"):
        self.sessions = parse_agenda(agenda_path)
        self._build_index()

    def _build_index(self):
        corpus_docs = []

        for s in self.sessions:
            doc = f"{s['title']} {s['keywords']} {s['keywords']} {s['description']}"
            corpus_docs.append(doc)

        self.vectorizer = TfidfVectorizer(
            preprocessor=preprocess,
            ngram_range=(1, 2),
            min_df=1,
            sublinear_tf=True,
        )

        self.tfidf_matrix = self.vectorizer.fit_transform(corpus_docs)

    def match(self, user_text: str) -> dict:
        query_vec = self.vectorizer.transform([user_text])
        scores = cosine_similarity(query_vec, self.tfidf_matrix).flatten()

        best_idx = int(np.argmax(scores))
        best_score = float(scores[best_idx])

        ranked = sorted(
            [
                {
                    "session": self.sessions[i],
                    "score": float(scores[i])
                }
                for i in range(len(scores))
            ],
            key=lambda x: x["score"],
            reverse=True,
        )

        if best_score < self.SIMILARITY_THRESHOLD:
            return {
                "matched": None,
                "score": best_score,
                "ranked": ranked
            }

        return {
            "matched": self.sessions[best_idx],
            "score": round(best_score, 4),
            "ranked": ranked,
        }