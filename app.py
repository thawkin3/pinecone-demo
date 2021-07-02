from dotenv import load_dotenv
from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
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
    print("initialize_pinecone")
    load_dotenv()
    PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]
    pinecone.init(api_key=PINECONE_API_KEY)

def create_pinecone_index():
    print("create_pinecone_index")
    if pinecone_index_name in pinecone.list_indexes():
        pinecone.delete_index(pinecone_index_name)
    
    pinecone.create_index(name=pinecone_index_name, metric="cosine", shards=1)

    pinecone_index = pinecone.Index(name=pinecone_index_name)
    return pinecone_index

def download_data():
    print("download_data")
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(DATA_FILE):
        print("downloading TSV file")
        r = requests.get(DATA_URL)  # create HTTP response object
        with open(DATA_FILE, "wb") as f:
            f.write(r.content)

def read_tsv_file():
    pd.set_option("display.max_colwidth", 500)

    df = pd.read_csv(
        f"{DATA_FILE}", sep="\t", usecols=["qid1", "question1"], index_col=False
    )
    df = df.sample(frac=1).reset_index(drop=True)
    df.drop_duplicates(inplace=True)
    print(df.head())

    return df

def create_and_apply_model():
    print("create_and_apply_model")
    model = SentenceTransformer("average_word_embeddings_glove.6B.300d")
    df["question_vector"] = df.question1.apply(lambda x: model.encode(str(x)))

    acks = pinecone_index.upsert(items=zip(df.qid1, df.question_vector))
    print(pinecone_index.info())

    return model

# def query_pinecone(search_term):
def query_pinecone():
    print("query_pinecone")
    # print(search_term)
    # query_questions = [str(search_term)]
    query_questions = [
        "What is best way to make money online?",
    ]

    print("extracting embeddings for the questions")
    query_vectors = [model.encode(str(question)) for question in query_questions]

    print("querying pinecone")
    query_results = pinecone_index.query(queries=query_vectors, top_k=5)

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

initialize_pinecone()
pinecone_index = create_pinecone_index()
download_data()
df = read_tsv_file()
model = create_and_apply_model()
# query_pinecone()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/search", methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        # query_pinecone(request.form.questionInput)
        query_pinecone()
        return request.form.questionInput
    if request.method == 'GET':
        # query_pinecone(request.args.get('questionInput', ''))
        query_pinecone()
        return request.args.get('questionInput', '')
