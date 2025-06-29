from django.shortcuts import render,redirect,get_object_or_404

# Create your views here.
# views.py (in your messages app or relevant app)

from django.contrib.auth.decorators import login_required
from users.models import User  # Adjust if your user model is elsewhere
from .models import Message
from .forms import MessageForm
from products.models import Product
from django.db.models import Q,Max

@login_required
def message_inbox(request):
    user = request.user

    # All messages where user is sender or receiver
    messages = Message.objects.filter(sender=user) | Message.objects.filter(receiver=user)
    messages = messages.order_by('-timestamp')

    context = {
        'messages': messages
    }

    return render(request, 'messaging/chat_inbox.html', context)


def compose_message(request, receiver_phone, product_id):
    sender = request.user
    receiver = get_object_or_404(User, phone_number=receiver_phone)
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = MessageForm(request.POST, sender=sender, receiver=receiver, product_id=product_id)
        if form.is_valid():
            form.save()
            return redirect('chat_inbox')  # Or wherever you want to go
    else:
        form = MessageForm(sender=sender, receiver=receiver, product_id=product_id)

    return render(request, 'messaging/compose.html', {
        'form': form,
        'receiver': receiver,
        'product':product,
    })


"""def chat_inbox(request):
    user = request.user
    #messages = Message.objects.filter(Q(sender=user) | Q(receiver=user)).order_by('-timestamp')
    messages = Message.objects.all()

    threads = {}  # key: (other_user.id, product.id), value: latest message
    for msg in messages:
        other_user = msg.receiver if msg.sender == user else msg.sender
        key = (other_user.phone_number, msg.product.id if msg.product else None)

        # Only keep the latest message per thread
        if key not in threads or msg.timestamp > threads[key].timestamp:
            threads[key] = msg

    context = {
        'threads': [{
            'user': User.objects.get(id=k[0]),
            'product': Product.objects.get(id=k[1]) if k[1] else None,
            'last_message': v
        } for k, v in threads.items()]
    }
    print(threads)
    return render(request, 'messaging/chat_inbox.html', context)
    context = {'messages':messages}
    return (request,'messaging/chat_inbox.html', context)"""


def chat_inbox(request):
    user = request.user
    messages = Message.objects.filter(Q(sender=user) | Q(receiver=user)).order_by('-timestamp')

    threads = {}
    for msg in messages:
        other_user = msg.receiver if msg.sender == user else msg.sender
        key = (other_user.phone_number, msg.product.id if msg.product else None)
        if key not in threads or msg.timestamp > threads[key].timestamp:
            threads[key] = msg

    context = {
        'threads': [{
            'user': User.objects.get(phone_number=k[0]),
            'product': Product.objects.get(id=k[1]) if k[1] else None,
            'last_message': v
        } for k, v in threads.items()]
    }

    return render(request, 'messaging/chat_inbox.html', context)


def chat_thread(request, user_id, product_id):
    current_user = request.user
    other_user = get_object_or_404(User, phone_number=user_id)
    product = get_object_or_404(Product, id=product_id)

    # Get all messages between current user and other user for this product
    messages = Message.objects.filter(
        Q(sender=current_user, receiver=other_user) | Q(sender=other_user, receiver=current_user),
        product=product
    ).order_by('timestamp')
    Message.objects.filter(sender=current_user, receiver=other_user, product_id=product_id, is_read=False).update(is_read=True)

    # Handle message form submission
    if request.method == 'POST':
        form = MessageForm(request.POST, sender=current_user, receiver=other_user, product_id=product_id)
        reply_to_id = request.POST.get('reply_to_id')
        if form.is_valid():
            new_message = form.save(commit=False)
            if reply_to_id:
                try:
                    replied_message = Message.objects.get(id=reply_to_id)
                    new_message.reply_to = replied_message
                except Message.DoesNotExist:
                    pass
            new_message.save()
            return redirect('chat_thread', user_id=other_user.phone_number, product_id=product_id)
    else:
        form = MessageForm()

    return render(request, 'messaging/chat_thread.html', {
        'messages': messages,
        'form': form,
        'receiver': other_user,
        'product': product,
        'current_user': current_user,
    })