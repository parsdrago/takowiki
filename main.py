from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
article_directory = "./articles"

templates = Jinja2Templates(directory="templates")

@app.get("/")
def get_index_page():
    return {}

@app.get("/{name:path}", name="path-convertor")
def get_article(request: Request, name: str):
    with open(f"{article_directory}/{name}") as f:
        return templates.TemplateResponse("article.html", {"request": request, "article": f.read()})
