# -*- coding: utf-8 -*-
from client import plugin
from requests import post
import re
import json


class HomeAssistantPlugin(plugin.SpeechHandlerPlugin):
    def get_phrases(self):
         return [
            self.gettext("TURN"),
            self.gettext("SWITCH"),
            self.gettext("TOGGLE"),
            self.gettext("INCREASE"),
            self.gettext("DECREASE"),
            self.gettext("RAISE"),
            self.gettext("LOWER"),
            self.gettext("DIM"),
            self.gettext("BRIGHTEN"),
            self.gettext("OPEN"),
            self.gettext("CLOSE")]

    def handle(self, text, mic):
        """
        Home Assistant conversation integration

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        """
        
        host = self.profile['HomeAssistant']['Host']
        port = self.profile['HomeAssistant']['Port'] if 'Port' in self.profile['HomeAssistant'] else 8123
        password = self.profile['HomeAssistant']['Password']

        url = 'http://' + host + ':' + str(port) + '/api/services/conversation/process'
        headers = {'x-ha-access': password, 'content-type': 'application/json'}
        
        reResult = re.search(r'(' + '|'.join(self.get_phrases()) + ')(?: the )?(.*)', text, re.IGNORECASE)
        text = reResult.group(0)
        data = json.dumps({'text':text})
        
        response = post(url, data, headers=headers)
        #print(response.text)

        mic.say(reResult.group(2))

    def is_valid(self, text):
        """
        Returns True if input is related phrases.

        Arguments:
        text -- user-input, typically transcribed speech
        """
        return any(p.lower() in text.lower() for p in self.get_phrases())
