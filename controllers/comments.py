from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.comment import CommentModel
from models.tea import TeaModel
from serializers.comment import CommentSchema
from typing import List
from database import get_db

router = APIRouter()

# get all comments for a specific tea
@router.get("/teas/{tea_id}/comments", response_model=List[CommentSchema])
def get_comments_for_tea(tea_id: int, db: Session = Depends(get_db)):
    tea = db.query(TeaModel).filter(TeaModel.id == tea_id).first()
    if not tea:
        raise HTTPException(status_code=404, detail="Tea not found")
    return tea.comments

# get single comment by id
@router.get("/comments/{comment_id}", response_model=CommentSchema)
def get_single_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.query(CommentModel).filter(CommentModel.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment

# add new comment to a tea
@router.post("/teas/{tea_id}/comments", response_model=CommentSchema, status_code=status.HTTP_201_CREATED)
def create_comment(tea_id: int, comment_data: dict, db: Session = Depends(get_db)):
    # Check if tea exists
    tea = db.query(TeaModel).filter(TeaModel.id == tea_id).first()
    if not tea:
        raise HTTPException(status_code=404, detail="Tea not found")
    
    new_comment = CommentModel(content=comment_data["content"], tea_id=tea_id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

# update comment by id
@router.put("/comments/{comment_id}", response_model=CommentSchema)
def update_comment(comment_id: int, comment_data: dict, db: Session = Depends(get_db)):
    db_comment = db.query(CommentModel).filter(CommentModel.id == comment_id).first()
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if "content" in comment_data:
        db_comment.content = comment_data["content"]

    db.commit()
    db.refresh(db_comment)
    return db_comment

# delete comment by id
@router.delete("/comments/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = db.query(CommentModel).filter(CommentModel.id == comment_id).first()
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    db.delete(db_comment)
    db.commit()
    return {"message": f"Comment with ID {comment_id} has been deleted"}