# -*- coding: utf-8 -*-
from client import plugin
import re
import wolframalpha


class KnowledgedPlugin(plugin.SpeechHandlerPlugin):
    def get_priority(self):
        return -10
        
    def get_phrases(self):
        return [
            self.gettext("WHO"),
            self.gettext("WHAT"),
            self.gettext("DO"),
            self.gettext("HOW"),
            self.gettext("WHEN"),
            self.gettext("CONVERT"),
            self.gettext("WHERE"),
            self.gettext("ARE"),
            self.gettext("WHICH"),
            self.gettext("CAN"),
            self.gettext("WHY"),
            self.gettext("IS"),
            self.gettext("GIVE"),
            self.gettext("DEFINE"),
            self.gettext("POD")]

    def handle(self, text, mic):
        """
        WolframAlpha

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        """
        
        app_id = self.profile['keys']['WOLFRAMALPHA']
        
        client = wolframalpha.Client(app_id)

        query = client.query(text)
        
        if len(query.pods) > 0:
            response = ""
            pod = query.pods[1]
            if pod.text:
                response = pod.text.splitlines()[0]
                response = re.match(r'([^\(]*)', pod.text, re.IGNORECASE).group(1)
            else:
                response = "I can not find anything"

            mic.say(response.replace("|",""))
        else:
            mic.say("Sorry, Could you be more specific?.")

    def is_valid(self, text):
        """
        Returns True if input is related phrases.

        Arguments:
        text -- user-input, typically transcribed speech
        """
        return any(p.lower() in text.lower() for p in self.get_phrases())
