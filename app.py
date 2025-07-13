from flask import Flask, render_template, request
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'

shared_state = {
    "min_val": 1,
    "max_val": 100,
    "current_number": None,
    "secret_number": None
}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "update_range" in request.form:
            try:
                shared_state["min_val"] = int(request.form.get("min", 1))
                shared_state["max_val"] = int(request.form.get("max", 100))
            except:
                pass

        if "generate" in request.form:
            # 💡 При генерации сбрасываем секрет
            shared_state["secret_number"] = None
            shared_state["current_number"] = random.randint(
                shared_state["min_val"], shared_state["max_val"]
            )

    # Что отображать
    number = shared_state["secret_number"] if shared_state["secret_number"] is not None \
             else shared_state["current_number"]

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
            message = "✔️ Секрет сохранён"
        else:
            message = "❌ Введите только цифры!"
    return render_template("secret.html", message=message)

@app.route("/clear")
def clear():
    shared_state["secret_number"] = None
    shared_state["current_number"] = None
    return render_template("index.html",
                           number=None,
                           min_val=shared_state["min_val"],
                           max_val=shared_state["max_val"])

if __name__ == "__main__":
    app.run(debug=True)
