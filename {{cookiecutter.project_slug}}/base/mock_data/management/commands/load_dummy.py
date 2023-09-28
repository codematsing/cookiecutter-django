from applications.tests.factories import ApplicationFactory
from auxiliaries.benefits.tests.factories import BenefitFactory
from auxiliaries.colleges.models import College
from auxiliaries.constituent_universities.models import ConstituentUniversity
from auxiliaries.contacts.tests.factories import ContactFactory
from auxiliaries.courses.models import Course
from auxiliaries.degree_levels.models import DegreeLevel
from auxiliaries.status_tags.scholarship_status.models import ScholarshipStatus
from auxiliaries.status_tags.application_status.models import ApplicationStatus
from auxiliaries.status_tags.checklist_status.models import ChecklistStatus
from auxiliaries.status_tags.scholar_tags.models import ScholarTag
from auxiliaries.status_tags.benefits_status.models import BenefitsStatus
from auxiliaries.status_tags.rankings.models import Ranking
from auxiliaries.status_tags.scholar_status.models import ScholarStatus
from auxiliaries.status_tags.application_status.tests.factories import (
    ApplicationStatusFactory,
)
from auxiliaries.status_tags.fund_status.tests.factories import FundStatusFactory
from auxiliaries.status_tags.scholar_tags.tests.factories import ScholarTagFactory
from auxiliaries.status_tags.scholarship_status.tests.factories import (
    ScholarshipStatusFactory,
)
from auxiliaries.year_levels.tests.factories import YearLevelFactory
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.conf import settings
from donors.tests.factories import DonorFactory
from faker import Faker
from fund_accounts.tests.factories import FundAccountFactory
from posts.tests.factories import PostFactory
from random import choices, randint, choice
from scholars.tests.factories import ScholarFactory
from scholarships.benefits.tests.factories import ScholarshipBenefitFactory
from scholarships.checklists.tests.factories import ScholarshipChecklistFactory
from scholarships.qualification_sets.primary_qualifications.models import (
    ValidationCondition,
    DummyApplicantData,
    ConditionEvaluator,
)
from scholarships.qualification_sets.primary_qualifications.tests.factories import (
    PrimaryQualificationFactory,
)
from scholarships.qualification_sets.qualifications.tests.factories import (
    ScholarshipQualificationFactory,
)
from scholarships.qualification_sets.tests.factories import QualificationSetFactory
from scholarships.tests.factories import ScholarshipFactory
from file_management.tests.factories import DocumentMetadataFactory
import os
import pandas as pd
import random

random.seed(0)
Faker.seed(0)

tags_item_to_model_dict = {
        'Scholarship' : ScholarshipStatus,
        'Scholarship Post' : None,
        'Application' : ApplicationStatus,
        'Ranking' : Ranking,
        'Status of Documents' : ChecklistStatus,
        'Scholar Tag' : ScholarTag,
        'Scholar Status': ScholarStatus,
        'Benefits': BenefitsStatus
        }


class Command(BaseCommand):
    help = "create dummy data"

    def set_course_df(self):
        csv_file = os.path.join(settings.APPS_DIR, "fixtures", "courses_evaluated.csv")
        self.df = pd.read_csv(csv_file, quotechar='"')

    def load_colleges_from_df(self):
        for college in self.df["college_id"].unique():
            College.objects.get_or_create(name=college)

    def load_degrees_and_courses_from_df(self):
        for index, row in self.df.drop_duplicates(
            subset=["dl", "dl_abbr", "new_course"], keep="first"
        ).iterrows():
            dl = row["dl"]
            dl_abbr = row["dl_abbr"]
            name = row["new_course"]
            dl_object = DegreeLevel.objects.get_or_create(
                name=dl, abbreviation=dl_abbr
            )[0]
            Course.objects.get_or_create(name=name, degree=dl_object)

    def load_cu_from_df(self):
        for cu in self.df["constituent_unit"].unique():
            college_names = self.df[self.df["constituent_unit"] == cu][
                "new_course"
            ].unique()
            colleges = College.objects.filter(name__in=college_names)
            cu_object = ConstituentUniversity.objects.get_or_create(name=cu)[0]
            ContactFactory(content_object=cu_object)

    def setup_initial_users(self):
        sao = Group.objects.get_or_create(name="Scholarship Affairs Officers")[0]
        admin_user = get_user_model().objects.get_or_create(
            username="admin",
            email="admin@example.com",
            is_superuser=True,
            is_active=True,
            is_staff=True,
        )[0]
        sao_user = get_user_model().objects.get_or_create(
            username="sao", email="sao@up.edu.ph", is_active=True
        )[0]
        sao_user.groups.add(sao)
        for user in [sao_user, admin_user]:
            user.set_password("qwer!@#$")
            user.save()

    def set_tags_df(self):
        csv_file = os.path.join(settings.APPS_DIR, "fixtures", "tags.csv")
        self.tags_df = pd.read_csv(csv_file, quotechar='"')

    def create_status_tags_from_df(self, item):
        filtered_df = self.tags_df.loc[self.tags_df['item'] == item]
        created_tags = []
        for index in filtered_df.index:
            name = filtered_df['tag_name'][index]
            desc = filtered_df['description'][index]
            fg = filtered_df['foreground_hex'][index]
            bg = filtered_df['background_hex'][index]
            created_tags.append(tags_item_to_model_dict[item].objects.get_or_create(name=name,
                                            description=desc,
                                            foreground=fg,
                                            background=bg)[0])

        return created_tags


    def generate_scholarship_status_tags(self):
        return self.create_status_tags_from_df('Scholarship')

    def generate_application_status_tags(self):
        return self.create_status_tags_from_df('Application')

    def generate_checklist_status_tags(self):
        return self.create_status_tags_from_df('Status of Documents')

    def generate_scholar_tags(self):
        return self.create_status_tags_from_df('Scholar Tag')

    def generate_benefits_status_tags(self):
        return self.create_status_tags_from_df('Benefits')

    def generate_rankings_tags(self):
        return self.create_status_tags_from_df('Ranking')

    def generate_scholar_status_tags(self):
        return self.create_status_tags_from_df('Scholar Status')

    def generate_tags(self):
        self.set_tags_df()
        # self.scholarship_status = ScholarshipStatusFactory.create_batch(5)
        self.scholarship_status = self.generate_scholarship_status_tags()
        # self.app_status = ApplicationStatusFactory.create_batch(5)
        self.app_status = self.generate_application_status_tags()
        self.benefits = BenefitFactory.create_batch(5)
        self.benefit_status_tag = self.generate_benefits_status_tags()
        # self.scholar_tags = ScholarTagFactory.create_batch(5)
        self.scholar_tags = self.generate_scholar_tags()
        self.checklist_status = self.generate_checklist_status_tags()
        self.ranking_tags = self.generate_rankings_tags()
        self.scholar_status = self.generate_scholar_status_tags()

        self.fund_status = FundStatusFactory.create_batch(5)
        self.year_levels = YearLevelFactory.create_batch(4)

    def setup_validation_condition(self):
        _eval = {
            "gwa": ConditionEvaluator.LessThanEqual,
            "income": ConditionEvaluator.LessThanEqual,
            "year_level": ConditionEvaluator.MultiModelChoice,
            "course": ConditionEvaluator.MultiModelChoice,
            "university": ConditionEvaluator.MultiModelChoice,
        }
        for field in DummyApplicantData._meta.fields:
            if field.name in _eval.keys():
                data = {
                    "field_name_mapping": field.name,
                    "model_mapping": ContentType.objects.get(
                        model="dummyapplicantdata"
                    ),
                    "category_name": field.name,
                    "condition_evaluator": _eval[field.name],
                    "initial_criterion": f"{field.name} must meet value:",
                }
                _obj = ValidationCondition.objects.get_or_create(**data)[0]

    def _setup_applicant_data(self, qualification_set, applicant):
        applicant_data = {}
        for qual in qualification_set.qualifications.filter(
            primaryqualification__isnull=False
        ):
            qual = qual.primaryqualification
            attribute = qual.validation_criterion.field_name_mapping
            if qual.primaryqualification.validation_criterion.condition_evaluator in [
                ConditionEvaluator.ModelChoice,
                ConditionEvaluator.MultiModelChoice,
            ]:
                applicant_data[attribute] = choice(qual.deserialize_values())
            else:
                applicant_data[attribute] = (
                    choice([0.5, 0.75, 1]) * qual.deserialize_values()
                )
        applicant_data["user"] = applicant
        DummyApplicantData.objects.get_or_create(**applicant_data)

    def generate_donors_to_scholars(self):
        for donor in DonorFactory.create_batch(5):
            fund_account_number = choices([1, 2], [0.7, 0.3])[0]
            for fund in FundAccountFactory.create_batch(
                fund_account_number, donor=donor, status=choice(self.fund_status)
            ):
                scholarship_number = randint(1, 3)
                for scholarship in ScholarshipFactory.create_batch(
                    scholarship_number,
                    fund_account=fund,
                    status=choice(self.scholarship_status),
                ):
                    for benefit in self.benefits:
                        value = randint(1, 7) * 1000
                        ScholarshipBenefitFactory(
                            scholarship=scholarship, benefit=benefit, value=value
                        )
                    DocumentMetadataFactory.create_batch(2, content_object=scholarship)
                    ScholarshipChecklistFactory.create_batch(3, scholarship=scholarship)
                    set_number = choices([1, 3], [0.7, 0.3])[0]
                    for _set in QualificationSetFactory.create_batch(
                        set_number, scholarship=scholarship
                    ):
                        for condition in ValidationCondition.objects.all():
                            PrimaryQualificationFactory.create(
                                validation_criterion=condition,
                                scholarship=scholarship,
                                set=_set,
                            )
                        ScholarshipQualificationFactory(
                            set=_set, scholarship=scholarship
                        )
                        applicants_number = randint(1, _set.no_slots + 1)
                        for app in ApplicationFactory.create_batch(
                            applicants_number,
                            scholarship=scholarship,
                            qualification_set=_set,
                            status=choice(self.app_status),
                        ):
                            self._setup_applicant_data(_set, app.applicant)
                            if choice([True, False]):
                                ScholarFactory.create(
                                    application=app,
                                    scholarship=scholarship,
                                    tag=choice(self.scholar_tags),
                                )

    def generate_blog_posts(self):
        PostFactory.create_batch(20)

    def handle(self, *args, **kwargs):
        self.set_course_df()
        self.load_colleges_from_df()
        self.load_degrees_and_courses_from_df()
        self.load_cu_from_df()
        self.setup_initial_users()
        self.setup_validation_condition()
        self.generate_tags()
        self.generate_donors_to_scholars()
        self.generate_blog_posts()
