from dotenv import load_dotenv
from langchain.chains.llm import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.chains import GraphCypherQAChain
from langchain.graphs import Neo4jGraph
from langchain.memory import ConversationBufferWindowMemory
from langchain.schema.messages import AIMessage, HumanMessage
from langchain.memory.chat_message_histories.in_memory import ChatMessageHistory
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import asyncio
import neo4j
from socket_server import sio
from fhir.resources.R4B.bundle import Bundle
from query_prompts import CYPHER_QA_PROMPT, CYPHER_GENERATION_PROMPT
import os

if (dotenv_path := os.environ.get("ENV_FILE")):
  load_dotenv(dotenv_path)
else:
  load_dotenv()

# NOTE: could make all questions have an accompanying patient id that we're
# asking questions about? That way you can change who you're asking questions
# about without removing chat history?
# Should be really easy to do by just adding a parameter to the prompts.

# TODO: preprocessing the data
# * automate removing numbers from patient names
# * turning the full urls into IDs it understands by stripping urn:uuid

# Selecting the local graph connected
# TODO: make sure this can't mutate the graph
graph = Neo4jGraph(
  url="bolt://localhost:7687",
  username=os.environ['NEO4J_QUERY_USER'],
  password=os.environ['NEO4J_QUERY_PASSWORD']
)

# Take a look at how the DB looks
# print(graph.schema)

# Chain just for performing the queries
query_chain = GraphCypherQAChain.from_llm(
  ChatOpenAI(temperature=0), graph=graph, verbose=True, top_k=10,
  prompt = CYPHER_GENERATION_PROMPT,
  return_direct = True,
  validate_cypher=True
)

# NOTE: If we want a custom schema instead of the thing that it auto-generates
# we can just set the query_chain.graph_schema property.
# I'm not sure how much I like the default one, especially the properties part.
# It's all very JSON formatted. Maybe that's a good thing?
# print(query_chain.graph_schema)

async def get_records(question):
  """Get the json records that seem relevant to the question."""
  # The QAChain code doesn't properly implement async stuff, so we run it in
  # a different thread synchronously
  def run():
    return query_chain.run({"query":question})
  output = await asyncio.to_thread(run)
  print(output)
  return output

async def qa_with_records(records, chat_history, question):
  msg_history = ChatMessageHistory(messages=chat_history)
  qa_chain = LLMChain(
    llm=ChatOpenAI(temperature=0),
    prompt=CYPHER_QA_PROMPT,
  )
  # I want to process the records into something that's more plain text instead
  # of JSON. I don't know if that will actually help it answer better.
  res = await qa_chain.acall({"question": question, "context": records,
    "history": ConversationBufferWindowMemory(k=20,chat_memory=msg_history)})
  return res[qa_chain.output_key]

if __name__ == "__main__":
  async def main():
    chat_history = []
    while True:
      user_input = input("Enter a medical history query (or type 'exit' to quit): ")
      if user_input.lower() == 'exit':
          break
      records = await get_records(user_input)
      print(f"related records: {records}")
      res = await qa_with_records(records, chat_history, user_input)
      print(f"response: {res}")
      chat_history.append(HumanMessage(content=user_input))
      chat_history.append(AIMessage(content=res))
      print(chat_history)
  asyncio.run(main())
