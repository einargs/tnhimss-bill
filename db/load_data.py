from fhir.resources.R4B.bundle import Bundle
from fhir.resources.R4B.patient import Patient
from fhir.resources.R4B.practitioner import Practitioner
from fhir.resources.R4B.condition import Condition
from fhir.resources.R4B.encounter import Encounter
from fhir.resources.R4B.medicationrequest import MedicationRequest
from neo4j import AsyncGraphDatabase
import asyncio
import pathlib
import re
import os
from dotenv import load_dotenv

# Relationships to add:

def entries(cls, bundle):
  return (entry.resource for entry in bundle.entry \
          if isinstance(entry.resource, cls))

async def load_for(cls, bundle, tx, mk_args, template):
  await tx.run(template, {
    'props': list(map(mk_args, entries(cls, bundle)))
  })

def strip_numbers(name):
  return re.sub("\d","", name)

async def load_from_bundle(session, bundle):
  async with await session.begin_transaction() as tx:
    load_for(Practitioner, bundle, tx, lambda prac: {
      "fname": strip_numbers(prac.name[0].given[0]),
      "lname": strip_numbers(prac.name[0].family),
      "gender": prac.gender,
      "id": prac.id
    }, """
UNWIND props AS map
CREATE (prov: Practitioner map);
""")

# Here we specify the file we want to load.
async def main():
  load_dotenv()
  filename = pathlib.Path("./data/fhir/Aaron697_Brekke496_2fa15bc7-8866-461a-9000-f739e425860a.json")
  bundle = Bundle.parse_file(filename)
  auth = (os.environ['NEO4J_ADMIN_USER'], os.environ['NEO4J_ADMIN_PASSWORD'])

  async with AsyncGraphDatabase("bolt://localhost:7687", auth) as driver:
    async with driver.session() as session:
      load_from_bundle(session, bundle)

if __name__ == "__main__":
  asyncio.run(main())
