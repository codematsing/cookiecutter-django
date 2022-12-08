from django.views.generic import DetailView

# Create your views here.


class DetailView(DetailView):
    """Allows use of fields in detail view for template view
    Use in tags in 'utils/detail_wrapper/tags.py'
    \{\% load detail \%\}
    \{\% detail fields \%\}
    """

    fields = "__all__"

    def get_context_data(self, *arg, **kwargs):
        context = super().get_context_data(*arg, **kwargs)
        context["fields"] = self.get_field_context()
        return context

    def get_field_context(self):
        obj = self.get_object()
        if hasattr(self, "model"):
            if self.fields == "__all__":
                self.fields = self.model._meta.fields
        return {getattr(obj, field) for field in self.fields}
