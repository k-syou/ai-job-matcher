from pydantic import BaseModel


class UserInfo(BaseModel):
    job_id: str
    skills: str
    experience_years: int
    is_entry_level: bool
    salary: str
    location: str
    benefits: str
    target_position: str
    certifications: str = ""
    languages: str = ""
