from django import forms
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            # authenticate that the user is exist
            user = authenticate(username=username, password=password)

            if not user:  # if does not give a user model object
                raise forms.ValidationError('User does not exist')

            if not user.check_password(password):
                raise forms.ValidationError('Incorrect password')

            if not user.is_active:
                raise forms.ValidationError('User is no longer active')

        return super(UserLoginForm, self).clean(*args, **kwargs)

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    # check if two passwords matched or not
    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password != password2:
            raise forms.ValidationError('Password must match!')

        return password

    # check if username already registered or not
    def clean_username(self):
        username = self.cleaned_data.get('username')
        username_qs = User.objects.filter(username=username)

        if username_qs.exists():
            raise forms.ValidationError('This username is not available!')
        else:
            return username

    # check if email already registered or not
    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_qs = User.objects.filter(email=email)

        if email_qs.exists():
            raise forms.ValidationError('This email has already been registered!')
        else:
            return email