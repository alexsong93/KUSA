from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response
import json
import os
from postmark import PMMail
from django.core.urlresolvers import reverse

# Create your views here.

def homepage(request):
    with open("templates/exec.json") as json_file:
        execs = json.load(json_file)
        return render(request, 'english.html', {"execs":execs})

def contact(request):
    errors = []
    if request.method == 'POST':
        if not request.POST.get('subject', ''):
            errors.append('Enter a subject.')
        if not request.POST.get('message', ''):
            errors.append('Enter a message.')
        if request.POST.get('email') and '@' not in request.POST['email']:
            errors.append('Enter a valid e-mail address.')
        if not errors:
            message = PMMail(api_key = os.environ.get('POSTMARK_API_KEY'),
                 subject = request.POST['subject'],
                 sender = request.POST['email'],
                 to = 'alexsong93@gmail.com',
                 text_body = request.POST['message'])
            message.send()
            # send_mail(
            #     request.POST['subject'],
            #     request.POST['message'],
            #     request.POST.get('email', 'noreply@simplesite.com'),
            #     ['alexsong93@gmail.com'], #email address where message is sent.
            #     fail_silently=False
            # )
            # return render(request, 'english.html' {'form_success' : True})
            return HttpResponseRedirect('/')
    return render(request, 'english.html',
        {'errors': errors})

    

