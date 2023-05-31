from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin


class OwnerListView(ListView):
    """
    Sub-class of inbuilt list_view
    """


class OwnerDetailView(DetailView):
    """
    Sub-class
    """


class OwnerCreateView(LoginRequiredMixin, CreateView):

    def form_valid(self, form):
        object_ = form.save(commit=False)
        object_.owner = self.request.user
        object_.save()
        return super().form_valid(form)


class OwnerUpdateView(LoginRequiredMixin, UpdateView):

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerDeleteView(LoginRequiredMixin, DeleteView):

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)
