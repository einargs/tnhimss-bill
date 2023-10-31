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
patient_info_dict = dict()

# Parse through dictionary to print key (resource names) and values.
def recursive_parser(data, fields, info):
    patient_string = "Patient"
    encounter_string = "Encounter"
    condition_string = "Condition"
    if isinstance(data, dict):
        for key, value in data.items():
            while key == patient_string or key == encounter_string or key == condition_string:
              for values in value:
                general = list(value)[9]
                deceasedTime = list(value)[21]
                contact = list(value)[18]
                extension = list(value)[25][:]

                info[general[0]] = general[1]
                info[deceasedTime[0]] = deceasedTime[1]
                info[contact[0]] = general[1]
                info[extension[0]] = extension[1]
                search_strings = ['age', 'birthDate', 'name', 'language', 'gender', 'appointment', 'diagnosis',
                                  'episodeOfCare', 'hospitalization', 'multipleBirthBoolean', 'location',
                                  'deceasedDateTime']
                values_list = list(values)
                if values_list[0] in search_strings:
                  info[values_list[0]] = values_list[1] 
                  # print(values)
                  if isinstance(data,list) and value in fields:
                    print()
                  if isinstance(value, (dict, list)):
                    recursive_parser(value, fields)
              break

recursive_parser(filtered_fhir_dict, to_include, patient_info_dict)

# print(patient_info_dict)


#Create variables for each field
name_fields = list(patient_info_dict['name'][0])
# extension_fields = list(patient_info_dict['contact'][0])
date_of_birth = patient_info_dict['birthDate']
patient_language = patient_info_dict['language']
patient_gender = patient_info_dict['gender']
appointment = patient_info_dict['appointment']
patient_location = patient_info_dict['location']
patient_diagnosis = patient_info_dict['diagnosis']
patient_hospitalized = patient_info_dict['hospitalization']
deceasedTime = patient_info_dict['deceasedDateTime']
patient_contact = patient_info_dict['contact']
# print(patient_contact[0])
# general_pract = patient_info_dict['generalPractioner']
# patient_hospDate = patient_info_dict['start']


# View which fields and their values are included: For testing.
# def format_patient(data):
#   print()
#   if isinstance(data, dict):
#     for key, value in data.items():
#       if isinstance(value, dict):
#          format_patient(value)
#       else:
#          print(key)
#          print(value)

# format_patient(patient_info_dict)  


# Display patient info.
def patient_info(name, birth, lang, gender, appt, loc, diag, hosp):
  profile = f'''
            The patient is named {name[9][1]} {name[4][1]} {name[6][1]}.\n
            The patient reported language is {lang}.\n
            The patient's date of birth is {birth}.\n
            The patient is a {gender}.\n
            The patient's reported appointment is {appt}.\n
            The patient's has been diagnosed with {diag}.\n
            The patient has been hospitalized for {hosp} at {loc}.
            '''
  return profile

print(patient_info(name_fields, date_of_birth, patient_language, patient_gender,
              appointment, patient_location, patient_diagnosis,
                patient_hospitalized)
)


# Examples of statements about patient
'''
The patient is named {Patient.name.prefix} {Patient.name.given} {Patient.name.family}. They is {Patient.age} years old.
The patient primarily speaks {Patient.language}.
The patient's date of birth is {Patient.birthDate}.
The patient is a {Patient.gender}.
The patient's appointment is {Encounter.appointment}.
The patient's has been diagnosed with {Encounter.diagnosis}, {Encounter.episodeOfCare}.
  If {Encounter.hospitalization} is not None:
    The patient has been hospitalized for {Encounter.hostitalization} at {Encounter.location} on {Encounter.start}.
  If {Patient.multipleBirthBoolean} is True:
    The patient was a part of multiple births.
  If {Patient.deceasedDateTime} is not None:
    The patient's date of death is {Patient.deceasedDateTime}.

'''