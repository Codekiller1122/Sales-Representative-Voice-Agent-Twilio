from django.conf import settings
from django.http import JsonResponse, HttpResponse
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VoiceGrant
from twilio.twiml.voice_response import VoiceResponse

def generate_token(request):
    identity = request.GET.get('identity', 'sales_agent')
    token = AccessToken(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_API_KEY_SID, settings.TWILIO_API_KEY_SECRET, identity=identity)
    voice_grant = VoiceGrant(outgoing_application_sid=settings.TWIML_APP_SID, incoming_allow=True)
    token.add_grant(voice_grant)
    jwt = token.to_jwt()
    if isinstance(jwt, bytes):
        jwt = jwt.decode('utf-8')
    return JsonResponse({'token': jwt, 'identity': identity})

def voice_response(request):
    response = VoiceResponse()
    to = request.GET.get('to') or request.POST.get('to')
    if to:
        dial = response.dial(callerId=settings.TWILIO_PHONE_NUMBER)
        if to.startswith('+'):
            dial.number(to)
        else:
            dial.client(to)
    else:
        response.say('Incoming call. Connecting to sales agent.')
        response.dial().client('sales_agent')
    return HttpResponse(str(response), content_type='text/xml')
