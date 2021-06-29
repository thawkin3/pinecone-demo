from dotenv import load_dotenv
from flask import Flask
from flask import render_template
from flask import url_for
import os
import pandas as pd
import pinecone
import requests
from sentence_transformers import SentenceTransformer

app = Flask(__name__)

load_dotenv()
PINECONE_API_KEY = os.environ['PINECONE_API_KEY']

pinecone.init(api_key=PINECONE_API_KEY)

index_name = "question-answering-chatbot"

if index_name in pinecone.list_indexes():
    pinecone.delete_index(index_name)

pinecone.create_index(name=index_name, metric="cosine", shards=1)
index = pinecone.Index(name=index_name)

DATA_DIR = "tmp"
DATA_FILE = f"{DATA_DIR}/quora_duplicate_questions.tsv"
DATA_URL = "https://qim.fs.quoracdn.net/quora_duplicate_questions.tsv"

def download_data():
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(DATA_FILE):
        r = requests.get(DATA_URL)  # create HTTP response object
        with open(DATA_FILE, "wb") as f:
            f.write(r.content)

download_data()

pd.set_option("display.max_colwidth", 500)

df = pd.read_csv(
    f"{DATA_FILE}", sep="\t", usecols=["qid1", "question1"], index_col=False
)
df = df.sample(frac=1).reset_index(drop=True)
df.drop_duplicates(inplace=True)
print(df.head())

model = SentenceTransformer("average_word_embeddings_glove.6B.300d")
df["question_vector"] = df.question1.apply(lambda x: model.encode(str(x)))

acks = index.upsert(items=zip(df.qid1, df.question_vector))
print(index.info())


query_questions = [
    "What is best way to make money online?",
]

# extract embeddings for the questions
query_vectors = [model.encode(str(question)) for question in query_questions]

# query pinecone
query_results = index.query(queries=query_vectors, top_k=5)

# show the results
for question, res in zip(query_questions, query_results):
    print("\n\n\n Original question : " + str(question))
    print("\n Most similar questions based on pinecone vector search: \n")

    df_result = pd.DataFrame(
        {
            "id": res.ids,
            "question": [
                df[df.qid1 == int(_id)].question1.values[0] for _id in res.ids
            ],
            "score": res.scores,
        }
    )
    print(df_result)

@app.route("/")
def index():
    return render_template("index.html")
