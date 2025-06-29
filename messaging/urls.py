from django.urls import path
from . import views

urlpatterns = [
    path('chat_inbox/', views.chat_inbox, name='chat_inbox'),
    path('compose/<str:receiver_phone>/<int:product_id>', views.compose_message, name='compose_message'),
    path('thread/<str:user_id>/<int:product_id>/', views.chat_thread, name='chat_thread'),
]
