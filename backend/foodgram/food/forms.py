from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Recipe


class AddRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = 'Категория не выбрана'

    class Meta:
        model = Recipe
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise forms.ValidationError('Длина превышает 200 символов')

        return title


"""class AddPostForm(forms.ModelForm):
    title = forms.CharField(max_length=250, label='Название')
    slug = forms.SlugField(max_length=150)
    content = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 60, 'rows': 10})
        )
    is_published = forms.BooleanField(required=False, initial=True)
    cat = forms.ModelChoiceField(queryset=Category.objects.all())"""


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(
        label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'})
        )
    email = forms.EmailField(
        label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'})
        )
    password1 = forms.CharField(
        label='Пароль', widget=forms.PasswordInput(
            attrs={'class': 'form-input'}
            )
        )
    password2 = forms.CharField(
        label='Повтор пароля', widget=forms.PasswordInput(
            attrs={'class': 'form-input'}
            )
        )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'})
        )
    password = forms.CharField(
        label='Пароль', widget=forms.PasswordInput(
            attrs={'class': 'form-input'}
            )
        )
