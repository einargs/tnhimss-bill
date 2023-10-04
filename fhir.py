from fhir.resources.R4B.bundle import Bundle
from fhir.resources.R4B.explanationofbenefit import ExplanationOfBenefit
import pathlib

filename = pathlib.Path("./data/fhir/Aaron697_Brekke496_2fa15bc7-8866-461a-9000-f739e425860a.json")
bundle = Bundle.parse_file(filename)
eobs = [entry.resource for entry in bundle.entry \
    if isinstance(entry.resource, ExplanationOfBenefit)]
print(eobs[0].billablePeriod.start)
