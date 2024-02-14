class User:
  def __init__(self, username: str, hashed_password: str, name: str) -> None:
    self.username = username
    self.hashed_password = hashed_password
    self.name = name