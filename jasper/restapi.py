# -*- coding: utf-8 -*-
from jasper import plugin
from flask import  Flask, jsonify, request
import json
import threading
import logging


class RestAPI(object):

    def __init__(self, profile, mic, conversation):
        self.profile = profile
        self.mic = mic
        self.conversation = conversation

        try:
            host = self.profile['restapi']['Host']
        except KeyError:
            host = '0.0.0.0'

        try:
            port = self.profile['restapi']['Port']
        except KeyError:
            port = 5000

        try:
            password = self.profile['restapi']['Password']
        except KeyError:
            password = None

        # create thread for http listener
        t = threading.Thread(target=self.startRestAPI, args=(host, port, password))
        t.daemon = True
        t.start()

    def startRestAPI(self, host, port, password):
        app = Flask(__name__)

        @app.route('/')
        def index():
            return "Jasper restAPI: running"

        @app.route('/restapi/say', methods=['POST'])
        def say_task():
            if not request.json or not 'text' in request.json:
                abort(400)
            text = request.json['text']

            self.mic.say(str(text))

            return jsonify({'text': text}), 201

        @app.route('/restapi/transcribe', methods=['GET'])
        def transcribe_task():
            transcribed = self.mic.active_listen()

            return jsonify({'transcribed':transcribed}), 201

        @app.route('/restapi/activate', methods=['GET'])
        def activate_task():
            transcribed = self.mic.active_listen()
            result = self.conversation.handleInput(transcribed)

            return jsonify({'transcribed':transcribed, 'result':result}), 201

        @app.route('/restapi/waitforkeyword', methods=['POST'])
        def waitforkeyword_task():
            if not request.json or not 'keyword' in request.json:
                abort(400)
            keyword = request.json['keyword']

            self.mic.wait_for_keyword(keyword)

            return jsonify({'keyword': keyword}), 201

        @app.route('/restapi/playfile', methods=['POST'])
        def playfile_task():
            if not request.json or not 'filename' in request.json:
                abort(400)
            filename = request.json['filename']

            self.mic.play_file(filename)

            return jsonify({'filename': filename}), 201


        # start http listener
        app.run(host='0.0.0.0', port=port, debug=False)
