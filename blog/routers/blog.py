from fastapi import APIRouter, Depends, HTTPException, status, Response
from typing import List
from sqlalchemy.orm import Session
from .. import schemas, database, models


router = APIRouter()
getDb = database.getDb

@router.get('/blog', response_model=List[schemas.ShowBlog], tags=['blogs'])
def getBlogs(db: Session = Depends(database.getDb)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.post('/blog', status_code=status.HTTP_200_OK, tags=['blogs'])
def createBlog(request: schemas.Blog, db: Session = Depends(getDb)):
    newBlog = models.Blog(title=request.title, body=request.body, userId=1)
    db.add(newBlog)
    db.commit()
    db.refresh(newBlog)
    return newBlog

@router.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])
def destroyBlog(id, db: Session = Depends(getDb)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog is not available please enter the valid blog id") 
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return 'Done'

@router.put('/blog/{id}', status_code=status.HTTP_200_OK, tags=['blogs'])
def updateBlog(id, request: schemas.Blog, db: Session = Depends(getDb)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog is not available please enter the valid blog id")
    blog.updated(request)
    db.commit()
    #db.query(models.Blog).add_column('Author')
    #db.commit()
    return 'Updated'

#@router.get('/blog', response_model=List[schemas.ShowBlog], tags=['blogs'])
#def getBlogs(response: Response, db: Session = Depends(getDb)):
#    blogs = db.query(models.Blog).all()
#    return blogs


@router.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog, tags=['blogs'])
def getBlogById(id,response: Response, db: Session = Depends(getDb)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id {id} is not available')
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {'detail':f'Blog with the id {id} is not available'}
    return blog