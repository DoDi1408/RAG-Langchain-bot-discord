import logging
import logging.handlers
from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response

load_dotenv()
DISCORD_TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
print(DISCORD_TOKEN)

intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('(Message was empty because intents were not enabled probably)')
        return
    try:
        response: str = get_response(user_message)
        print("responding with " + response)
        await message.channel.send(response)
    except Exception as e:
        print("errorrrrr HELP")

@client.event
async def on_ready() -> None:
    print(str(client.user) + " is now running!")

@client.event
async def on_message(message: Message) -> None:
    print("Received a message!")
    if message.author == client.user:
        return
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)
    print("From: " + username)
    print("@ channel: " + channel)
    print("With content: " + user_message)
    await send_message(message, user_message)

def main() -> None:
    client.run(token=DISCORD_TOKEN)

if __name__ == "__main__":
    main()


"""
app = Flask(__name__)
CORS(app, support_credentials=True)

vectorstore = superIndexingFunction()
rag_chain = createRagChain(vectorstore)


@app.route('/prompt', methods=['POST'])
@cross_origin(origin='*',supports_credentials=True)
def create_prompt():
    app.print('received a /prompt')
    user_prompt = json.loads(request.data)
    app.print(user_prompt)
    if 'message' not in user_prompt:
        return jsonify({ 'error': 'missing message' }), 400

    output = ""
    for chunk in rag_chain.stream(user_prompt['message']):
        output += chunk

    return jsonify({'output': output}), 200

if __name__ == "__main__":
    from waitress import serve
    PORT = 5134
    serve(app, host="0.0.0.0", port=PORT)

"""
