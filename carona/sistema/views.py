# coding: utf-8

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.db.models import Min, Max, Sum, Q
from django.db.models.loading import get_model
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.utils.html import mark_safe
from django.views.generic import ListView


from carona.sistema.models import Perfil, Mensagem
from carona.sistema.forms import PerfilUsuarioForm, MensagemForm, AlterarSenhaForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def home(request):
    return render(request, 'sistema/home.html', {})


def cadastro(request, pk=None):
    try:
        perfil = request.user.perfil
    except:
        perfil = None

    form = PerfilUsuarioForm(request.POST or None, instance=perfil)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, u'Usuário Cadastrado Com Sucesso')
            return redirect(reverse('home'))
    return render(request, 'sistema/cadastro.html', {'form': form})


@login_required
def excluir_conta(request, confirma=False):
    if not confirma:
        return render(request, 'sistema/excluir_conta.html', {})

    request.user.is_active = False
    request.user.save()
    logout(request)
    return redirect(reverse('home'))

@login_required
def alterar_senha(request):
    form = AlterarSenhaForm(request.POST or None, instance=request.user)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, u'Senha alterada com sucesso')
            return redirect(reverse('home'))
    return render(request, 'sistema/alterar_senha.html', {'form': form})

@login_required
def conta(request):
    return cadastro(request)


@login_required
def mensagens(request, des_pk=None):
    user = request.user
    if des_pk:
        if int(des_pk) == user.pk:
            raise Http404

    destinatarios = []

    for mensagem in user.remetente.all():
        if mensagem.destinatario not in destinatarios:
            if mensagem.destinatario.pk != user.pk:
                destinatarios.append(mensagem.destinatario)

    if des_pk:
        destinatario = get_object_or_404(User, pk=des_pk)

        q1 = Q(destinatario=destinatario)
        q2 = Q(remetente=user)

        q3 = Q(destinatario=user)
        q4 = Q(remetente=destinatario)

        q = (q1 & q2) | (q3 & q4)

        mensagens_des = Mensagem.objects.filter(q).order_by('data')
    else:
        mensagens_des = destinatario = None

    form = MensagemForm(request.POST or None,
            destinatario=destinatario,
            remetente=user)

    if request.method == 'POST':
        if form.is_valid():
            mensagem = form.save()

            return redirect(reverse('mensagem', kwargs={'des_pk': mensagem.destinatario.pk}))

    return render(request, 'sistema/mensagem.html', {'form': form,
        'destinatarios': destinatarios,
        'mensagens_des': mensagens_des,
        'destinatario': destinatario})
