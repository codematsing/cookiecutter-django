from django.views.generic import DetailView

# Create your views here.


class DetailView(DetailView):
    """Rationale: Allows use of fields in detail view for template view
    Use in tags in 'utils/detail_wrapper/tags.py'
    {% raw %}
    {% load detail %}
    {% detail fields %}
    {% endraw %}

    Why have this?
    So that each detail view will just specify fields to be shown
    Better solution than disabling UpdateView
    This inherits from DetailView than UpdateView,
    however it functions similar to updateview fields,
    it uses fields to specify what fields to show and in order
    and uses a template to load it

    How to use in file?
    from utils.base_views.import BaseDetailView

    class ModelDetailView(BaseDetailView):
        fields = '__all__'
        template_name = 'pages/detail.html'
    """

    fields = "__all__"
    def get_field_value(self, obj, field_name):
        return getattr(obj, field_name)

    def get_context_data(self, *arg, **kwargs):
        context = super().get_context_data(*arg, **kwargs)
        context["fields"] = self.get_field_context()
        return context

    def get_fields(self):
        return self.fields

    def get_field_context(self):
        obj = self.get_object()
        fields = self.get_fields()
        if hasattr(self, "model"):
            if fields == "__all__":
                fields = [field.name for field in self.model._meta.fields]
            return {field:self.get_field_value(obj, field) for field in fields}
        return {}