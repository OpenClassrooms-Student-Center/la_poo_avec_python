class Agent():
  #country = "France"
  #gps = (7.605993, 37.941810)
  #agreeableness = 0.18949229496582184

  def __init__(self, **kwargs):
    for key, value in kwargs.items():
      setattr(self, key, value)

  @property
  def gps(self):
      return (self.longitude, self.latitude)
