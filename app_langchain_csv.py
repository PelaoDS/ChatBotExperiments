from flask import Flask, render_template, request, jsonify

from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_openai import ChatOpenAI #, OpenAI

# Get Secrets
with open('key.txt', 'r') as file:
    text = file.read()

# Create Agent
agent = create_csv_agent(
    ChatOpenAI(temperature=0, model="ft:gpt-3.5-turbo-0613:personal::8sbdrlGd", api_key=text),
    "autos_clean.csv",
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS,
)

app = Flask(__name__)

# Define the default route to return the index.html file
@app.route("/")
def index():
    return render_template("index.html")

# Define the /api route to handle POST requests
@app.route("/api", methods=["POST"])
def api():
    try:
        # Get the message from the POST request
        message = request.json.get("message")

        # # Send the message to OpenAI's API and receive the response
        # completion = client.chat.completions.create(
        #     model="ft:gpt-3.5-turbo-0613:personal::8sbdrlGd",
        #     messages=[
        #         {"role": "system", "content": "Dado el interés de un cliente en un auto usado en Chile, proporcionarás información experta, cortés y respetuosa para facilitar la venta. No usarás mas de 70 palabras por respuesta`. Feel free to re-run this cell if you want a better result.."},
        #         {"role": "user", "content": message}
        #     ]
        #)

        # # Check if the response was generated successfully
        # if completion.choices:
        #     ai_response = completion.choices[0].message.content
        #     return jsonify({'message': ai_response})
        # else:
        #     return jsonify({'error': 'Failed to generate response!'})

        response = agent.run(message)
        print(response)
        return jsonify({'message': response})

    except Exception as e:
        # Handle errors gracefully
        print(f"Error: {str(e)}")
        return jsonify({'error': 'An error occurred'}), 500

if __name__ == '__main__':
    app.run()

