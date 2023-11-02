from fhir.resources.R4B.bundle import Bundle
from fhir.resources.R4B.patient import Patient
from fhir.resources.R4B.practitioner import Practitioner
from fhir.resources.R4B.condition import Condition
from fhir.resources.R4B.encounter import Encounter
from fhir.resources.R4B.organization import Organization
from fhir.resources.R4B.observation import Observation
from fhir.resources.R4B.medicationrequest import MedicationRequest
from fhir.resources.R4B.procedure import Procedure
from neo4j import AsyncGraphDatabase
from functools import partial
import asyncio
import pathlib
import re
import os
import aiofiles
from dotenv import load_dotenv

# Relationships to add:

def entries(cls, bundle):
  return (entry.resource for entry in bundle.entry \
          if isinstance(entry.resource, cls))

async def load_for(bundle, tx, cls, mk_args):
  f = lambda e: {
    "type":cls.__name__.lower(),
    "id":e.id,
    **mk_args(e)
  }
  # print(list(map(f, entries(cls, bundle))))
  template = """
    UNWIND $props AS map
    CREATE (e)
    SET e = map
    WITH e
    CALL apoc.create.addLabels(e, [$type]) YIELD node
    RETURN node;
  """

  await tx.run(template, {
    'type': cls.__name__,
    'props': list(map(f, entries(cls, bundle)))
  })

def strip_numbers(name):
  return re.sub("\d","", name)

def clean_ref(ref):
  return ref.removeprefix("urn:uuid:")

def gen_human(e):
  return {
    "fname": strip_numbers(e.name[0].given[0]),
    "lname": strip_numbers(e.name[0].family),
    'gender': e.gender,
  }

def gen_address(e):
  a = e.address[0]
  return {
    'state': a.state,
    'city': a.city,
    'zip_code': a.postalCode,
    'address_line': e.address[0].line[0]
  }

def gen_period(prefix, period):
  # Kiriti: do these need to be prefixed? In encounter they're encstart and
  # encend
  sv = prefix + '_start_date'
  se = prefix + '_end_date'
  return {
    sv: period.start,
    se: period.end
  }

def reason_code(e):
  if e.reasonCode is not None and len(e.reasonCode) > 0:
    return {'reason': e.reasonCode[0].coding[0].display}
  else:
    return {}

def reason_id(e):
  return ({'reason_id': clean_ref(e.reasonReference[0].reference)}
      if e.reasonReference is not None else {})

async def load_from_bundle(session, bundle):
  async with await session.begin_transaction() as tx:
    load = partial(load_for, bundle, tx)
    await load(Patient, lambda e: {
      **gen_human(e),
      **gen_address(e),
      'birth_date': e.birthDate,
    })
    await load(Practitioner, lambda e: {
      **gen_human(e),
    })
    await load(Organization, lambda e: {
      **gen_address(e),
      'name': e.name,
      # Kiriti: this was orgtype. Should it be shortened?
      'organization_type': e.type[0].text,
    })
    await load(Encounter, lambda e: {
      **gen_period('encounter', e.period),
      'class': e.class_fhir.code,
      'patient_name': strip_numbers(e.subject.display),
      'patient_id': clean_ref(e.subject.reference),
      'provider_name': strip_numbers(e.participant[0].individual.display),
      'provider_id': clean_ref(e.participant[0].individual.reference),
      'organization_name': e.serviceProvider.display,
      'organization_id': clean_ref(e.serviceProvider.reference),
      #**reason_code(e),
      # 'reason': e.reasonCode?[0].coding[0].display,
      'status': e.status,
    })
    await load(Condition, lambda e: {
      'clinical_status': e.clinicalStatus.coding[0].code,
      'clinical_status': e.verificationStatus.coding[0].code,
      'description': e.code.text,
      'patient_id': clean_ref(e.subject.reference),
      'encounter_id': clean_ref(e.encounter.reference),
      'onset_date': e.onsetDateTime,
      'recorded_date': e.recordedDate,
    })
    await load(Observation, lambda e: {
      'category': e.category[0].coding[0].display,
      'kind': e.code.text,
      'encounter_id': clean_ref(e.encounter.reference),
      'date_time': e.effectiveDateTime,
      **({
      'value': float(e.valueQuantity.value),
      'unit': e.valueQuantity.unit,
      } if e.valueQuantity is not None else {}),
      'patient_id': clean_ref(e.subject.reference),
    })
    await load(MedicationRequest, lambda e: {
      'status': e.status,
      'intent': e.intent,
      'description': e.medicationCodeableConcept.text,
      'patient_id': clean_ref(e.subject.reference),
      'encounter_id': clean_ref(e.encounter.reference),
      **reason_id(e),
      'requester_name': strip_numbers(e.requester.display),
      'requester_id': clean_ref(e.requester.reference),
      'authored_on': e.authoredOn,
    })
    await load(Procedure, lambda e: {
      **gen_period('procedure', e.performedPeriod),
      'status': e.status,
      'description': e.code.text,
      'patient_id': clean_ref(e.subject.reference),
      'encounter_id': clean_ref(e.subject.reference),
      **reason_id(e),
    })
async def delete_all(session):
  await session.run("MATCH (n) DETACH DELETE n")

async def setup_relations(session):
  async with aiofiles.open('./db/setup_relations.txt', 'r') as f:
    code = await f.read()
    await session.run("CALL apoc.cypher.runMany($code, {})", code=code)

# Here we specify the file we want to load.
async def main():
  load_dotenv()
  aaron = pathlib.Path("./data/fhir/Aaron697_Brekke496_2fa15bc7-8866-461a-9000-f739e425860a.json")
  clara = pathlib.Path("./data/fhir/Clara183_Carbajal274_FHIR.json")
  aaron_bundle = Bundle.parse_file(aaron)
  clara_bundle = Bundle.parse_file(clara)
  auth = (os.environ['NEO4J_ADMIN_USER'], os.environ['NEO4J_ADMIN_PASSWORD'])

  async with AsyncGraphDatabase.driver("bolt://localhost:7687", auth=auth) as driver:
    async with driver.session() as session:
      await delete_all(session)
      await load_from_bundle(session, clara_bundle)
      await load_from_bundle(session, aaron_bundle)
      await setup_relations(session)

if __name__ == "__main__":
  asyncio.run(main())
