# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import json
import os
import uuid
from typing import List, Union

from apps.config import API_GENERATOR
from apps.home import blueprint
from characterai import PyAsyncCAI
from flask import jsonify, render_template, request
from flask_login import current_user, login_required
from jinja2 import TemplateNotFound

chat_id = ""
token = os.environ.get("CHARACTER_AI_TOKEN")
char_id = "0O_ZRNC8cerri24KyvASHYrr9aXAzUbqRNQhq-xk1DE"
user_id = "307781294"
client = PyAsyncCAI(token)
messages: List[dict[str, Union[bool, str]]] = []


@blueprint.route("/index")
@login_required
async def index():
    messages.clear()
    global client
    client = await initialize_ai_chat()
    return render_template("home/index.html", name=current_user.username)


async def initialize_ai_chat():
    global chat_id
    chat_id = str(uuid.uuid4())
    _client = PyAsyncCAI(token)
    async with _client.connect() as chat2:
        _chat, _greeting = await chat2.new_chat(char_id, chat_id, user_id)

        print(json.dumps(_chat))
        print(json.dumps(_greeting))

        greeting = (
            _greeting["turn"]["candidates"][0]["raw_content"]
            .split("For example:")[1]
            .strip()
        )
        formatted_string = (
            "Warning: You are interacting with an AI language model. "
            "The responses do not reflect any personal opinions or "
            "views of Noah Gift. <br> <br>" + greeting
        )
        messages.append({"text": formatted_string, "incoming": True})
        return _client


@blueprint.route("/get_messages")
@login_required
def get_messages():
    return jsonify({"messages": messages})


@blueprint.route("/send_message", methods=["POST"])
@login_required
async def send_message():
    new_message = request.form.get("message")
    print(f"Received new message: {new_message}")
    messages.append({"text": new_message, "incoming": False})

    # Wait for the get_chat coroutine to complete
    # _client = PyAsyncCAI(token)
    author = {
        "author_id": user_id,
        "is_human": True,
        "name": current_user.username,
    }
    async with client.connect() as chat2:
        data = await chat2.send_message(char_id, chat_id, new_message, author)
        print(json.dumps(data))
        # name = data['src_char']['participant']['name']
        text = data["turn"]["candidates"][0]["raw_content"]
        messages.append({"text": text, "incoming": True})

    return jsonify({"success": True})


@blueprint.route("/<template>")
@login_required
def route_template(template):
    try:
        if not template.endswith(".html"):
            template += ".html"

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template(
            "home/" + template,
            segment=segment,
            API_GENERATOR=len(API_GENERATOR),
        )

    except TemplateNotFound:
        return render_template("home/page-404.html"), 404

    except:
        return render_template("home/page-500.html"), 500


# Helper - Extract current page name from request
def get_segment(request):
    try:
        segment = request.path.split("/")[-1]

        if segment == "":
            segment = "index"

        return segment

    except:
        return None
