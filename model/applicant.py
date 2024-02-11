from education import Education
from experience import Experience

class Applicant:
  def __init__(self, 
               name: str, 
               age: int, 
               total_years_experince: int,
               education: Education,
               experiences: list[Experience],
               skills: list[str]) -> None:
    self.name = name
    self.age = age
    self.total_years_experince = total_years_experince
    self.education = education
    self.experiences = experiences
    self.skills = skills
    