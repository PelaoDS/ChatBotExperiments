from flask import Flask, render_template, request, jsonify
import openai
import ast
import pandas as pd

# OBS: OJO QUE completion.model_name y completion.messages[0].content están hardcodeados

app = Flask(__name__)

# Set up OpenAI API credentials
with open('key.txt', 'r') as file:
    text = file.read()
    client = openai.OpenAI(
        api_key=text
    )

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

        # Generamos Clasificador de mensaje de inventario
        with open('autos_clean.csv', 'r', encoding='utf-8') as file:
            # Lee el contenido del archivo
            content = file.read()
        clasificator_question = """Responde a la pregunta con la siguiente estructura:  [SI o NO]|[id1, id2, ...]
                                    Donde si la pregunta es de inventario respondes de la forma SI|[id1, id2, id3] ,  donde id1, id2 y id3 corresponden a id's del inventario del csv que te mostraré después. Por el otro lado, si la pregunta no es de inventario la respuesta es NO|[]
                                    csv de inventario:
                                    {}
                                    pregunta: {}
        """.format(content, message)

        # Generamos la pregunta
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": clasificator_question}
            ]
        )
        respuesta_inventario, list_autos = completion.choices[0].message.content.split('|')
        
        if respuesta_inventario == 'SI':
            texto_base = "El/los autos que buscas que tenemos en inventario es/son: "
            my_list = ast.literal_eval(list_autos)
            df = pd.read_csv('autos_clean.csv', index_col=[0])
            df_filtered = df.loc[my_list]
            texto_base = "El/los autos que buscas que tenemos en inventario es/son: "
            for row in df_filtered.values:
                row_text = "\n "
                for i,j in zip(df_filtered.columns, row):
                    row_text += "{}:{} ".format(i, j)
                texto_base += row_text
            return jsonify({'message': texto_base})

        else:
            # Send the message to OpenAI's API and receive the response
            completion = client.chat.completions.create(
                model="ft:gpt-3.5-turbo-0613:personal::8sbdrlGd",
                messages=[
                    {"role": "system", "content": "Dado el interés de un cliente en un auto usado en Chile, proporcionarás información experta, cortés y respetuosa para facilitar la venta. No usarás mas de 70 palabras por respuesta`. Feel free to re-run this cell if you want a better result.."},
                    {"role": "user", "content": message}
                ]
            )

            # Check if the response was generated successfully
            if completion.choices:
                ai_response = completion.choices[0].message.content
                return jsonify({'message': ai_response})
            else:
                return jsonify({'error': 'Failed to generate response!'})

    except Exception as e:
        # Handle errors gracefully
        print(f"Error: {str(e)}")
        return jsonify({'error': 'An error occurred'}), 500

if __name__ == '__main__':
    app.run()
