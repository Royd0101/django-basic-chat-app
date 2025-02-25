import json
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict
from django.contrib.auth import get_user_model
from chat.models import ChatMessage
from asgiref.sync import sync_to_async

User = get_user_model()
app = FastAPI()

# Store active WebSocket connections
active_connections: Dict[int, WebSocket] = {}

async def get_user(user_id: int):
    """ Fetch user from Django ORM """
    return await sync_to_async(User.objects.get)(id=user_id)



async def save_message(sender_id: int, receiver_id: int, message: str):
    """ Save message in Django database """
    try:
        sender = await sync_to_async(User.objects.get)(id=sender_id)
        receiver = await sync_to_async(User.objects.get)(id=receiver_id)

        chat_message = await sync_to_async(ChatMessage.objects.create)(
            sender=sender, receiver=receiver, message=message
        )

        print(f"✅ Message saved: '{chat_message.message}' from {sender.username} to {receiver.username}")

        return chat_message  # Return saved message for confirmation

    except User.DoesNotExist:
        print(f"❌ ERROR: User not found (Sender: {sender_id}, Receiver: {receiver_id})")
        return None
    except Exception as e:
        print(f"❌ ERROR SAVING MESSAGE: {e}")
        return None



@app.websocket("/ws/chat/{sender_id}/{receiver_id}")
async def websocket_chat(websocket: WebSocket, sender_id: int, receiver_id: int):
    """ WebSocket connection handler for chat """

    await websocket.accept()
    active_connections[sender_id] = websocket
    active_connections[receiver_id] = websocket  # Track receiver as well

    print(f"🔵 User {sender_id} connected for chat with {receiver_id}")

    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            message_text = message_data.get("message")

            if not message_text:
                print("⚠️ Empty message received. Ignoring.")
                continue

            print(f"📩 Message received: {message_text} from {sender_id} to {receiver_id}")

            # Save message to database
            await save_message(sender_id, receiver_id, message_text)

            # Send message to receiver if online
            if receiver_id in active_connections:
                await active_connections[receiver_id].send_text(json.dumps({
                    "sender": sender_id,
                    "message": message_text
                }))
            else:
                print(f"⚠️ User {receiver_id} is offline, message stored but not delivered.")

    except WebSocketDisconnect:
        print(f"🔴 User {sender_id} disconnected")
        active_connections.pop(sender_id, None)  # Remove sender from active connections
        active_connections.pop(receiver_id, None)  # Remove receiver as well

