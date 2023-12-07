# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request, jsonify
from flask_login import login_required
from jinja2 import TemplateNotFound

from apps.config import API_GENERATOR
from typing import Union, List
from characterai import PyAsyncCAI
import os
import asyncio
@blueprint.route('/index')
# @login_required
def index():
    return render_template('home/index.html')

messages: List[dict[str, Union[bool, str]]] = [

]


async def initialize_ai_chat():
    client = PyAsyncCAI(os.environ.get("CHARACTER_AI_TOKEN"))
    char = "0O_ZRNC8cerri24KyvASHYrr9aXAzUbqRNQhq-xk1DE"
    chat = await client.chat2.get_chat(char)
    author = {'author_id': chat['chats'][0]['creator_id']}

    async def get_chat():
        return await client.chat2.get_chat(char)

    # Run the get_chat coroutine in the background
    chat_task = asyncio.create_task(get_chat())

    return client, char, chat_task, author

@blueprint.route('/get_messages')
# @login_required
def get_messages():
    return jsonify({'messages': messages})


@blueprint.route('/send_message', methods=['POST'])
# @login_required
async def send_message():
    new_message = request.form.get('message')
    print(f'Received new message: {new_message}')
    messages.append({'text': new_message, 'incoming': False})

    client, char, chat_task, author = await initialize_ai_chat()

    # Wait for the get_chat coroutine to complete
    chat = await chat_task
    async with client.connect() as chat2:
        data = await chat2.send_message(
            char, chat['chats'][0]['chat_id'],
            new_message, author
        )
        # name = data['src_char']['participant']['name']
        text = data['turn']['candidates'][0]['raw_content']
        messages.append({'text': text, 'incoming': True})

    return jsonify({'success': True})


@blueprint.route('/<template>')
@login_required
def route_template(template):
    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment, API_GENERATOR=len(API_GENERATOR))

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):
    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
