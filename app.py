from dotenv import load_dotenv
from flask import Flask
from flask import render_template
from flask import url_for
import os
import pandas as pd
import pinecone

app = Flask(__name__)

load_dotenv()
pinecone_api_key = user = os.environ['PINECONE_API_KEY']

pinecone.init(api_key=pinecone_api_key)

# list your Pinecone indexes
print('listing existing pinecone indexes')
print(pinecone.list_indexes())

# Delete the index
print('deleting existing pinecone indexes')
pinecone.delete_index("hello-tyler-pinecone-index")

# Create an index
print('creating a new index')
pinecone.create_index("hello-tyler-pinecone-index", metric="euclidean")

# Connect to the index
print('connecting to the index')
index = pinecone.Index("hello-tyler-pinecone-index")

# Generate some data
print('generating some data')
df = pd.DataFrame(data={
    "id": ["A", "B", "C", "D", "E"],
    "vector": [[1]*2, [2]*2, [3]*2, [4]*2, [5]*2]
})

# Insert the data
print('inserting data')
index.upsert(items=zip(df.id, df.vector))

# Query the index and get similar vectors
print('querying data')
print(index.query(queries=[[0, 1]], top_k=3))

# Get index info
print('index info')
index.info()
print(index.info())

@app.route("/")
def index():
    return render_template("index.html")

