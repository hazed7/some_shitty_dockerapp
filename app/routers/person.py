from fastapi import APIRouter, Depends, HTTPException, status
from ..schemas.person import PersonSchema
from ..dependencies import get_database
from psycopg2.extras import RealDictCursor
import uuid

router = APIRouter()

@router.post("/persons/", response_model=PersonSchema, status_code=status.HTTP_201_CREATED)
def create_person(person: PersonSchema, db=Depends(get_database)):
    cursor = db.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
        INSERT INTO persons (full_name, phone_number, date_of_birth, consent_to_personal_data)
        VALUES (%s, %s, %s, %s) RETURNING *;
        """, (person.full_name, person.phone_number, person.date_of_birth, person.consent_to_personal_data))
    new_person = cursor.fetchone()
    db.commit()
    cursor.close()
    return new_person

@router.get("/persons/{person_id}", response_model=PersonSchema)
def get_person(person_id: uuid.UUID, db=Depends(get_database)):
    cursor = db.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM persons WHERE person_id = %s;", (str(person_id),))
    person = cursor.fetchone()
    cursor.close()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person

@router.put("/persons/{person_id}", response_model=PersonSchema)
def update_person(person_id: uuid.UUID, person: PersonSchema, db=Depends(get_database)):
    cursor = db.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
        UPDATE persons SET full_name = %s, phone_number = %s, date_of_birth = %s, consent_to_personal_data = %s
        WHERE person_id = %s RETURNING *;
        """, (person.full_name, person.phone_number, person.date_of_birth, person.consent_to_personal_data, str(person_id)))
    updated_person = cursor.fetchone()
    db.commit()
    cursor.close()
    if not updated_person:
        raise HTTPException(status_code=404, detail="Person not found")
    return updated_person

@router.delete("/persons/{person_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_person(person_id: uuid.UUID, db=Depends(get_database)):
    cursor = db.cursor()
    cursor.execute("DELETE FROM persons WHERE person_id = %s RETURNING person_id;", (str(person_id),))
    deleted_id = cursor.fetchone()
    db.commit()
    cursor.close()
    if not deleted_id:
        raise HTTPException(status_code=404, detail="Person not found")
    return {"message": "Person deleted successfully"}