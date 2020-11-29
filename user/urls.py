
from django.urls import path


from user.views import create, login, index, search, detail, delete, logout, send_message

app_name='user'
urlpatterns=[
    path('create/',create,name='create'),
    path('login/',login,name='login'),
    path('index/',index,name='index'),
    path('search/',search,name='search'),
    path('detail/',detail,name='detail'),
    path('delete/<int:id>',delete,name='delete'),
    path('logout',logout,name='logout'),
    path('send_message/',send_message,name='send_message'),
]