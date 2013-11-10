# coding: utf-8

from django.db import models
from django.contrib.auth.models import User
from municipios.models import Municipio

PERIODO = (
    (1, u'Manhã'),
    (2, u'Tarde'),
    (3, u'Noite'),
)

TIPO = (
    (1, u'Passageiro'),
    (2, u'Motorista'),
)


class Curso(models.Model):
    nome = models.CharField(max_length=100)

    def __unicode__(self):
        return self.nome


class Ponto(models.Model):
    # Longitude
    x = models.CharField(max_length=255)
    # Latitude
    y = models.CharField(max_length=255)


class Perfil(models.Model):
    user = models.OneToOneField(User)
    curso = models.ForeignKey(Curso)
    ponto = models.ForeignKey(Ponto)
    periodo = models.SmallIntegerField(choices=PERIODO)
    tipo = models.SmallIntegerField(choices=TIPO)
    municipio = models.ForeignKey(Municipio)
    bairro = models.CharField(max_length=55)
    rua = models.CharField(max_length=55)
    numero = models.CharField(max_length=55)
    complemento = models.CharField(max_length=255, null=True, blank=True)


class Mensagem(models.Model):
    remetente = models.ForeignKey(User, related_name='remetente')
    destinatario = models.ForeignKey(User, related_name='destinatario')
    mensagem = models.TextField()
    data = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s: %s" % (
            self.destinatario.first_name,
            self.mensagem[:50]
        )
