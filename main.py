from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import markdown

app = FastAPI()
article_directory = "./articles"

templates = Jinja2Templates(directory="templates")

@app.get("/")
def get_index_page():
    return {}

@app.get("/{name:path}/edit", name="path-convertor")
def get_article(request: Request, name: str):
    with open(f"{article_directory}/{name}") as f:
        content = f.read()
        return templates.TemplateResponse("edit.html", {"request": request, "name": name, "article": content})

def read_file(name, request):
    with open(f"{article_directory}/{name}") as f:
        content = markdown.markdown(f.read())
        return templates.TemplateResponse("article.html", {"request": request, "article": content})

@app.get("/{name:path}", name="path-convertor")
def get_article(request: Request, name: str):
    return read_file(name, request)

@app.post("/{name:path}", name="path-converter")
def post_article(request: Request, name: str, article: str=Form(...)):
    with open(f"{article_directory}/{name}", "w") as f:
        f.write(article)
    return read_file(name, request)
