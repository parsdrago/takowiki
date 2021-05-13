from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import markdown
import os

app = FastAPI()
article_directory = "./articles"

templates = Jinja2Templates(directory="templates")

@app.get("/")
def get_index_page():
    return {}

def name_file(name):
    return f"{article_directory}/{name}.md"

def create_new_article_file(name):
    directories = name.split("/")
    path_so_far = "" 
    for directory in directories[:-1]:
        path_so_far += directory + "/"
        if not os.path.isdir(path_so_far):
            os.mkdir(path_so_far)

    if not os.path.isfile(name):
        open(name, "a")

@app.get("/articles/{name:path}/edit", name="path-convertor")
def get_article(request: Request, name: str):
    file_name = name_file(name)

    create_new_article_file(file_name)

    with open(file_name) as f:
        content = f.read()
        return templates.TemplateResponse("edit.html", {"request": request, "name": name, "article": content})

def read_file(name, request):
    with open(name_file(name)) as f:
        content = markdown.markdown(f.read())
        return templates.TemplateResponse("article.html", {"request": request, "name": name, "article": content})

@app.get("/articles/{name:path}", name="path-convertor")
def get_article(request: Request, name: str):
    return read_file(name, request)

@app.post("/articles/{name:path}", name="path-converter")
def post_article(request: Request, name: str, article: str=Form(...)):
    with open(name_file(name),"w") as f:
        f.write(article)
    return read_file(name, request)
