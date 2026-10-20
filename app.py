from flask import Flask, request, render_template, redirect, url_for, session
from datetime import datetime
import json
import os


with open('plates.json', 'r', encoding='utf-8') as file:
    Data = json.load(file)


def save_data():
    with open('plates.json', 'w', encoding="utf-8") as f:
        json.dump(Data, f, ensure_ascii=False, indent=2)


app = Flask(__name__)
print(os.environ["SECRET_KEY"])
app.secret_key = os.environ["SECRET_KEY"]


@app.route("/")
def index():
    events = reversed(Data["events"])
    storage = []
    for i in Data["storage"]:
        storage.append(f'⌀{i} — {Data["storage"][i]} шт.')

    headers = ["Дата", "Время", "Оператор", "Событие", "⌀", "Ост."]

    username = session.get("username")
    if username:
        operator = Data["users"][username]
    else:
        operator = None

    return render_template("events.html",
                           username=operator,
                           events=events,
                           headers=headers,
                           storage=storage,
                           plates=Data["plates"],
                           rolls=Data["rolls"])


@app.route("/send", methods=["POST"])
def send():
    action = request.form["action"]
    roll = request.form["roll"]
    plate = request.form["plate"].split("№")[-1]

    if action == "Добавить":
        old_value = Data["storage"][plate]
        now_value = old_value + 10
        Data["storage"][plate] = now_value
        action = "+ 10 шт."
    else:
        old_value = Data["storage"][plate]
        now_value = old_value - 1
        Data["storage"][plate] = now_value
        action = f"({action[0]}) {roll}"

    username = session.get("username")
    if username:
        operator = Data["users"][username]
    else:
        operator = None

    # сохранение / отправка сообщения
    print(f"{action} | {roll} | {plate}")

    line = [
        str(datetime.now().strftime("%d.%m.%y")),
        str(datetime.now().strftime("%H:%M")),
        str(operator),
        str(action),
        str(plate),
        str(now_value)
    ]
    Data["events"].append(line)

    save_data()
    return redirect(url_for("index"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if Data["auth"].get(username) == password:
            session["username"] = username
            return redirect(url_for("index"))

        return render_template("login.html")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))
