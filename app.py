from quart import Quart
import socketio
import hypercorn
import asyncio
import aiofiles
import pathlib
from fhir.resources.R4B.bundle import Bundle

# If we end up needing quart, this is how you integerate the two:
# https://python-socketio.readthedocs.io/en/latest/api.html#socketio.ASGIApp

from quart_cors import cors

app = Quart(__name__)
app = cors(app, allow_origin="*")
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
asgi = socketio.ASGIApp(sio, other_asgi_app=app)

def patient_json_path(patient_id):
  """
  Converts a patient ID into the correct path to their json file.
  """
  match patient_id:
    case "aaron-brekke":
      return pathlib.Path("./data/fhir/Aaron697_Brekke496_2fa15bc7-8866-461a-9000-f739e425860a.json")
    case _:
      raise "Unknown patient id"

async def load_fhir_bundle(patient_id):
  """
  Load and parse the appropriate FHIR json file for a patient id.
  """
  file_path = patient_json_path(patient_id)
  async with aiofiles.open(file_path) as file:
    raw_json = await file.read()
    return Bundle.parse_raw(raw_json)

def format_records(bundle):
  """
  Format the bundle of healthcare records so the chatbot can understand it.
  """
  return "SOME PLACEHOLDER TEXT"

def create_summary_prompt(formatted_records):
  """
  Use the formatted records string to prompt the chatbot to
  summarize the health records.
  """
  return "PLACEHOLDER RECORD SUMMARY"

def format_transcript(formatted_records, transcript):
  """
  Format the chat between the chatbot and user so far into something the
  chatbot can reply to. Also include information from the formatted
  healthcare records. Prompt the chatbot to respond.
  """
  print(transcript)
  return "PLACEHOLDER TRANSCRIPT"

async def send_to_chatbot(msg):
  """
  Send a string to the chatbot and get back its response.
  """
  return f'PLACEHOLDER RESPONSE TO {msg}'
@sio.on('connect')
async def handle_connect(sid, arg):
  print("connected {}".format(sid))

@sio.on('start-chat')
async def handle_start_chat(sid, patient_id):
  print(f"starting chat {sid}")
  bundle = await load_fhir_bundle(patient_id)
  formatted_records = format_records(bundle)
  summary_prompt = create_summary_prompt(bundle)
  summary = await send_to_chatbot(summary_prompt)
  async with sio.session(sid) as session:
    session['patient_id'] = patient_id
    session['formatted_records'] = formatted_records
    session['chatlog'] = [summary]
    await sio.emit('server-msg', data=summary, to=sid)

@sio.on('client-msg')
async def handle_client_msg(sid, msg):
  async with sio.session(sid) as session:
    if 'patient_id' not in session:
      raise RuntimeError("client-msg received without first receiving a start-chat")
    session['chatlog'].append(msg)
    transcript_prompt = format_transcript(
        session['formatted_records'], session['chatlog'])
    reply = await send_to_chatbot(transcript_prompt)
    session['chatlog'].append(reply)
    await sio.emit('server-msg', data=reply, to=sid)