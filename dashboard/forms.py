from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from accounts.models import Team


# kullanıcı kayıt formu
class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(label="Ad")
    last_name = forms.CharField(label="Soyad")
    email = forms.EmailField(label="E-posta")
    team = forms.CharField(label="Takım")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2', 'team']

    def clean_team(self):
        team_id = self.cleaned_data.get('team')

        # Takım adının veritabanında mevcut olup olmadığını kontrol et
        if not Team.objects.filter(id=int(team_id)).exists():
            raise forms.ValidationError(f"Hatalı takım.")

        return team_id