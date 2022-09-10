def list_to_tuple(li):
  if (len(li) == 1):
    return f"({li[0]})"
  return f"{tuple(li)}"