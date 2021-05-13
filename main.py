from fastapi import FastAPI

app = FastAPI()
article_directory = "./articles"

@app.get("/")
def get_index_page():
    return {}

@app.get("/{name:path}", name="path-convertor")
def get_article(name):
    with open(f"{article_directory}/{name}") as f:
            return f.read()
