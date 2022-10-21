from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import Group
from django import forms
from doctors.models import User
from handonvitals.settings import ALLOWED_USER_EMAIL_DOMAINS
from django.core.mail import send_mail
from django.contrib import messages

admin.site.unregister(Group)

# TODO: handle exception!
def send_password_via_email(user, password):
    subject_template = "A sua conta em HandOnVitals"
    body_template = "{title} {first_name} {last_name}, foi criada uma conta em HandOnVitals para si.\nAs suas credenciais são:\nEmail: {email}\nPassword: {password}\n\nAltere a sua password assim que puder."

    send_mail(
    subject=subject_template,
    message=body_template.format(title=user.title, first_name=user.first_name, last_name=user.last_name, email=user.email, password=password),
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=[user.email])


class UserForm(forms.ModelForm):
    # Make them required
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)

    def clean_email(self):
        data = self.cleaned_data['email']
        domain = data.split('@')[1]
        allowed_domains = ALLOWED_USER_EMAIL_DOMAINS
        if domain not in allowed_domains:
            raise forms.ValidationError(f'Only the following email domains are allowed: {", ".join(allowed_domains)}')

        return data

    class Meta:
        model = User
        fields = ['email', 'title', 'first_name', 'last_name', 'ballot']


class UserAdmin(admin.ModelAdmin):
    exclude = ['last_login', 'groups', 'user_permissions', 'is_superuser', 'is_staff', 'is_active', 'date_joined']
    form = UserForm

    def save_model(self, request, obj, form, change):
        password = User.objects.make_random_password()
        try:
            send_password_via_email(obj, password)
        except:
            messages.set_level(request, messages.ERROR)
            messages.error(request, 'Failed sending email to doctor')
        
        obj.set_password(password)
        obj.save()

admin.site.register(User, UserAdmin)
