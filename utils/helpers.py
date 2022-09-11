# To add in mysql query : [a,b,c] => (a, b, c)
def list_to_tuple(li):
  if (type(li) != list):
    raise TypeError("Invalid List Provided")
  if (len(li) == 1):
    return f"({li[0]})"
  return f"{tuple(li)}"

class Wrapper_For_Read():
  def __init__(self, blob):
    self.blob = blob
  def read(self, *args):
    return self.blob