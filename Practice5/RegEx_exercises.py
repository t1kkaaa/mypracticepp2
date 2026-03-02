import re

# 1
def task1(text):
  if re.search("ab*", text):
    return "Found a match!"
  else:
    return "Not matched!"

# 2
def task2(text):
  if re.search("ab{2,3}", text):
    return "Found a match!"
  else:
    return "Not matched!"

# 3
def task3(text):
  return re.findall("[a-z]+_[a-z]+", text)

# 4
def task4(text):
  return re.findall("[A-Z][a-z]+", text)

# 5
def task5(text):
  if re.search("a.*b$", text):
    return "Found a match!"
  else:
    return "Not matched!"

# 6
def task6(text):
  return re.sub("[ ,.]", ":", text)

# 7
def task7(text):
  words = text.split('_')
  return "".join(x.title() for x in words)

# 8
def task8(text):
  return re.findall("[A-Z][^A-Z]*", text)

# 9
def task9(text):
  return re.sub(r"(\w)([A-Z])", r"\1 \2", text)

# 10
def task10(text):
  str1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
  return re.sub('([a-z0-9])([A-Z])', r'\1_\2', str1).lower()
