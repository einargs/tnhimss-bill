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

# for key, value in filtered_fhir_dict.items():
  # print(key, str(value))

#pattern = r'\w+\s*=\s*None,*? '
# f = 'dictFile.txt'

# def writeDict(fhir_dict, f):
#     with open(f, "a") as file:
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

# for key in filtered_fhir_dict.keys():
#    for value in filtered_fhir_dict.values():
#       if 

# word = 'Extension'
# if word in filtered_fhir_dict.values():
# # Print the loaded dictionary
#    print(f"The value '{word}' is in the dictionary.")
# else:
#     print(f"The value '{word}' is not in the dictionary.")
exp = r'\w.+'
to_include = (('language', exp), ('modifierExtension', exp), ('active', exp),
               ('contact', exp), ('deceasedBoolean', exp), ('deceasedDateTime', exp), ('gender', r'(male|female)'), 
               ('generalPractitioner', exp), ('managingOrganization', exp), ('multipleBirthBoolean', r'(False|True)'),
               ('multipleBirthInteger', exp), ('appointment', exp), ('diagnosis', exp), ('episodeOfCare', exp),
               ('hospitalization', exp), ('identifier', exp), ('length', exp), ('location', exp), ('partOf', exp),
               ('priority', exp), ('reasonReference', exp), ('serviceType', exp), ('status', 'finished'), ('statusHistory', exp),
               ('abatementAge', exp), ('asserter', exp), ('bodySite', exp), ('category', exp), ('evidence', exp),
               ('identifier', exp), ('note', exp), ('onsetAge', exp), ('recorder', exp), ('severity', exp), ('stage', exp),
               ('reasonReference', exp), ('status', exp), ('telecom', exp), ('author', exp), ('contributor', exp), 
               ('created', exp), ('description', exp), ('goal', exp), ('identifier', exp), ('intent', exp), ('replaces', exp),
               ('status', exp), ('supportingInfo', exp), ('title', exp), ('doseQuantity', exp), ('education', exp),
               ('expirationDate', exp), ('fundingSource', exp), ('identifier', exp), ('isSubpotent', exp), ('location', exp),
               ('lotNumber', exp), ('manufacturer', exp), ('note', exp), ('performer', exp), ('programEligibility', exp),
               ('protocolApplied', exp), ('reaction', exp), ('reasonCode', exp), ('reasonReference', exp),
               ('recorded', exp), ('status', exp), ('statusReason', exp), ('subpotentReason', exp), 
               ('complication', exp), ('complicationDetail', exp), ('focalDevice', exp), ('followUp', exp), ('identifier', exp),
               ('location', exp), ('note', exp), ('outcome', exp), ('partOf', exp), ('performedAge', exp), ('performedDateTime', exp),
               ('category', exp), ('courseOfTherapyType', exp), ('detectedIssue', exp), ('dispenseRequest', exp), ('doNotPerform', exp),
               ('eventHistory', exp), ('groupIdentifier', exp), ('substitution', exp), ('supportingInformation', exp)
               )
print(type(to_include))
# list_include = list()
# for item in to_include:
#    list_include.append(str(item))
#     matches = re.findall(exp, values)
   
def recursive_parser(data, fields):
    if isinstance(data, dict):
        for key, value in data.items():
          print(key)
          if isinstance(value,str) and re.match(exp, value):
            print("matched: ", value)
          print()
        if isinstance(value, (dict,list)):
            recursive_parser(value, fields)

recursive_parser(filtered_fhir_dict, to_include)

pattern = r'\d+'  # This pattern matches one or more digits

# Use the regular expression pattern in various operations
text = "There are 123 apples and 456 oranges."

# print(matches)  # Output: ['123', '456']

# Create an instance of ImagingStudy (replace with your actual instance)
imaging_study = ImagingStudy

# Use the dir() function to get the list of attributes and methods
methods_and_attributes = dir(imaging_study)

# Print the list
# for item in methods_and_attributes:
#   print(item)



# This code here creates a set of all the different kinds of resources in the
# bundle.
# fhir_types = set()
# for entry in bundle.entry:
#   words_to_exclude = ['Claim', 'ExplanationOfBenefit']
#   fhir_types.add(entry.resource.resource_type)
#   fhir_types = fhir_types - set(words_to_exclude)
#   for entry_key in fhir_types:
#     if entry_key == bundle.entry:
#       fhir_dict[entry_key] = str(entry.resourse)

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
