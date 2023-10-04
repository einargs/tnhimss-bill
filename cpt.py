import pathlib
import random

cpt_path = pathlib.Path("./data/pruned-cpt.txt")

cpt_codes = {}

with open(cpt_path) as file:
  for line in file:
    if line:
      obj = line.split('\t', 1)
      (code, desc) = obj
      cpt_codes[code] = desc.strip()

cpt_keys = list(cpt_codes.keys())

def get_random_code():
  code = random.choice(cpt_keys)
  return (code, cpt_codes[code])

def get_random_codes(num):
  return [get_random_code() for _ in range(num)]

print(get_random_codes(6))
