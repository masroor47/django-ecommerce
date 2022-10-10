# from base64 import urlsafe_b64decode, urlsafe_b64encode
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.utils.encoding import force_bytes, force_str
from .forms import RegistrationForm
from .token import account_activation_token
from .models import UserBase

# Create your views here.

@login_required
def dashboard(request):
    return render(request, 'account/user/dashboard.html')

def account_register(request):

    if request.method == 'POST':
        print("form submitted")
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            print("form valid")
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = "Activate your Account"
            email_context = {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            }
            message = render_to_string('account/registration/account_activation_email.html', email_context)
            print("email about to be sent")
            user.email_user(subject=subject, message=message)

            return render(request, 'account/registration/register_email_confirm.html')
        else:
            print("form is not valid")

    
    else:
        print("In The Elseeee")
        registerForm = RegistrationForm()
        context = {
            'form': registerForm,
        }
        return render(request, 'account/registration/register.html', context)



def account_activate(request, uidb64, token):
    print("this function triggered")
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
    except:
        pass
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:dashboard')
    else:
        return render(request, 'account/registration/activation_invalid.html')
