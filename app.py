from flask import Flask, request, render_template_string
import openai
import os
from dotenv import load_dotenv

load_dotenv()  # Loads .env file
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<body>
<h2>Eco AI Demo</h2>

<form method="POST">
<textarea name="q" rows="4" cols="50"
placeholder="How can I reduce my carbon footprint?"></textarea><br><br>
<button type="submit">Ask AI</button>
</form>

{% if answer %}
<h3>AI Response:</h3>
<pre>{{ answer }}</pre>
{% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    answer = ""
    if request.method == "POST":
        question = request.form["q"]

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Your name is Eco AI. Your goal is to help the user decrease there carbon footprint. Introduce yourself in your response to the next prompt before answering it."},
                {"role": "user", "content": question}
            ]
        )

        answer = response.choices[0].message.content

    return render_template_string(HTML, answer=answer)

app.run()
