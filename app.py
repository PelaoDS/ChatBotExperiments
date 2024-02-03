from flask import Flask, render_template, request, jsonify
import openai

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
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
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
