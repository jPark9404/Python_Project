from django.shortcuts import render

# Create your views here.
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from .models import Message
from .forms import ContactForm


def index(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            content = form.cleaned_data['content']
            phone_number = form.cleaned_data['phone_number']
            html = render_to_string('contact/contactform.html', {
                'name': name,
                'email': email,
                'phone_number': phone_number,
                'content': content,
            })

            Message.objects.create(name=name, email=email, phone_number=phone_number, content=content)

            send_mail('The contact form subject', 'This is the message', 'harmony.restaurant202@gmail.com',
                      ['harmony.restaurant202@gmail.com'], html_message=html)

            return redirect('messageSuccess')
    else:
        form = ContactForm()

    return render(request, 'contact/index.html', {
        'form': form
    })


def messageSuccess(request):
    return render(request, 'contact/messageSuccess.html'
        )
