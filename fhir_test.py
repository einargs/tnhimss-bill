from fhir.resources.R4B.bundle import Bundle
from fhir.resources.R4B.patient import Patient
from fhir.resources.R4B.explanationofbenefit import ExplanationOfBenefit
import pathlib

# Here we specify the file we want to load.
filename = pathlib.Path("./data/fhir/Aaron697_Brekke496_2fa15bc7-8866-461a-9000-f739e425860a.json")
bundle = Bundle.parse_file(filename)
eobs = [entry.resource for entry in bundle.entry \
    if isinstance(entry.resource, ExplanationOfBenefit)]
for entry in bundle.entry:
  if isinstance(entry.resource, Patient):
    print(entry.json())
    break

# This code here creates a set of all the different kinds of resources in the
# bundle.
fhir_types = set()
for entry in bundle.entry:
  fhir_types.add(entry.resource.resource_type)
print(fhir_types)
