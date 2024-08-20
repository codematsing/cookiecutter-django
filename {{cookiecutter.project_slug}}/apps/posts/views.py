from typing import Any, List, Sequence
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from auxiliaries.courses.models import Course
from django.db.models.query import QuerySet
from auxiliaries.status_tags.form_status.models import FormStatus
from scholarships.qualification_sets.primary_qualifications.models import PrimaryQualification, ValidationCondition
from scholarships.qualification_sets.models import QualificationSet
from django.contrib import messages
from .models import Post, ScholarshipPost, BlogPost
from django.views.generic.list import MultipleObjectMixin
from django.views.generic import RedirectView
from django.views.generic.detail import SingleObjectMixin
from formset.views import FormView
from django.urls import reverse_lazy
from urllib.parse import urlencode
from django.http import QueryDict
from datetime import datetime
from utils.base_views.public_views import (
    PublicListView,
    PublicDetailView,)
from utils.base_views.admin_views import (
    AdminListView,
    AdminCreateView,
    AdminUpdateView,
    AdminDeleteView,
)
from posts.forms import FilterForm, PostForm
from applications.models import Application
from auxiliaries.status_tags.application_status.models import ApplicationStatus
from scholarships.qualification_sets.qualifications.models import ScholarshipQualification
from scholarships.checklists.models import ScholarshipChecklist
from auxiliaries.checklist_responses.models import ChecklistResponse
from auxiliaries.status_tags.checklist_status.models import ChecklistStatus
from utils.permissions import IsSAOPermissionMixin

import logging
logger = logging.getLogger(__name__)

# Create your views here.
class PostListView(PublicListView):
    model = BlogPost
    template_name='posts/list.html'
    paginate_by = 12

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.filter(is_published=True)
        if tag_pk:=self.request.GET.get('tag', None):
            qs = qs.filter(tags__pk=tag_pk)
        return qs

    def get_json_query(self, _dict=dict()):
        _dict = {"qualification_set__isnull":True, "is_published":True}
        return super().get_json_query(_dict)

class PostCreateView(IsSAOPermissionMixin, AdminCreateView):
    model = Post
    form_class = PostForm
    success_message = ''

class BlogPostListView(IsSAOPermissionMixin, AdminListView):
    model = BlogPost
    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        return qs.filter(is_published=True)

    def get_page_title(self):
        return 'Announcement Posts'

    def get_ajax_list_url(self):
        """Ajax list url that will be processed in template view
        """
        ajax_url = f"posts:ajax:blogs_list"
        return reverse_lazy(ajax_url, kwargs=self.kwargs)

class PostDetailView(PublicDetailView):
    model = Post
    template_name = 'posts/detail.html'

    def get_template_names(self):
        _object = self.get_object()
        if hasattr(_object, "qualification_set"):
            return 'posts/scholarship_detail.html'
        return super().get_template_names()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        _object = self.get_object()
        if hasattr(_object, "qualification_set"):
            context["user_can_apply"] = _object.qualification_set.user_can_apply(self.request.user)
            if not self.request.user.is_anonymous:
                context["user_application"] = Application.objects.filter(applicant=self.request.user, qualification_set=self.get_object().qualification_set)
        return context


class PostUpdateView(IsSAOPermissionMixin, AdminUpdateView):
    model = Post
    form_class = PostForm
    fields = ['body']

class PostDeleteView(IsSAOPermissionMixin, AdminDeleteView):
    model = Post

class ScholarshipPostListView(MultipleObjectMixin, FormView):
    model = ScholarshipPost
    template_name='posts/scholarship_list.html'
    paginate_by = 8
    form_class = FilterForm

    def get(self, request, *args, **kwargs):
        # copy from ListView
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_query_dict_from_params(self):
        params = self.request.GET.urlencode()
        query_dict = QueryDict(params)
        res = {}
        for key in query_dict:
            values = query_dict.getlist(key)
            if key in ['constituent_university', 'course', 'year_level']:
                res[key] = [int(value) for value in values]
            else:
                res[key] = int(values[0]) if values[0].isnumeric() else values[0]
        return res

    def _filter_by_primary_qualification(self, category_name, query_dict):
        value_from_form = query_dict.get(category_name, None)
        filter_kwargs = {}
        if value_from_form:
            values_list = value_from_form if isinstance(value_from_form, list) or not value_from_form else [value_from_form,]
            primary_qualifications = PrimaryQualification.objects.filter(validation_criterion__category_name=category_name)
            valid_pk_list = list(filter(lambda primary_qualification: any(primary_qualification.value_meets_validation(value, is_pk=True) for value in values_list), primary_qualifications))
            filter_kwargs.update({'qualification_set__qualifications__pk__in':valid_pk_list})
        return filter_kwargs

    def get_form(self):
        form = super().get_form()
        if self.request.user.is_anonymous:
            form.fields['qualified_applications'].widget = forms.HiddenInput()
        return form

    def get_queryset(self):
        query_dict = self.get_query_dict_from_params()
        qs = self.model.objects.filter(is_published=True)
        filter_kwargs = {}
        if title:=query_dict.get('title', False):
            filter_kwargs.update({
                'title__icontains':title
            })
        if no_slots := query_dict.get('no_slots'):
            filter_kwargs.update({
                'qualification_set__no_slots__gte':no_slots
            })
        if not bool(query_dict.get('closed_applications', True)):
            filter_kwargs.update({
                'qualification_set__application_deadline__gte':datetime.now()
            })
        if bool(query_dict.get('qualified_applications')) and not self.request.user.is_anonymous:
            qualset_pk_list = QualificationSet.objects.user_qualification_options(self.request.user).values_list('pk', flat=True)
            filter_kwargs.update({
                'qualification_set__pk__in':qualset_pk_list
            })
        else:
            filter_kwargs.update(self._filter_by_primary_qualification('constituent_university', query_dict))
            filter_kwargs.update(self._filter_by_primary_qualification('course', query_dict))
            filter_kwargs.update(self._filter_by_primary_qualification('year_level', query_dict))
            filter_kwargs.update(self._filter_by_primary_qualification('overall_gwa', query_dict))
        logger.info(filter_kwargs)
        return qs.filter(**filter_kwargs).order_by(self.get_ordering())

    def get_ordering(self) -> Sequence[str]:
        query_dict = self.get_query_dict_from_params()
        order_by = query_dict.get('order_by', "qualification_set__application_deadline")
        return order_by

    def form_valid(self, form):
        self.data = form.data
        return super().form_valid(form)

    def get_success_url(self):
        params = urlencode(self.data, doseq=True)
        url = f"{reverse_lazy('posts:scholarship_list')}?{params}"
        return url

    def get_initial(self):
        return self.get_query_dict_from_params()

class ScholarshipApplicationRedirectView(LoginRequiredMixin, SingleObjectMixin, RedirectView):
    pk_url_kwarg = "pk"
    model = ScholarshipPost

    def create_application(self, scholarship, qualification_set, user):
        application_kwargs = {
                'scholarship':scholarship,
                'qualification_set':qualification_set,
                'applicant':user,
                'status': ApplicationStatus.objects.update_or_create(name='Submitted',foreground='#000000', background='#FFFFFF')[0],
            }
        application = Application.objects.create(**application_kwargs);
        return application

    def get_redirect_url(self, *args, **kwargs):
        post = self.get_object()
        current_user = self.request.user
        if not post.qualification_set.user_can_apply(current_user):
            raise Http404

        if qualset:=getattr(post, 'qualification_set', None):
            scholarship = qualset.scholarship
            application = self.create_application(scholarship=scholarship, qualification_set=qualset, user=self.request.user)
            messages.success(self.request, f"Congratulations! You have successfully applied for {scholarship}!")
            if scholarship.supplemental_documents.count():
                messages.warning(self.request, "Please ensure to submit additional documents before the application deadline to be ensure qualification for the scholarship")
            return application.get_absolute_url()
