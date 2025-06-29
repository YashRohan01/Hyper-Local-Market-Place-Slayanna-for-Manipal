# donations/views.py
from django.shortcuts import render, redirect
from .forms import DonationForm
from django.contrib.auth.decorators import login_required

@login_required
def donate_product(request):
    if request.method == 'POST':
        form = DonationForm(request.POST, user=request.user)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.donor = request.user
            donation.save()
            return redirect('home')  # or wherever you want
    else:
        form = DonationForm(user=request.user)

    return render(request, 'donations/donate_form.html', {'form': form})
