from experience import Experience
from education import Education
from application import Application

class Job:
  def __init__(self, 
               description: str, 
               required_skills: list[str],
               required_experiences: list[Experience], 
               required_education: Education,
               salary_lower_bound: int,
               salary_upper_bound: int,
               applications: list[Application]) -> None:
    self.description = description
    self.required_skills = required_skills
    self.required_experiences = required_experiences
    self.required_education = required_education
    self.salary_lower_bound = salary_lower_bound
    self.salary_upper_bound = salary_upper_bound
    self.applications = applications