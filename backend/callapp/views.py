import os
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VoiceGrant
from twilio.twiml.voice_response import VoiceResponse

def generate_token(request):
    identity = request.GET.get('identity', 'anonymous')

    token = AccessToken(
        settings.TWILIO_ACCOUNT_SID,
        settings.TWILIO_API_KEY_SID,
        settings.TWILIO_API_KEY_SECRET,
        identity=identity
    )
    voice_grant = VoiceGrant(
        outgoing_application_sid=settings.TWIML_APP_SID,
        incoming_allow=True
    )
    token.add_grant(voice_grant)
    jwt = token.to_jwt()
    # to_jwt() returns bytes in newer twilio versions, decode if needed
    if isinstance(jwt, bytes):
        jwt = jwt.decode('utf-8')
    return JsonResponse({'token': jwt, 'identity': identity})


def voice_response(request):
    # Twilio will POST or GET here to fetch TwiML instructions for a call
    response = VoiceResponse()
    to = request.GET.get('to') or request.POST.get('to')

    if to:
        # Outgoing: dial a client identity or a phone number depending on format
        dial = response.dial(callerId=settings.TWILIO_PHONE_NUMBER)
        if to.startswith('+'):
            dial.number(to)
        else:
            # treat as client identity
            dial.client(to)
    else:
        # Generic incoming behavior: connect to client named 'receiver'
        response.say('You have an incoming call. Connecting to client.')
        response.dial().client('receiver')

    return HttpResponse(str(response), content_type='text/xml')
