from django.urls import path
from . import views

app_name = 'noteapp'

urlpatterns = [
    path('', views.main, name='main'),
    path('note/', views.note, name='note'),
    path('tag/', views.tag, name='tag'),
    path('details/<int:note_id>', views.details, name='details'),
    path('done/<int:note_id>', views.set_done, name='set_done'),
    path('undone/<int:note_id>', views.set_undone, name='set_undone'),
    path('delete/<int:note_id>', views.delete_note, name='delete'),
]
