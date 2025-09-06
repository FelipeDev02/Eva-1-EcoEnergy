from django import forms
from django.contrib.auth.models import User
from dispositivos.models import Organization

class OrganizationRegisterForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            Organization.objects.create(
                user=user,
                name=self.cleaned_data['name'],
                email=self.cleaned_data['email']
            )
        return user