from flask import Flask, render_template, request
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'

# Глобальное состояние
shared_state = {
    "min_val": 1,
    "max_val": 100,
    "secret_number": None
}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        shared_state["min_val"] = int(request.form.get("min", 1))
        shared_state["max_val"] = int(request.form.get("max", 100))

    number = shared_state["secret_number"] if shared_state["secret_number"] is not None \
             else random.randint(shared_state["min_val"], shared_state["max_val"])

    return render_template("index.html",
                           number=number,
                           min_val=shared_state["min_val"],
                           max_val=shared_state["max_val"])

@app.route("/secret", methods=["GET", "POST"])
def secret():
    message = ""
    if request.method == "POST":
        code = request.form.get("code", "")
        if code.isdigit():
            shared_state["secret_number"] = int(code)
            message = "✔️ Принято"
        else:
            message = "❌ Введите только цифры!"

    return render_template("secret.html", message=message)

@app.route("/clear")
def clear():
    shared_state["secret_number"] = None
    return render_template("index.html",
                           number=random.randint(shared_state["min_val"], shared_state["max_val"]),
                           min_val=shared_state["min_val"],
                           max_val=shared_state["max_val"])
