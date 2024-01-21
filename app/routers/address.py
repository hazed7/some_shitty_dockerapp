from fastapi import APIRouter, Depends, HTTPException, status
from ..schemas.address import AddressSchema
from ..dependencies import get_database
from psycopg2.extras import RealDictCursor
import uuid

router = APIRouter()

@router.post("/addresses/", response_model=AddressSchema, status_code=status.HTTP_201_CREATED)
def create_address(address: AddressSchema, db=Depends(get_database)):
    cursor = db.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
        INSERT INTO addresses (person_id, address)
        VALUES (%s, %s) RETURNING *;
        """, (str(address.person_id), address.address))
    new_address = cursor.fetchone()
    db.commit()
    cursor.close()
    if not new_address:
        raise HTTPException(status_code=400, detail="Error creating address")
    return new_address

@router.get("/addresses/{address_id}", response_model=AddressSchema)
def get_address(address_id: uuid.UUID, db=Depends(get_database)):
    cursor = db.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM addresses WHERE address_id = %s;", (str(address_id),))
    address = cursor.fetchone()
    cursor.close()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address

@router.put("/addresses/{address_id}", response_model=AddressSchema)
def update_address(address_id: uuid.UUID, address: AddressSchema, db=Depends(get_database)):
    cursor = db.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
        UPDATE addresses SET person_id = %s, address = %s
        WHERE address_id = %s RETURNING *;
        """, (str(address.person_id), address.address, str(address_id)))
    updated_address = cursor.fetchone()
    db.commit()
    cursor.close()
    if not updated_address:
        raise HTTPException(status_code=404, detail="Address not found")
    return updated_address

@router.delete("/addresses/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_address(address_id: uuid.UUID, db=Depends(get_database)):
    cursor = db.cursor()
    cursor.execute("DELETE FROM addresses WHERE address_id = %s RETURNING address_id;", (str(address_id),))
    deleted_id = cursor.fetchone()
    db.commit()
    cursor.close()
    if not deleted_id:
        raise HTTPException(status_code=404, detail="Address not found")
    return {"message": "Address deleted successfully"}
