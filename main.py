from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import markdown
import os
import glob

app = FastAPI()
article_directory = "./articles"

templates = Jinja2Templates(directory="templates")

@app.get("/")
def get_index_page():
    return {}

def pack_content_list(file_list):
    result = {}
    for file_name in file_list:
        print(file_name)
        name_to_show = "/".join(file_name.split("/")[2:])[:-3]
        link = file_name[1:][:-3]

        result[name_to_show] = link
        
    return result

@app.get("/contents")
def get_contents_table(request: Request):
    file_list = glob.glob(f"{article_directory}/*.md") + glob.glob(f"{article_directory}/**/*.md")
    pack = pack_content_list(file_list)
    print(pack)
    return templates.TemplateResponse("contents.html", {"request": request, "file_list": pack})

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
