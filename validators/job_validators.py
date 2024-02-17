from config import *


def validate_job_elements(title: str, company_name: str, description: str, 
                          salary_lower_bound: int, salary_upper_bound: int) -> None:
  validate_title(title)
  validate_company_name(company_name)
  validate_description(description)
  validate_salary_lower_bound(salary_lower_bound)
  validate_salary_upper_bound(salary_lower_bound, salary_upper_bound)


def validate_title(title: str) -> None:
  if title is None or title == '':
    raise ValueError('Missing job title.')
  
  if len(title) > JOB_TITLE_MAXIMUM_LENGTH:
    raise ValueError('Job title is too long')


def validate_company_name(company_name: str) -> None:
  if company_name is None or company_name == '':
    raise ValueError('Missing company name.')
  
  if len(company_name) > JOB_COMPANY_NAME_MAXIMUM_LENGTH:
    raise ValueError('Company name title is too long.')
  

def validate_description(description: str) -> None:
  if description is None or description == '':
    raise ValueError('Missing job description.')

  if len(description) > JOB_DESCRIPTION_MAXIMUM_LENGTH:
    raise ValueError('Job description is too long')


def validate_salary_lower_bound(salary_lower_bound: int) -> None:
  if salary_lower_bound is None:
    raise ValueError('Missing salary lower bound')
  
  try:
    salary_lower_bound = (int) (salary_lower_bound)
  except ValueError as e:
    raise ValueError('Job lower salary bound must be numeric')

  if salary_lower_bound < 0:
    raise ValueError('Job lower salary bound cannot be negative')


def validate_salary_upper_bound(salary_lower_bound: int, salary_upper_bound: int) -> None:
  if salary_upper_bound is None:
    raise ValueError('Missing salary upper bound')

  try:
    salary_upper_bound = (int) (salary_upper_bound)
  except ValueError as e:
    raise ValueError('Job upper salary bound must be numeric')

  if salary_upper_bound < 0:
    raise ValueError('Job upper salary bound cannot be negative')
  
  if salary_upper_bound < (int) (salary_lower_bound):
    raise ValueError('Job upper salary bound cannot be less than the lower bound.')