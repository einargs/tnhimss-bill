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

async def send_msg(msg, *, to):
  """Send the contents of a langchain message to the client to be displayed."""
  await sio.emit('server-msg', data=msg.content, to=to)

async def question_response(sid, chat_history, question):
  """Responds to a question asked by a user.

  Also responds with the underlying records."""
  records = await asyncio.create_task(query.get_records(question))
  task = asyncio.create_task(
    sio.emit('records', data=records, to=sid)
  )
  response = await query.qa_with_records(records, chat_history, question)
  msg = AIMessage(content=response)
  await asyncio.gather(
    task,
    send_msg(msg, to=sid)
  )
  return msg

@sio.on('connect')
async def handle_connect(sid, arg):
  print("connected {}".format(sid))

@sio.on('start-chat')
async def handle_start_chat(sid, patient_id):
  print(f"starting chat {sid}")
  async with sio.session(sid) as session:
    session['patient_id'] = patient_id
    start_msg = AIMessage(content='Hello! How can I help you query records today?')
    session['chatlog'] = []
    await send_msg(start_msg, to=sid)

@sio.on('client-msg')
async def handle_client_msg(sid, msg_text):
  msg = HumanMessage(content=msg_text)
  async with sio.session(sid) as session:
    if 'patient_id' not in session:
      raise RuntimeError("client-msg received without first receiving a start-chat")
    reply = await question_response(sid, session['chatlog'], msg_text)
    session['chatlog'].append(msg)
    session['chatlog'].append(reply)
