from flask import redirect, url_for, request
from ..app import app, db


@app.route("/select/<int:num_inventaire>")
def select(num_inventaire):
    print(request.args)
    print(request.data)
    return {"N_inventaire": num_inventaire}