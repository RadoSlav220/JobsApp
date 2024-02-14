from user import User
from job import Job

class Recruiter(User):
  def __init__(self, 
               username: str,
               hashed_password: str,
               name: str, 
               company_name: str,
               jobs_posted: list[Job]) -> None:
    super().__init__(username, hashed_password, name)
    self.company_name = company_name
    self.jobs_posted = jobs_posted