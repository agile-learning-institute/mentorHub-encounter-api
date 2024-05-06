from flask import Flask

app = Flask(__name__)

def hello_world(**kwargs):
    if len(kwargs) < 1:
        return "Hello, World!"
    else:
        str = """"""
        for key, value in kwargs.items():
            str += f"the {key} is {value}\n"
        return str

app.add_url_rule("/api/encounters/", methods=["GET", "POST"], view_func=hello_world)
app.add_url_rule("/api/encounters/<id>/", methods=["GET", "PATCH"], view_func=hello_world)
app.add_url_rule("/api/plans/", methods=["GET", "POST"], view_func=hello_world)
app.add_url_rule("/api/plans/<id>/", methods=["GET", "PATCH"], view_func=hello_world)
