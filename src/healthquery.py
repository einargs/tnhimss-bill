import os
import time
import logging
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains import GraphCypherQAChain
from langchain.graphs import Neo4jGraph
from langchain.prompts.prompt import PromptTemplate

load_dotenv()

# Just logging the setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_URL = os.getenv("DB_URL", "bolt://localhost:7687")
DB_USERNAME = os.getenv("DB_USERNAME", "neo4j")
DB_PASSWORD = os.getenv("DB_PASSWORD", "queryhealth1")
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))

# Need to play with this more
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

    Cypher examples:
    # Example using patient name
    # How many procedures has patient 'Clara183 Carbajal274' undergone?
    MATCH (p:Patient {{fname:"Clara183", lname:"Carbajal274"}})-[:PROCEDUREFORTREATMENT]->(procedure)
    RETURN count(procedure) AS procedureCount

    # Example using patient ID
    # How many procedures has a patient with a given ID undergone?
    MATCH (p:Patient {{id:"P12345"}})-[:PROCEDUREFORTREATMENT]->(procedure)
    RETURN count(procedure) AS procedureCount

    - Also, patient names in the question may not have numbers present in them, so if "Clara Carbajal" appears
      in the question, assume that it is referring to Clara183 Carbajal274. Also display answers without these
      numbers if displaying name.

    Note:
    - Do not include any explanations or apologies in your responses.
    - Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
    - Do not include any text except the generated Cypher statement.

    The question is:
    {question}
    The cypher query is:
"""

CYPHER_GENERATION_PROMPT = PromptTemplate(
    input_variables=["schema", "question"], template=CYPHER_GENERATION_TEMPLATE
)


def initialize_graph():
    try:
        graph = Neo4jGraph(
            url=DB_URL,
            username=DB_USERNAME,
            password=DB_PASSWORD
        )
        return graph
    except Exception as e:
        logger.error(f"Error initializing graph: {e}")
        return None


def initialize_chain(graph):
    try:
        chain = GraphCypherQAChain.from_llm(
            ChatOpenAI(temperature=0), graph=graph, verbose=True, top_k=10,
            cypher_prompt=CYPHER_GENERATION_PROMPT  # adding the prompt here
        )
        return chain
    except Exception as e:
        logger.error(f"Error initializing chain: {e}")
        return None


def get_response(chain, user_input, retries=MAX_RETRIES):
    for i in range(retries):
        try:
            response = chain.run(user_input)
            return response
        except Exception as e:
            logger.error(f"Error getting response: {e}")
            if i < retries - 1:
                logger.info("Retrying...")
                time.sleep(2)  # Wait for 2 seconds before retrying
            else:
                logger.error("Max retries reached.")
    return None


def main():
    graph = initialize_graph()
    if not graph:
        logger.error("Failed to initialize graph. Exiting...")
        return

    chain_language_example = initialize_chain(graph)
    if not chain_language_example:
        logger.error("Failed to initialize chain. Exiting...")
        return

    while True:
        user_input = input("Enter a medical history query (or type 'exit' to quit): ")

        if user_input.lower() == 'exit':
            break

        response = get_response(chain_language_example, user_input)
        if response:
            print(response)
        else:
            print("Failed to get a response. Please try again later.")


if __name__ == "__main__":
    main()
