# -*- coding: utf-8 -*-
from jasper import plugin
import re


class SilencePlugin(plugin.SpeechHandlerPlugin):
    def get_phrases(self):
         return [
            self.gettext("QUIET"),
            self.gettext("SILENCE")]

    def handle(self, text, mic):
        """
        Home Assistant conversation integration

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        """

        mic.say('Silence Mode')
        
        mic.wait_for_keyword(mic._keyword + ' COME BACK')

        mic.say(mic._keyword + ' back online')
        

    def is_valid(self, text):
        """
        Returns True if input is related phrases.

        Arguments:
        text -- user-input, typically transcribed speech
        """
        return any(p.lower() in text.lower() for p in self.get_phrases())
