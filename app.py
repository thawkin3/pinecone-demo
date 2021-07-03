from dotenv import load_dotenv
from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
import json
import os
import pandas as pd
import pinecone
import requests
from sentence_transformers import SentenceTransformer

app = Flask(__name__)

pinecone_index_name = "question-answering-chatbot"
DATA_DIR = "tmp"
DATA_FILE = f"{DATA_DIR}/quora_duplicate_questions.tsv"
DATA_URL = "https://qim.fs.quoracdn.net/quora_duplicate_questions.tsv"

def initialize_pinecone():
    load_dotenv()
    PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]
    pinecone.init(api_key=PINECONE_API_KEY)

def delete_existing_pinecone_index():
    if pinecone_index_name in pinecone.list_indexes():
        pinecone.delete_index(pinecone_index_name)

def create_pinecone_index():
    pinecone.create_index(name=pinecone_index_name, metric="cosine", shards=1)
    pinecone_index = pinecone.Index(name=pinecone_index_name)

    return pinecone_index

def download_data():
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(DATA_FILE):
        r = requests.get(DATA_URL)
        with open(DATA_FILE, "wb") as f:
            f.write(r.content)

def read_tsv_file():
    df = pd.read_csv(
        f"{DATA_FILE}", sep="\t", usecols=["qid1", "question1"], index_col=False
    )
    df = df.sample(frac=1).reset_index(drop=True)
    df.drop_duplicates(inplace=True)

    return df

def create_and_apply_model():
    model = SentenceTransformer("average_word_embeddings_glove.6B.300d")
    df["question_vector"] = df.question1.apply(lambda x: model.encode(str(x)))
    pinecone_index.upsert(items=zip(df.qid1, df.question_vector))

    return model

def query_pinecone(search_term):
    query_question = str(search_term)
    query_vectors = [model.encode(query_question)]

    query_results = pinecone_index.query(queries=query_vectors, top_k=5)
    res = query_results[0]

    results_list = []

    for idx, _id in enumerate(res.ids):
        results_list.append({
            "id": _id,
            "question": df[df.qid1 == int(_id)].question1.values[0],
            "score": res.scores[idx],
        })

    return json.dumps(results_list)

initialize_pinecone()
delete_existing_pinecone_index()
pinecone_index = create_pinecone_index()
download_data()
df = read_tsv_file()
model = create_and_apply_model()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/search", methods=["POST", "GET"])
def search():
    if request.method == "POST":
        return query_pinecone(request.form.question)
    if request.method == "GET":
        return query_pinecone(request.args.get("question", ""))
