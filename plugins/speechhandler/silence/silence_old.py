# -*- coding: utf-8-*-
import re

WORDS = ['QUIET', 'SILENCE']


def handle(text, mic, profile):
    """
        Reports that the user has unclear or unusable input.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """
    
    mic.say('Silence Mode')
    
    mic.wait_for_keyword(self._keyword + ' ON')
    #threshold, transcribed = mic.passiveListen(PERSONA = 'JARVIS ON')
    #    
    #if threshold:
    #    mic.say('true')
    #
    #while not threshold :
    #    threshold, transcribed = mic.passiveListen('JARVIS ON')

    mic.say(self._keyword + ' back online')


def isValid(text):
    isValid = False

    for w in WORDS:
       if re.search(r'\b%s\b' % w, text, re.IGNORECASE):
          return True
