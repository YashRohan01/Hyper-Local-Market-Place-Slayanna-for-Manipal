from django.views.generic import CreateView,DetailView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .models import Product, ProductImage, Category
from .forms import ProductForm, ProductImageFormSet

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/create.html'
    success_url = reverse_lazy('home')  # Or your preferred success URL

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['image_formset'] = ProductImageFormSet(
                self.request.POST, 
                self.request.FILES,
                queryset=ProductImage.objects.none()  # Empty queryset for new products
            )
        else:
            context['image_formset'] = ProductImageFormSet(
                queryset=ProductImage.objects.none()
            )
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']
    
        self.object = form.save(commit=False)
        self.object.seller = self.request.user
        self.object.save()

    # ✅ Set many-to-many category field from manually submitted checkboxes
        categories = self.request.POST.getlist('category')
        self.object.category.set(categories)

        if image_formset.is_valid():
            instances = image_formset.save(commit=False)
            for instance in instances:
                instance.product = self.object
                instance.save()
            return redirect(self.get_success_url())

        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        # You can customize where to redirect after successful creation
        return reverse_lazy('home')
    
class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/detail.html'