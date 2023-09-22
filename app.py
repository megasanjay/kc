# pylint: skip-file
import os
import json
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from keycloak import KeycloakAdmin, KeycloakOpenID, KeycloakOpenIDConnection


app = Flask(__name__)

CLIENT_ID = "flaskee"
CLIENT_SECRET = "X5Gnn2yLLc4RV48Nkvm1hLm9h8NurDh1"
KEYCLOAK_URI = "http://localhost:8080/"
REALM = "master"

keycloak_openid = KeycloakOpenID(
    server_url=KEYCLOAK_URI,
    client_id=CLIENT_ID,
    realm_name=REALM,
    client_secret_key=CLIENT_SECRET,
)

keycloak_connection = KeycloakOpenIDConnection(
    server_url=KEYCLOAK_URI,
    client_id=CLIENT_ID,
    username="admin",
    password="admin",
    realm_name=REALM,
    client_secret_key=CLIENT_SECRET,
)

keycloak_admin = KeycloakAdmin(connection=keycloak_connection)


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/signup", methods=["POST"])
def signup():
    body = request.get_json()

    for field in ["username", "password"]:
        if field not in body:
            return f"Field {field} is missing!", 400

    count_users = keycloak_admin.users_count()

    print(count_users)

    print(body)

    new_user = keycloak_admin.create_user(
        {
            "username": body["username"],
            "email": body["username"] + "@gmail.com",
            "enabled": True,
            "credentials": [
                {"type": "password", "value": body["password"], "temporary": False}
            ],
        },
        exist_ok=False,
    )

    print(new_user)

    return jsonify(new_user), 200
    # return "OK", 200


@app.route("/token_login/", methods=["POST"])
def get_token():
    body = request.get_json()

    for field in ["username", "password"]:
        if field not in body:
            return f"Field {field} is missing!", 400

    token = keycloak_openid.token(username=body["username"], password=body["password"])

    return jsonify(token), 200
