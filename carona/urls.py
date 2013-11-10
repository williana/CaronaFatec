from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'carona.sistema.views.home', name='home'),
    url(r'^cadastro/$', 'carona.sistema.views.cadastro', name='cadastro'),
    url(r'^conta/$', 'carona.sistema.views.conta', name='conta'),

    url(r'^login/$', login, {'template_name': 'sistema/login.html'}, name='login'),
    url(r'^logout/$', logout, {"next_page": "/"}, name='logout'),

    url(r'^mensagem/$', 'carona.sistema.views.mensagens', name='mensagem'),
    url(r'^mensagem/(?P<des_pk>\d+)/$', 'carona.sistema.views.mensagens', name='mensagem'),

    url(r'^excluir_conta/confirma/$', 'carona.sistema.views.excluir_conta',
        {'confirma': True}, name='excluir_conta_confirma'),
    url(r'^excluir_conta/$', 'carona.sistema.views.excluir_conta', name='excluir_conta'),
    url(r'^alterar_senha/$', 'carona.sistema.views.alterar_senha', name='alterar_senha'),

    url(r'^municipios_app/', include('municipios.urls')),
)
