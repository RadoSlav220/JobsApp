from enums.education_field import EducationField
from enums.education_level import EducationLevel

class Education:
  def __init__(self, field: EducationField, level: EducationLevel) -> None:
    self.field = field
    self.level = level