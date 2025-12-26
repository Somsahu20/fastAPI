from sqlalchemy.engine.row import Row
from app.models import Posts
from token import OP
from turtle import delay
from fastapi import FastAPI, Depends, Response, status, HTTPException, APIRouter
from typing import Optional, List
from fastapi.params import Body
from psycopg2.extras import RealDictCursor
import psycopg2, time
from sqlalchemy.orm import Session
from sqlalchemy import select, update, func
from .. import models, schema
from .. import oauth
from starlette.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND, HTTP_201_CREATED
from ..utils import get_db
from json import dumps

router = APIRouter()

while True:
    try:
        con = psycopg2.connect(host='localhost', database='fastapiDb', user='postgres', password='20102004', cursor_factory=RealDictCursor)
        # curr = con.cursor()

        # curr.execute("select * from posts")
        # obj = curr.fetchall()
        # print(obj)
        break
    except Exception as err:
        print("Connection to server failed")
        print(f"Error is {err}")
        time.sleep(5)

# @router.get('/') #? decorator provides it to become an important function. Used to change function's behaviour
# async def root():
#     return {"message": "Hello World"}

@router.get('/alchemy')
def get_post(db: Session = Depends(get_db)):
    
    return {"message": "Success"}

# def create(payload: dict = Body(...)):
#     print(payload)
#     return {"name": f"{payload["Name"]}",
#             "surname": f"{payload["Surname"]}"}

def boolConvert(b: str) -> bool:

    if not b:
        return False

    b = b.strip().lower()
    
    if b == "true":
        return True
    elif b == "false":
        return False
    else:
        return None

@router.get('/posts')
def get_posts():
    #! fetchone() to be used if and only if we want only one tuple. For eg. if we want to find a tuple with that id
    cursor = con.cursor()
    cursor.execute('select * from posts')
    data = cursor.fetchall()
    
    return data


@router.get('/alchemy/posts', response_model=List[schema.PostResponse]) #? We use list here beause we are returning an array
def get_post_al(db: Session = Depends(get_db), u: models.User = Depends(oauth.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = None):

    try:
        stmt = select(models.Posts).where(u.id == models.Posts.user_id, models.Posts.name.like('%'+search+ '%')).offset(skip) #! Make the query
        results = db.execute(stmt).scalars().fetchmany(limit); #! Execute the query
        return results
    except Exception as err:
        print("Error at alchemy get")
        print("Error is ", err)
        raise HTTPException(status_code=404, detail='Error in getting posts')

@router.get('/get/posts/votes/', response_model=List[schema.PostOut])
def get_votes_from_posts(db: Session = Depends(get_db), u: models.User = Depends(oauth.get_current_user)):

    try:
        stmt = select(models.Posts, func.count(models.Vote.post_id).label("votes")).select_from(models.Posts).join(models.Vote, models.Posts.id == models.Vote.post_id).group_by(models.Posts.id)

        result = db.execute(stmt).all()

        li = []

        for res in result:

            post = res[0]
            votes = res[1]
            new_op = schema.PostOut(Post=schema.PostResponse.model_validate(post), votes=votes)
            li.append(new_op)
        

        # Convert Row objects to dictionaries
        # data = []
        # for row in result:
        #     post = row[0]  # Posts model instance
        #     votes = row[1]  # vote count
        #     post_dict = {
        #         "id": post.id,
        #         "name": post.name,
        #         "surname": post.surname,
        #         "is_married": post.is_married,
        #         "created_at": post.created_at,
        #         "user_id": post.user_id,
        #         "votes": votes
        #     }
        #     data.append(post_dict

        return li


    except Exception as err:
        print("Error in post vote join")
        print("Error is", err)
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='Couldn\'t retrieve the post and votes together')



@router.post('/create', status_code=status.HTTP_201_CREATED)
def create(post: schema.Post, res: Response):
    # print(post)
    postDict = post.model_dump()
    # # print(post.model_dump())
    # my_posts.append(postDict)
    # print(f"The status code sent is {res.status_code}")
    # return {"data": postDict}

    name = postDict.get("name")
    surname = postDict.get("surname")
    married = postDict.get("is_married")  #? Already a boolean from Pydantic model


    try:
        cursor = con.cursor()
        cursor.execute('insert into posts (name, surname, is_married) values (%s, %s, %s)', (name, surname, married)) #? %s protects us from sql injection. So never ever directly put variables in the query
        con.commit()  #! Don't forget to commit the transaction!
        return {"message": "Inserting op was successful"}
    except Exception as err:
        print("Error at create")
        print("Error is ", err)
        raise HTTPException(status_code=404, detail='Error in adding tuple') 

@router.post('/alchemy/create', status_code=HTTP_201_CREATED, response_model=schema.PostResponse)
def al_create(post: schema.Post, db: Session = Depends(get_db), u: models.User = Depends(oauth.get_current_user)):
    try:
        # new_post = models.Posts(name=post.name, surname=post.surname, is_married=post.is_married)
        # db.add(new_post)
        # db.commit()
        # db.refresh(new_post)
        user_id = u.id
        post_dict = post.model_dump()
        post_dict.update({'user_id': user_id})
        new_post = models.Posts(**post_dict)
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post
    except Exception as err:
        print("Error at alchemy create")
        print("Error is", err)
        raise HTTPException(status_code=404, detail='Couldn\'t add the post')




@router.get("/posts/{id}")
def get_posts(id: int, res: Response):
    
    #! id : int -> ensures that id is an integer and not some random text

    # found: bool = False

    # for p in my_posts:
    #     if p['id'] == id:
    #         found = True
    #         return {"data": p}
        
    # if not found:
    #     raise HTTPException(status_code=404, detail=f"ID not found for {id}")

    cursor = con.cursor()
    cursor.execute(""" select * from posts where id = (%s) """, (id,)) #! id, this comma is necessary as just (id) equals id an integer. But (id,) makes it a tuple. Psycopg2 expects a tuple
    data = cursor.fetchone()

    if data:
        res.status_code = HTTP_200_OK
        return data
    else:
        raise HTTPException(status_code=404, detail=f'Post with id: {id} not found')


@router.get('/alchemy/posts/{id}', response_model=schema.PostResponse)
def get_post_alchemy(id: int, db: Session = Depends(get_db), u: models.User = Depends(oauth.get_current_user)):

    try:
        stmt = select(models.Posts).where(models.Posts.id == id)
        p = db.execute(stmt).scalar_one()
        return p
    except Exception as err:
        print("Error at get post by id using orm")
        print("Error is", err)
        raise HTTPException(status_code=403, detail='Error retrieve post by id')
    

@router.get('/get/posts/votes/{id}', response_model=schema.PostOut)
def get_by_id(id: int, db: Session = Depends(get_db), user = Depends(oauth.get_current_user)):

    try:
        stmt = select(models.Posts, func.count(models.Vote.post_id).label("votes")).select_from(models.Posts).join(models.Vote, models.Posts.id == models.Vote.post_id).where(models.Posts.id == id).group_by(models.Posts.id)

        result = db.execute(stmt).one()
        post = result[0]
        vote = result[1]

        new_op = schema.PostOut(Post=schema.PostResponse.model_validate(post), votes=vote)
        return new_op
    except Exception as error:
        print("Error in get_by_id")
        print("Error is", error)
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='Could not find post and votes by post\'s id')


@router.delete('/delete/{id}')
def delete_post(id: int, res: Response):

    # idx = -1

    # for ind, p in enumerate(my_posts):
    #     if p["id"] == id:
    #         idx = ind
    #         break

    # if idx != -1:
    #     my_posts.pop(idx)
    #     res.status_code = status.HTTP_204_NO_CONTENT
    #     return {"message": f"Successfully deleted post with id: {id}"}
    # else:
    #     raise HTTPException(status_code=404, detail=f"Post not found with id {id}")

    try:
        cursor = con.cursor()
        cursor.execute(""" delete from posts where id = (%s) returning * """, (id, ))

        data = cursor.fetchone()
        con.commit()

        

        res.status_code = HTTP_204_NO_CONTENT
        return data

    except Exception as err:
        print("Error at delete post")
        print("Error is", err)
        raise HTTPException(status_code=404, detail="Couldn't be deleted")


@router.delete('/alchemy/del/{id}', status_code=status.HTTP_204_NO_CONTENT)
def alchemy_delete(id: int, db: Session = Depends(get_db), u: models.User = Depends(oauth.get_current_user)):

    stmt = select(models.Posts).where(models.Posts.id == id)
    p = db.execute(stmt).scalar_one()

    if not p:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id: {id} not found')

    if p.user_id != u.id:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail='Can\'t allow to delete the post')

    db.delete(p)
    db.commit()

    return None
    


@router.put('/update/{id}', status_code=status.HTTP_200_OK)
def update_post(id: int, post: schema.Post, res: Response):

    # idx = -1

    # for ind, p in enumerate( my_posts):
    #     if p['id'] == id:
    #         idx = ind
    #         break

    # if idx != -1:
    #     up_post = post.model_dump()
    #     my_posts[idx] = up_post
    #     return {"data": up_post}
    # else:
    #     print("No found")
    #     raise HTTPException(status_code=404, detail=f"No post with id {id}")

    try:
        cursor = con.cursor()
        cursor.execute(""" update posts set name = (%s), surname = (%s), is_married = (%s) where id = (%s) returning * """, (post.name, post.surname, post.is_married, id))

        con.commit()

        data = cursor.fetchone()
        res.status_code = HTTP_200_OK
        return data


    except Exception as err:
        print("Error at update post")
        print("Error is", err)
        raise HTTPException(status_code=404, detail=f'Posts with id {id} not found')


@router.put('/alchemy/update/{id}', status_code=status.HTTP_200_OK, response_model=schema.PostResponse)
def alchemy_update(id: int, post: schema.Post, db: Session = Depends(get_db), u: models.User = Depends(oauth.get_current_user)):

    

    post_dict = post.model_dump()
    post_dict.update({"user_id": u.id})


    query = select(models.Posts).where(models.Posts.id == id)
    og_p = db.execute(query).scalar_one()

    if not og_p:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post with id: {id}not found')

    if og_p.user_id != u.id:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail='Not allowed to change the post')

    stmt = update(models.Posts).where(models.Posts.id == id).values(**post_dict).returning(models.Posts)
    p = db.execute(stmt).scalar_one()

    db.commit()
    return p


    # except Exception as err:
    #     print("Error at update alchemy")
    #     print("Error is", err)
    #     db.rollback()
    #     raise HTTPException(status_code=404, detail='Error in updating the post')