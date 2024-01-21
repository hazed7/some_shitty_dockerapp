from fastapi import APIRouter, Depends, HTTPException, status
from ..schemas.relative import RelativeSchema
from ..dependencies import get_database
from psycopg2.extras import RealDictCursor
import uuid

router = APIRouter()

@router.post("/relatives/", response_model=RelativeSchema, status_code=status.HTTP_201_CREATED)
def create_relative(relative: RelativeSchema, db=Depends(get_database)):
    cursor = db.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
        INSERT INTO relatives (person_id, relative_name, relation_type)
        VALUES (%s, %s, %s) RETURNING *;
        """, (str(relative.person_id), relative.relative_name, relative.relation_type))
    new_relative = cursor.fetchone()
    db.commit()
    cursor.close()
    if not new_relative:
        raise HTTPException(status_code=400, detail="Error creating relative")
    return new_relative

@router.get("/relatives/{relative_id}", response_model=RelativeSchema)
def get_relative(relative_id: uuid.UUID, db=Depends(get_database)):
    cursor = db.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM relatives WHERE relative_id = %s;", (str(relative_id),))
    relative = cursor.fetchone()
    cursor.close()
    if not relative:
        raise HTTPException(status_code=404, detail="Relative not found")
    return relative

@router.put("/relatives/{relative_id}", response_model=RelativeSchema)
def update_relative(relative_id: uuid.UUID, relative: RelativeSchema, db=Depends(get_database)):
    cursor = db.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
        UPDATE relatives SET person_id = %s, relative_name = %s, relation_type = %s
        WHERE relative_id = %s RETURNING *;
        """, (str(relative.person_id), relative.relative_name, relative.relation_type, str(relative_id)))
    updated_relative = cursor.fetchone()
    db.commit()
    cursor.close()
    if not updated_relative:
        raise HTTPException(status_code=404, detail="Relative not found")
    return updated_relative

@router.delete("/relatives/{relative_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_relative(relative_id: uuid.UUID, db=Depends(get_database)):
    cursor = db.cursor()
    cursor.execute("DELETE FROM relatives WHERE relative_id = %s RETURNING relative_id;", (str(relative_id),))
    deleted_id = cursor.fetchone()
    db.commit()
    cursor.close()
    if not deleted_id:
        raise HTTPException(status_code=404, detail="Relative not found")
    return {"message": "Relative deleted successfully"}
