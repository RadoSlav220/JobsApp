from job import Job

class Recruiter:
  def __init__(self, 
               name: str, 
               company_name: str,
               jobs_posted: list[Job]) -> None:
    self.name = name
    self.company_name = company_name
    self.jobs_posted = jobs_posted
    