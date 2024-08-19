from pydantic import BaseModel

# Define schemas for API request and response bodies
class ItemCreate(BaseModel):
    name: str
    description: str
    # ... other fields

class ItemResponse(BaseModel):
    id: str
    name: str
    description: str
    # ... other fields