from pydantic import BaseModel

# Define Pydantic models for data validation
class Item(BaseModel):
    id: str
    name: str
    description: str
    # ... other fields