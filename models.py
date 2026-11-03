from pydantic import BaseModel, Field, field_validator


class Student(BaseModel):
    name: str = Field(min_length=2)
    department: str = Field(min_length=2)
    email: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        if "@" not in value or "." not in value.split("@")[-1]:
            raise ValueError("Invalid email address")
        return value