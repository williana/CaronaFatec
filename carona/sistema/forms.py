# coding: utf-8
from datetime import datetime

from django import forms
from django.contrib.auth.models import User
from municipios.widgets import SelectMunicipioWidget
from carona.sistema.models import Perfil, Mensagem,Ponto


class PerfilUsuarioForm(forms.ModelForm):
    nome = forms.CharField(max_length=100)
    sobrenome = forms.CharField(max_length=100)
    email = forms.EmailField()

    ponto_lat = forms.CharField(
        max_length=255, widget=forms.HiddenInput, initial="-23.179080")
    ponto_long = forms.CharField(
        max_length=255, widget=forms.HiddenInput, initial="-45.887248")

    senha = forms.CharField(max_length=100, widget=forms.PasswordInput, required=True)
    senha_conf = forms.CharField(label=u"Confirmação", max_length=100, widget=forms.PasswordInput, required=True)

    def __init__(self, *args, **kwargs):
        super(PerfilUsuarioForm, self).__init__(*args, **kwargs)
        self.fields['municipio'].label = ''
        instance = kwargs.get('instance', False)

        if instance:
            self.fields['nome'].initial = instance.user.first_name
            self.fields['sobrenome'].initial = instance.user.last_name
            self.fields['email'].initial = instance.user.email
            self.fields['senha'].required = False
            self.fields['senha_conf'].required = False

    def clean_senha_conf(self):
        if self.cleaned_data['senha'] != self.cleaned_data['senha_conf']:
            raise forms.ValidationError(u"As senhas devem ser iguais!")
        return self.cleaned_data['senha_conf']

    def clean_email(self):
        email = User.objects.filter(email=self.cleaned_data['email'])
        if email and not self.instance.pk:
            raise forms.ValidationError(u"Email já cadastrado")
        elif email and (self.instance.user.email != self.cleaned_data['email']):
            raise forms.ValidationError(u"Email já cadastrado")
        return self.cleaned_data['email']

    def save(self, *args, **kwargs):
        is_new = self.instance.pk is None
        commit = kwargs.pop('commit', True)
        if is_new:
            user = User()
            ponto = Ponto()
        else:
            ponto = self.instance.ponto
            user = self.instance.user

        user.email = user.username = self.cleaned_data['email']
        user.first_name = self.cleaned_data['nome']
        user.last_name = self.cleaned_data['sobrenome']

        ponto.x = self.cleaned_data['ponto_long']
        ponto.y = self.cleaned_data['ponto_lat']

        if self.cleaned_data['senha']:
            user.set_password(self.cleaned_data['senha'])

        if commit:
            user.save()
            ponto.save()
            try:
                self.instance.pk = user.perfil.pk
            except:
                pass

            self.instance.ponto = ponto
            self.instance.user = user

        return super(PerfilUsuarioForm, self).save(*args, **kwargs)

    class Meta:
        model = Perfil
        exclude = ('user', 'ponto')
        widgets = {'municipio': SelectMunicipioWidget}

class AlterarSenhaForm(forms.ModelForm):
    password_conf = forms.CharField(label=u"Confirmação", widget=forms.PasswordInput)

    def clean_password_conf(self):
        senha = self.cleaned_data['password']
        senha_conf = self.cleaned_data['password_conf']
        if senha != senha_conf:
            raise forms.ValidationError(u"As senhas não coincidem")
        return senha

    def save(self, *args, **kwargs):
        commit = kwargs.pop('commit', True)
        kwargs['commit'] = False
        instance = super(AlterarSenhaForm, self).save(*args, **kwargs)

        instance.set_password(instance.password)

        if commit:
            instance.save()
        return instance

    class Meta:
        model = User
        fields = ("password",)
        widgets = {'password':forms.PasswordInput}


        

class MensagemForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.remetente = kwargs.pop('remetente', None)
        self.destinatario = kwargs.pop('destinatario', None)
        super(MensagemForm, self).__init__(*args, **kwargs)
        if self.destinatario:
            self.fields['destinatario'].widget = forms.HiddenInput()
            self.fields['destinatario'].initial = self.destinatario
        else:
            self.fields['destinatario'].queryset = User.objects.all().exclude(pk=self.remetente.pk)

    def save(self, *args, **kwargs):
        commit = kwargs.pop('commit', True)
        kwargs['commit'] = False
        instance = super(MensagemForm, self).save(*args, **kwargs)
        if self.destinatario:
            instance.destinatario = self.destinatario
        instance.remetente = self.remetente
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Mensagem
        exclude = ('remetente', 'data')
