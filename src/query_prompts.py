from langchain.prompts.prompt import PromptTemplate

CYPHER_QA_TEMPLATE = """You are an assistant that helps to form nice and human understandable answers.
The information part contains the provided information that you must use to construct an answer.
The provided information is authoritative, you must never doubt it or try to use your internal knowledge to correct it.
Make the answer sound as a response to the question. Do not mention that you based the result on the given information.
If the provided information is empty, say that you don't know the answer.

Past conversation with the user:
{history}

The question asked: {question}

JSON information answering the question: {context}

Helpful Answer:"""
CYPHER_QA_PROMPT = PromptTemplate(
  input_variables=["context", "question", "history"], template=CYPHER_QA_TEMPLATE
)

CYPHER_GENERATION_TEMPLATE = """
Task: Generate Cypher statement to query a Neo4j graph database based on the FHIR schema.
Instructions:
1. Use only the provided relationship types and properties in the schema.
2. Do not use any other relationship types or properties that are not provided.
3. Differentiate between 'Patient ID' and 'Patient name'. 'Patient ID' is a unique identifier for the patient, whereas 'Patient name' might refer to the actual name of the patient. They are not interchangeable.
4. If the question mentions a name, treat it as a 'Patient name', not an ID.
5. If the question specifies an ID, treat it strictly as 'Patient ID' and not a name.

Schema:
{schema}
Nodes:
- Practitioner (Constraints: id [UNIQUENESS])
- Condition (Constraints: id [UNIQUENESS])
- MedicationRequest (Constraints: id [UNIQUENESS])
- Organization (Constraints: id [UNIQUENESS])
- Observation (Constraints: id [UNIQUENESS])
- Patient (Constraints: id [UNIQUENESS])
- Encounter (Constraints: id_name [UNIQUENESS])
- Procedure (Constraints: id [UNIQUENESS])

Relationships:
- LATESTCONDITION
- HASENCOUNTER
- FIRSTCONDITION
- PROCEDUREFORTREATMENT
- CONDITION
- NEXTCONDITION
- HASOBSERVATION
- REVEALEDCONDITION
- TREATMENTFOR
- HAPPENEDAT

Cypher examples:
# Example giving information about how many procedures the patient has had.
Question: How many procedures has Clara Carbajal undergone?
Cypher: MATCH (p:Patient {{ fname:"Clara", lname:"Carbajal" }})-[:PROCEDUREFORTREATMENT]->(procedure)
RETURN count(procedure) AS procedureCount

# Example using a patient ID.
Question: How many procedures has a patient with a given ID undergone?
Cypher: MATCH (p:Patient {{id:"P12345"}})-[:PROCEDUREFORTREATMENT]->(procedure)
RETURN count(procedure) AS procedureCount

# Example returning information about a patient
Question: Summarize information about Clara.
Cypher: MATCH (p:Patient {{fname:"Clara"}})
RETURN p

# Example giving information about their last doctor visit.
Question: When did Aaron last see a doctor?
Cypher: MATCH (p:Patient {{fname: 'Aaron'}})-[:HASENCOUNTER]->(e:Encounter)
RETURN e.encounter_end_date
ORDER BY e.encounter_end_date DESC
LIMIT 1

Note:
- Do not include any explanations or apologies in your responses.
- Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
- Do not include any text except the generated Cypher statement.

question: {question}
Cypher:
"""

extra_examples = """
# Example giving information the location of their last medical encounter.
Question: Where did Clara last see a doctor?
Cypher: MATCH (p:Patient {{fname: 'Clara'}})-[:HASENCOUNTER]->(e:Encounter {{status: 'finished'}})-[:HAPPENEDAT]->(o:Organization)
RETURN o.name
ORDER BY e.encounter_end_date
LIMIT 1
"""

CYPHER_GENERATION_PROMPT = PromptTemplate(
    input_variables=["schema", "question"], template=CYPHER_GENERATION_TEMPLATE
)
