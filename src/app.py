from quart import Quart
import socketio
import hypercorn
import asyncio
import aiofiles
import pathlib
from langchain.schema.messages import AIMessage, HumanMessage
from fhir.resources.R4B.bundle import Bundle
from dotenv import load_dotenv
from socket_server import sio
import os
import query

# If we end up needing quart, this is how you integerate the two:
# https://python-socketio.readthedocs.io/en/latest/api.html#socketio.ASGIApp

from quart_cors import cors

app = Quart(__name__)
app = cors(app, allow_origin="*")
asgi = socketio.ASGIApp(sio, other_asgi_app=app)

def is_displayable_record(record):
  return (isinstance(record, dict) and
    'type' in record and
    record['type'] in ['condition','patient','organization'])

def record_from_dict_values(map):
  if isinstance(map, dict):
    for record in filter(is_displayable_record, map.values()):
      return record
  return None

async def send_records(records, to):
  async def send(r):
    if r['type'] == 'patient':
      r['birth_date'] = str(r['birth_date'])
    await sio.emit('records', data=r, to=to)
  # We only send the records if we know they're the right shape.
  if is_displayable_record(records):
    await send(records)
  elif (drecord := record_from_dict_values(records)):
    await send(drecord)
  elif isinstance(records, list):
    for record in records:
      if is_displayable_record(record):
        await send(record)
      elif (drecord := record_from_dict_values(record)):
        await send(drecord)

async def send_msg(msg, *, to):
  """Send the contents of a langchain message to the client to be displayed."""
  await sio.emit('server-msg', data=msg.content, to=to)

async def question_response(sid, chat_history, question):
  """Responds to a question asked by a user.

  Also responds with the underlying records."""
  try:
    records = await asyncio.create_task(query.get_records(question, chat_history))
    task = asyncio.create_task(
      send_records(records, to=sid)
    )
    response = await query.qa_with_records(records, chat_history, question)
    msg = AIMessage(content=response)
    await asyncio.gather(
      task,
      send_msg(msg, to=sid)
    )
    return msg
  except Exception:
    return AIMessage(content="Sorry, something went wrong and I couldn't understand that.")

@sio.on('connect')
async def handle_connect(sid, arg):
  print("connected {}".format(sid))
  async with sio.session(sid) as session:
    start_msg = AIMessage(content='Hello! How can I help you query records today?')
    session['chatlog'] = [start_msg]
    await send_msg(start_msg, to=sid)

@sio.on('client-msg')
async def handle_client_msg(sid, msg_text):
  msg = HumanMessage(content=msg_text)
  async with sio.session(sid) as session:
    if 'chatlog' not in session:
      raise RuntimeError("client-msg received without first receiving a start-chat")
    reply = await question_response(sid, session['chatlog'], msg_text)
    session['chatlog'].append(msg)
    session['chatlog'].append(reply)
