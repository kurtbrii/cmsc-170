import re

# TOKENIZE by splitting them into a single list
def readFile(file_name):
  f = open(file_name, "r")
  file = []
  lines = f.readlines()
  for line in lines:
    file.extend(line.split())
  return file

# removes non-alphaneumeric
def removeNonAlpha(item):
  if item != "":
    new_item = re.sub('[^a-z0-9]','', item)
    
  return new_item

def wordExists(words_dict, item):
  for i in range(len(words_dict)):
    if words_dict[i]["word"] == item:
      return i # returns the index so that the frequency of the element with that index will be incremented
  return -1

def outputFile(words_dict, file_name, words_counter):
  with open(file_name, 'w') as f:
    f.writelines(f"Dictionary Size: {len(words_dict)}\n")
    f.writelines(f"Total Number of Words: {words_counter}\n")
    f.writelines([f'{item["word"]}\t{item["frequency"]}\n' for item in words_dict])
  print("Output file successful")