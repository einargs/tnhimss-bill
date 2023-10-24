from dotenv import load_dotenv
from langchain.chains.llm import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.chains import GraphCypherQAChain
from langchain.graphs import Neo4jGraph
from langchain.chains.graph_qa.prompts import CYPHER_QA_PROMPT
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import asyncio
import neo4j
from socket_server import sio
from fhir.resources.R4B.bundle import Bundle

load_dotenv()

# TODO: code to load in all of the different bundles into the graph.
# NOTE: could make all questions have an accompanying patient id that we're
# asking questions about? That way you can change who you're asking questions
# about without removing chat history?

# Selecting the local graph connected
graph = Neo4jGraph(
    url="bolt://localhost:7687", username="neo4j", password="pleaseletmein"
)

# Take a look at how the DB looks
# print(graph.schema)

# Chain just for performing the queries
query_chain = GraphCypherQAChain.from_llm(
    ChatOpenAI(temperature=0), graph=graph, verbose=True, top_k=10,
    return_direct = True
)
# When we add memory we'll have to track it in the session dict.
qa_chain = LLMChain(llm=ChatOpenAI(temperature=0), prompt=CYPHER_QA_PROMPT)

async def get_records(question):
  """Get the json records that seem relevant to the question."""
  output = await query_chain.acall({"query":question})
  return output['result']

async def qa_with_records(records, question):
  # I want to process the records into something that's more plain text instead
  # of JSON. I don't know if that will actually help it answer better.
  res = await qa_chain.acall({"question": question, "context": records})
  return res[qa_chain.output_key]

if __name__ == "__main__":
  asyncio.run(query_graph("RETURN {}"))
if False:
  load_dotenv()
  # Stdin user input until the user exits
  while True:
    # Natural Language Query
    user_input = input("Enter a medical history query (or type 'exit' to quit): ")

    if user_input.lower() == 'exit':
        break  # Exit the loop if the user types 'exit'

    # Run the chain with the natural language query
    response = chain.run(user_input)

    print(response)

