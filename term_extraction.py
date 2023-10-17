from resource_import import *

# Here we specify the file we want to load.
filename = pathlib.Path("./data/fhir/Aaron697_Brekke496_2fa15bc7-8866-461a-9000-f739e425860a.json")
bundle = Bundle.parse_file(filename)

fhir_dict = {}  # Initialize an empty dictionary

# Iterate through bundle entries
for entry in bundle.entry:
    resource = entry.resource
    # Check if the resource is of any of the specified types
    if isinstance(resource, (Patient, CarePlan, CareTeam, Condition, Encounter, ImagingStudy, Immunization, MedicationRequest, Procedure)):
        # Determine the resource type
        resource_type = resource.__class__.__name__  # Get the class name as a string
        # Store the resource in the dictionary using the resource type as the key
        fhir_dict[resource_type] = resource

# Now, fhir_dict contains the filtered resources
# print(fhir_dict)

filtered_fhir_dict = {key: value for key, value in fhir_dict.items() if fhir_dict.items() is not None}

for key, value in filtered_fhir_dict.items():
  print(key, str(value))

#pattern = r'\w+\s*=\s*None,*? '
# f = 'dictFile.txt'

# def writeDict(fhir_dict, f):
#     with open(f, "w") as file:
#         for key, value in fhir_dict.items():
#             file.write(key + ", " + str(value) + "\n")

# writeDict(fhir_dict, f)


# Open and read the file
with open("dictFile.txt", "r") as file:
    for line in file:
        # Split each line by the '=' character
        parts = line.strip().split(",")
        
        # Check if the line has a valid key-value pair
        if len(parts) < 1:
            key, value = parts
            filtered_fhir_dict[key] = value

# Print the loaded dictionary
print(filtered_fhir_dict)

# This code here creates a set of all the different kinds of resources in the
# bundle.
fhir_types = set()
for entry in bundle.entry:
  words_to_exclude = ['Claim', 'ExplanationOfBenefit']
  fhir_types.add(entry.resource.resource_type)
  fhir_types = fhir_types - set(words_to_exclude)
  for entry_key in fhir_types:
    if entry_key == bundle.entry:
      fhir_dict[entry_key] = str(entry.resourse)

# print(fhir_types)
# print(fhir_dict)



# print(type(bundle)) # is fhir.resources.R4B.bundle.Bundle
# print(type(filename)) # pathlib.PosixPath
# print(eobs) # is a list

# pattern = re.compile(fhir_types)
# fhir_dict = json.loads(bundle)

# words_to_exclude='''
#   t
# '''

# bundle_dict = bundle.entry.dict()
# # eobs_dict = eobs.dict()
# pattern = re.compile(words_to_exclude)
# # matches = pattern.finditer(bundle_dict)
# # Use regular expression to filter values by pattern
# filtered_data = {key: value for key, value in bundle_dict.items() if key.startswith('t')}

# # Print filtered data
# print(filtered_data)

'''
for res_type in matches:
  print(res_type)

# excluded_words = [ i for i in words if not re.findall(r'\d', i ) ]


# Regular expression pattern to match email addresses
email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

# Use regular expression to filter values by pattern
filtered_data = {key: value for key, value in data.items() if re.search(email_pattern, value)}

# Print filtered data
print(filtered_data)
'''
