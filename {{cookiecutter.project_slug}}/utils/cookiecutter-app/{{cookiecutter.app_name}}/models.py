{% raw %}
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

# Create your models here.
class {{cookiecutter.snake_case_model_name}}(models.Model):
    name = models.CharField(
        max_length=128, 
        blank=True, 
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL)

    class Meta:
        permissions = [
            ('add_<model>_<model_fk>', 'Can add {{ cookiecutter.app_name[:-1]|replace('_', ' ')|title}} <model_fk>')
            ('change_<model>_<model_fk>', 'Can change {{ cookiecutter.app_name[:-1]|replace('_', ' ')|title}} <model_fk>')
            ('view_<model>_<model_fk>', 'Can view {{ cookiecutter.app_name[:-1]|replace('_', ' ')|title}} <model_fk>')
            ('remove_<model>_<model_fk>', 'Can remove {{ cookiecutter.app_name[:-1]|replace('_', ' ')|title}} <model_fk>')
            ('delete_<model>_<model_fk>', 'Can delete {{ cookiecutter.app_name[:-1]|replace('_', ' ')|title}} <model_fk>')
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            "{{cookiecutter.app_name}}:detail", 
            kwargs={"pk": self.pk}
            )

    def get_update_url(self):
        return reverse(
            "{{cookiecutter.app_name}}:update", 
            kwargs={"pk": self.pk}
            )

    def get_delete_url(self):
        return reverse(
            "{{cookiecutter.app_name}}:delete", 
            kwargs={"pk": self.pk}
            )
{% endraw %}