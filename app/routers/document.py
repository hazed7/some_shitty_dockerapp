from fastapi import APIRouter, Depends, HTTPException, status
from ..schemas.document import DocumentSchema
from ..dependencies import get_database
from psycopg2.extras import RealDictCursor
import uuid

router = APIRouter()

@router.post("/documents/", response_model=DocumentSchema, status_code=status.HTTP_201_CREATED)
def create_document(document: DocumentSchema, db=Depends(get_database)):
    cursor = db.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
        INSERT INTO documents (person_id, document_type, start_date, end_date)
        VALUES (%s, %s, %s, %s) RETURNING *;
        """, (str(document.person_id), document.document_type, document.start_date, document.end_date))
    new_document = cursor.fetchone()
    db.commit()
    cursor.close()
    if not new_document:
        raise HTTPException(status_code=400, detail="Error creating document")
    return new_document

@router.get("/documents/{document_id}", response_model=DocumentSchema)
def get_document(document_id: uuid.UUID, db=Depends(get_database)):
    cursor = db.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM documents WHERE document_id = %s;", (str(document_id),))
    document = cursor.fetchone()
    cursor.close()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document

@router.put("/documents/{document_id}", response_model=DocumentSchema)
def update_document(document_id: uuid.UUID, document: DocumentSchema, db=Depends(get_database)):
    cursor = db.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
        UPDATE documents SET person_id = %s, document_type = %s, start_date = %s, end_date = %s
        WHERE document_id = %s RETURNING *;
        """, (str(document.person_id), document.document_type, document.start_date, document.end_date, str(document_id)))
    updated_document = cursor.fetchone()
    db.commit()
    cursor.close()
    if not updated_document:
        raise HTTPException(status_code=404, detail="Document not found")
    return updated_document

@router.delete("/documents/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(document_id: uuid.UUID, db=Depends(get_database)):
    cursor = db.cursor()
    cursor.execute("DELETE FROM documents WHERE document_id = %s RETURNING document_id;", (str(document_id),))
    deleted_id = cursor.fetchone()
    db.commit()
    cursor.close()
    if not deleted_id:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"message": "Document deleted successfully"}
