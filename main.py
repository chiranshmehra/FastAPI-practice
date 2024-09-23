from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import uvicorn



app = FastAPI()


@app.get('/blog')
def index(limit = 10, published: bool = True):
    if published:
        return {'data': f'{limit} published blogs from the db'}
    else:
        return {'data': f'{limit} blogs form the db'}

@app.get('/blog/unpublished')
def unpublished():
    return {'data': 'unpublished'}
 


@app.get('/blog/{id}')
def showBlog(id: int):
    return {
        'data': id
    }


@app.get('/blog/{id}/comments')
def comments(id):

    return {'data':{'1','2'}}


class Blog(BaseModel):
    title: str
    body: str
    publishedAt: Optional[bool]



@app.post('/blog')
def createBlog(blog: Blog): 
    return {'data': f"Blog is created with title as {blog.title}"}



    