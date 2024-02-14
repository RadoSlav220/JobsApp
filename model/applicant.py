from education import Education
from experience import Experience

from user import User

class Applicant(User):
  def __init__(self, 
               username: str,
               hashed_password: str,
               name: str,
               total_years_experince: int,
               education: Education,
               experiences: list[Experience],
               skills: list[str]) -> None:
    super().__init__(username, hashed_password, name)
    self.total_years_experince = total_years_experince
    self.education = education
    self.experiences = experiences
    self.skills = skills
    