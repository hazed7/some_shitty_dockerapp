from fastapi import APIRouter, Depends, HTTPException, status
from ..schemas.work_experience import WorkExperienceSchema
from ..dependencies import get_database
from psycopg2.extras import RealDictCursor
import uuid

router = APIRouter()

@router.post("/work_experience/", response_model=WorkExperienceSchema, status_code=status.HTTP_201_CREATED)
def create_work_experience(work_experience: WorkExperienceSchema, db=Depends(get_database)):
    cursor = db.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
        INSERT INTO work_experience (person_id, company_name, job_title, start_date, end_date, rate_worked)
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING *;
        """, (str(work_experience.person_id), work_experience.company_name, work_experience.job_title, work_experience.start_date, work_experience.end_date, work_experience.rate_worked))
    new_work_experience = cursor.fetchone()
    db.commit()
    cursor.close()
    if not new_work_experience:
        raise HTTPException(status_code=400, detail="Error creating work experience")
    return new_work_experience

@router.get("/work_experience/{experience_id}", response_model=WorkExperienceSchema)
def get_work_experience(experience_id: uuid.UUID, db=Depends(get_database)):
    cursor = db.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM work_experience WHERE experience_id = %s;", (str(experience_id),))
    work_experience = cursor.fetchone()
    cursor.close()
    if not work_experience:
        raise HTTPException(status_code=404, detail="Work experience not found")
    return work_experience

@router.put("/work_experience/{experience_id}", response_model=WorkExperienceSchema)
def update_work_experience(experience_id: uuid.UUID, work_experience: WorkExperienceSchema, db=Depends(get_database)):
    cursor = db.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
        UPDATE work_experience SET person_id = %s, company_name = %s, job_title = %s, start_date = %s, end_date = %s, rate_worked = %s
        WHERE experience_id = %s RETURNING *;
        """, (str(work_experience.person_id), work_experience.company_name, work_experience.job_title, work_experience.start_date, work_experience.end_date, work_experience.rate_worked, str(experience_id)))
    updated_work_experience = cursor.fetchone()
    db.commit()
    cursor.close()
    if not updated_work_experience:
        raise HTTPException(status_code=404, detail="Work experience not found")
    return updated_work_experience

@router.delete("/work_experience/{experience_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_work_experience(experience_id: uuid.UUID, db=Depends(get_database)):
    cursor = db.cursor()
    cursor.execute("DELETE FROM work_experience WHERE experience_id = %s RETURNING experience_id;", (str(experience_id),))
    deleted_id = cursor.fetchone()
    db.commit()
    cursor.close()
    if not deleted_id:
        raise HTTPException(status_code=404, detail="Work experience not found")
    return {"message": "Work experience deleted successfully"}
