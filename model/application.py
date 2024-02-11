import datetime
from applicant import Applicant

class Application:
  def __init__(self, applicant: Applicant, date: datetime.date) -> None:
    self.applicant = applicant
    self.date = date