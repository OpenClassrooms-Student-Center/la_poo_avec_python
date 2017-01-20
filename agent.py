class Agent():
  #country = "France"
  #latitude = 7.605993
  #longitude = 37.941810
  #agreeableness = 0.18949229496582184

  def __init__(self, **kwargs):
    for key, value in kwargs.items():
      setattr(self, key, value)