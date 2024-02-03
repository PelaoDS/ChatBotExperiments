from flask import Flask, render_template, request, jsonify
import openai

# OBS: OJO QUE completion.model_name y completion.messages[0].content están hardcodeados

app = Flask(__name__)

# Set up OpenAI API credentials
with open('key.txt', 'r') as file:
    text = file.read()
    openai.api_key = text

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

        # Send the message to OpenAI's API and receive the response
        completion = openai.ChatCompletion.create(
            model="ft:gpt-3.5-turbo-0613:personal::8oDxipKY",
            messages=[
                {"role": "system", "content": "Dado el interés de un cliente en un auto usado en Chile, proporcionarás información experta, cortés y respetuosa para facilitar la venta.`. Feel free to re-run this cell if you want a better result.."},
                {"role": "user", "content": message}
            ]
        )

        # Check if the response was generated successfully
        if completion['choices'] and completion['choices'][0]['message']['content']:
            ai_response = completion['choices'][0]['message']['content']
            return jsonify({'message': ai_response})
        else:
            return jsonify({'error': 'Failed to generate response!'})

    except Exception as e:
        # Handle errors gracefully
        print(f"Error: {str(e)}")
        return jsonify({'error': 'An error occurred'}), 500

if __name__ == '__main__':
    app.run()
