from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.views import View

from .forms import (
    FundraisingCampaignForm,
    CommentForm
)
from .models import (
    CustomUser,
    FundraisingCampaign,
    VolunteerVacancy,
    NonprofitEvent,
)


def paginator(page_number, posts):
    paginator = Paginator(posts, settings.POSTS_ON_PAGE)
    page_obj = paginator.get_page(page_number)
    return page_obj


def index(request):
    template = 'main/index.html'
    return render(request, template)


def user_profile(request, user_id):
    template = 'main/user_profile.html'
    user = get_object_or_404(CustomUser, id=user_id)
    return render(request, template, {'user': user})


def fund_profile(request, fund_id):
    template = 'main/fund_profile.html'
    fund = get_object_or_404(CustomUser, id=fund_id)
    return render(request, template, {'fund': fund})


def list_funds(request):
    template = 'main/funds.html'
    funds = CustomUser.objects.filter(is_fund=True)
    page_obj = paginator(request.GET.get('page'), funds)
    return render(request, template, {'page_obj': page_obj})


def create_comment(request, model_type, model_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user

            if model_type == 'fundraising_campaign':
                model = FundraisingCampaign
            elif model_type == 'volunteer_vacancy':
                model = VolunteerVacancy
            elif model_type == 'nonprofit_event':
                model = NonprofitEvent

            content_object = get_object_or_404(model, pk=model_id)
            new_comment.content_object = content_object
            new_comment.save()
            return redirect(content_object.get_absolute_url())
    else:
        form = CommentForm()

    context = {
        'form': form,
        'model_type': model_type,
        'model_id': model_id,
    }
    return render(request, 'comment_create.html', context)


def create_fundraising_campaign(request):
    template = 'main/create_fundraising_campaign.html'
    if request.method == 'POST':
        form = FundraisingCampaignForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main/index.html')
    else:
        form = FundraisingCampaignForm()
    return render(request, template, {'form': form})


class BasePostView(View):
    template_name = None
    model = None

    def get(self, request, post_id):
        post = get_object_or_404(self.model, id=post_id)
        context = {
            'post': post,
            'form': CommentForm(),
            'comments': post.comments.all(),
        }
        return render(request, self.template_name, context)


class FundraisingCampaignView(BasePostView):
    template_name = 'main/fundraising_campaign.html'
    model = FundraisingCampaign


class VolunteerVacancyView(BasePostView):
    template_name = 'main/volunteer_vacancy.html'
    model = VolunteerVacancy


class NonprofitEventView(BasePostView):
    template_name = 'main/nonprofit_event.html'
    model = NonprofitEvent


class BasePostListView(View):
    template_name = None
    model = None

    def get(self, request, fund_id):
        posts = self.model.objects.filter(fund_id=fund_id)
        page_obj = paginator(request.GET.get('page'), posts)
        return render(request, self.template_name, {'page_obj': page_obj})
