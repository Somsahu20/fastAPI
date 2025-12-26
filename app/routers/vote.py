from .. import models
from ..schema import VoteGive, Vote, VoteResponse
from fastapi import APIRouter, Depends, HTTPException, Response
from ..utils import get_db
from sqlalchemy.orm import Session
from sqlalchemy import insert, select
from ..oauth import get_current_user
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from typing import List

router = APIRouter()

@router.get('/get/votes', response_model=List[VoteResponse])
def get_all_votes(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):

    try:
        stmt = select(models.Vote).where(models.Vote.user_id == user.id)
        
        result = db.execute(stmt).scalars().all()

        return result


    except Exception as err:
        print("Error in get_all_votes")
        print("Error is ", err)
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='Error in get_all_votes')

@router.post('/vote')
def cast_vote(vote: VoteGive, res: Response, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):

    
    
    try:
        p_id = vote.post_id

        check1 = select(models.Posts).where(models.Posts.id == p_id)
        check1_res = db.execute(check1).scalar_one_or_none()

        if check1_res is not None:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f'There is no post with id {p_id}')
        
        if vote.direction == 1:
            check_query = select(models.Vote).where(models.Vote.post_id == vote.post_id, models.Vote.user_id == user.id)
            check_res = db.execute(check_query).scalar_one_or_none()
            if check_res is not None:
                raise HTTPException(status_code=HTTP_409_CONFLICT, detail='User has already liked the post')

            vote_dict = vote.model_dump()
            vote_dict.pop("direction")
            vote_dict.update({"user_id": user.id})

            new_vote = models.Vote(**vote_dict)
            db.add(new_vote)
            db.commit()
            # res.status_code = HTTP_201_CREATED
            db.refresh(new_vote)
            return {"message": "successfully liked"}
        
        else:

            check_query = select(models.Vote).where(models.Vote.user_id == user.id, models.Vote.post_id == vote.post_id)
            check_res = db.execute(check_query).scalar_one_or_none()

            if check_res is None:
                raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='There is no such post liked by the user')

            # Delete the existing vote that was fetched from the database
            db.delete(check_res)
            db.commit()

            # res.status_code = HTTP_204_NO_CONTENT
            return {"message": "Successfully unliked"}
    except Exception as err:

        print("Error at cast_vote")
        print("error is ", err)
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='Error in casting vote')
    
