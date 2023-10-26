from resource_import import *
import datetime

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

# Filtered fhir_dict to exclude rsources with 'None' values
filtered_fhir_dict = {key: value for key, value in fhir_dict.items() if fhir_dict.items() is not None}

# Open and read the file
with open("dictFile.txt", "r") as file:
    for line in file:
        # Split each line by the '=' character
        parts = line.strip().split(",")
        
        # Check if the line has a valid key-value pair
        if len(parts) < 1:
            key, value = parts
            filtered_fhir_dict[key] = value

# List of values from dictionary keys we want to use.
to_include = [
    'language', 'modifierExtension', 'active', 'birthDate', 'contact', 'deceasedBoolean', 'deceasedDateTime', 'gender',
    'generalPractitioner', 'managingOrganization', 'multipleBirthBoolean', 'multipleBirthInteger', 'appointment', 'diagnosis',
    'episodeOfCare', 'hospitalization', 'identifier', 'length', 'location', 'partOf', 'priority', 'reasonReference', 'serviceType',
    'status', 'statusHistory', 'abatementAge', 'asserter', 'bodySite', 'category', 'evidence', 'identifier', 'note', 'onsetAge',
    'recorder', 'severity', 'stage', 'reasonReference', 'status', 'telecom', 'author', 'contributor', 'created', 'description',
    'goal', 'identifier', 'intent', 'replaces', 'status', 'supportingInfo', 'title', 'doseQuantity', 'education', 'expirationDate',
    'fundingSource', 'identifier', 'isSubpotent', 'location', 'lotNumber', 'manufacturer', 'note', 'performer',
    'programEligibility', 'protocolApplied', 'reaction', 'reasonCode', 'reasonReference', 'recorded', 'status', 'statusReason',
    'subpotentReason', 'complication', 'complicationDetail', 'focalDevice', 'followUp', 'identifier', 'location', 'note',
    'outcome', 'partOf', 'performedAge', 'performedDateTime', 'category', 'courseOfTherapyType', 'detectedIssue',
    'dispenseRequest', 'doNotPerform', 'eventHistory', 'groupIdentifier', 'substitution', 'supportingInformation'
]

# Parse through dictionary to print key (resource names) and values.
def recursive_parser(data, fields):
    if isinstance(data, dict):
        for key, value in data.items():
          print(key)
          for values in value:
            print(values)
            if isinstance(data,list) and value in fields:
              print(values)
            if isinstance(value, (dict, list)):
              recursive_parser(value, fields)

recursive_parser(filtered_fhir_dict, to_include)