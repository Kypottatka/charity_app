from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.urls import reverse

from .forms import (
    FundraisingCampaignForm,
    CommentForm
)
from .models import (
    CustomUser,
    UserProfile,
    FundProfile,
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
    if user.is_fund:
        return redirect('main:fund_profile', fund_id=user_id)

    user_profile, created = UserProfile.objects.get_or_create(user=user)

    volunteer_vacancy = VolunteerVacancy.objects.filter(user=user)
    nonprofit_event = NonprofitEvent.objects.filter(user=user)

    posts = list(volunteer_vacancy) + list(nonprofit_event)

    page_number = request.GET.get('page')
    page_obj = paginator(page_number, posts)
    context = {
        'user': user,
        'user_profile': user_profile,
        'posts': posts,
        'page_obj': page_obj,
    }

    for post in posts:
        if isinstance(post, VolunteerVacancy):
            post.show_link = True
            post.link_url = reverse(
                'main:volunteer_vacancy',
                args=[user_id, post.id])
        elif isinstance(post, NonprofitEvent):
            post.show_link = True
            post.link_url = reverse(
                'main:nonprofit_event',
                args=[user_id, post.id])
        else:
            post.show_link = False

    return render(request, template, context)


def fund_profile(request, fund_id):
    template = 'main/fund_profile.html'

    fund = get_object_or_404(CustomUser, id=fund_id, is_fund=True)
    fundraising_campaigns = FundraisingCampaign.objects.filter(fund=fund)

    fund_profile = FundProfile.objects.get(user=fund)

    page_number = request.GET.get('page')
    page_obj = paginator(page_number, fundraising_campaigns)
    context = {
        'fund_profile': fund_profile,
        'fund': fund,
        'posts': fundraising_campaigns,
        'page_obj': page_obj,
    }

    for post in fundraising_campaigns:
        post.link_url = reverse(
            'main:fundraising_campaign',
            args=[fund_id, post.id])
    return render(request, template, context)


def list_funds(request):
    template = 'main/funds.html'
    funds = FundProfile.objects.all()
    page_obj = paginator(request.GET.get('page'), funds)

    context = {
        'page_obj': page_obj,
    }

    for fund in funds:
        fund_user = fund.user
        fund.link_url = reverse(
            'main:fund_profile',
            args=[fund_user.id])
    return render(request, template, context)


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


def base_post_view(request, post_id, template_name, model, form_class):
    post = get_object_or_404(model, id=post_id)
    context = {
        'post': post,
        'form': form_class(),
    }
    return render(request, template_name, context)


def fundraising_campaign_view(request, fund_id, pk):
    template = 'includes/article_campaign.html'
    return base_post_view(
        request,
        pk,
        template,
        FundraisingCampaign,
        CommentForm
    )


def volunteer_vacancy_view(request, user_id, pk):
    template = 'includes/article.html'
    return base_post_view(
        request,
        pk,
        template,
        VolunteerVacancy,
        CommentForm
    )


def nonprofit_event_view(request, user_id, pk):
    template = 'includes/article.html'
    return base_post_view(
        request,
        pk,
        template,
        NonprofitEvent,
        CommentForm
    )


def base_post_list_view(request, fund_id, template_name, model):
    posts = model.objects.filter(fund_id=fund_id)
    page_obj = paginator(request.GET.get('page'), posts)
    return render(request, template_name, {'page_obj': page_obj})


def fundraising_campaign_list_view(request, fund_id):
    return base_post_list_view(
        request,
        fund_id,
        'main/fundraising_campaign_list.html',
        FundraisingCampaign
    )


def volunteer_vacancy_list_view(request, fund_id):
    return base_post_list_view(
        request,
        fund_id,
        'main/fundraising_campaign_list.html',
        VolunteerVacancy
    )


def nonprofit_event_list_view(request, fund_id):
    return base_post_list_view(
        request,
        fund_id,
        'main/fundraising_campaign_list.html',
        NonprofitEvent
    )
