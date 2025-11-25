from django.urls import path
from core.views import login, logout, home, listar, deletar, cadastrar, editar


urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('index/', home, name='index'),
    path('', home,name='home'),
    path('listar/', listar, name='listar'),
    path('deletar/', deletar, name='deletar'),
    path('cadastrar/', cadastrar, name='cadastrar'),
    path('editar/', editar, name='editar')
]