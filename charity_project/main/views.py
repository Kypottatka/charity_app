from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.urls import reverse

from .forms import (
    FundraisingCampaignForm,
    VolunteerVacancyForm,
    NonprofitEventForm,
    CommentFundForm,
    CommentNonprofitForm,
    CommentVolunteerForm,
    DonationForm,
    EditUserProfileForm,
    EditFundProfileForm
)
from .models import (
    CustomUser,
    UserProfile,
    FundProfile,
    FundraisingCampaign,
    VolunteerVacancy,
    NonprofitEvent,
    CommentFund,
    CommentNonprofit,
    CommentVolunteer,
    Donation,
)


def paginator(page_number, posts):
    paginator = Paginator(posts, settings.POSTS_ON_PAGE)
    page_obj = paginator.get_page(page_number)
    return page_obj


def index(request):
    template = 'main/index.html'
    donations = Donation.objects.all().order_by('-created_at')[:5]
    context = {
        'donations': donations,
    }
    return render(request, template, context)


def user_profile(request, user_id):
    template = 'main/user_profile.html'
    user = get_object_or_404(CustomUser, id=user_id)
    if user.is_fund:
        return redirect('main:fund_profile', fund_id=user_id)

    if request.user.id == user_id:
        return redirect('main:user_profile_me')

    user_profile, created = UserProfile.objects.get_or_create(user=user)

    volunteer_vacancy = VolunteerVacancy.objects.filter(user=user).order_by(
        '-created_at'
    )
    nonprofit_event = NonprofitEvent.objects.filter(user=user).order_by(
        '-created_at'
    )

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


def edit_user_profile(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.user.id != user_id:
        return redirect('main:user_profile_me')

    user_profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = EditUserProfileForm(
            request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('main:user_profile', user_id=user_id)
    else:
        form = EditUserProfileForm(instance=user_profile)

    context = {
        'user': user,
        'user_profile': user_profile,
        'form': form,
    }
    return render(request, 'main/edit_user_profile.html', context)


def fund_profile(request, fund_id):
    template = 'main/fund_profile.html'

    donations = Donation.objects.filter(fund_id=fund_id)
    raised = 0
    for donation in donations:
        raised += donation.amount

    fund = get_object_or_404(CustomUser, id=fund_id, is_fund=True)

    try:
        fund_profile = FundProfile.objects.get(user=fund)
    except FundProfile.DoesNotExist:
        fund_profile = FundProfile.objects.create(
            user=fund,
            name=fund.username
        )

    fundraising_campaigns = FundraisingCampaign.objects.filter(
        fund=fund).order_by('-created_at')

    fund_profile = FundProfile.objects.get(user=fund)

    page_number = request.GET.get('page')
    page_obj = paginator(page_number, fundraising_campaigns)
    context = {
        'fund_profile': fund_profile,
        'fund': fund,
        'posts': fundraising_campaigns,
        'page_obj': page_obj,
        'show_fund_link': True,
        'raised': int(raised),
    }
    return render(request, template, context)


def edit_fund_profile(request, fund_id):
    fund = get_object_or_404(CustomUser, id=fund_id)
    if request.user.id != fund_id:
        return redirect('main:fund_profile_me')

    fund_profile, created = FundProfile.objects.get_or_create(user=fund)

    if request.method == 'POST':
        form = EditFundProfileForm(
            request.POST, request.FILES, instance=fund_profile)
        if form.is_valid():
            form.save()
            return redirect('main:fund_profile', fund_id=fund_id)
    else:
        form = EditFundProfileForm(instance=fund_profile)

    context = {
        'fund': fund,
        'fund_profile': fund_profile,
        'form': form,
    }
    return render(request, 'main/edit_fund_profile.html', context)


def list_funds(request):
    template = 'main/funds.html'
    funds = FundProfile.objects.all()
    page_obj = paginator(request.GET.get('page'), funds)

    context = {
        'page_obj': page_obj,
    }
    return render(request, template, context)


def base_post_view(request, post_id, template_name, model, form_class):
    post = get_object_or_404(model, id=post_id)
    if model == FundraisingCampaign:
        context = {
            'post': post,
            'form': form_class(),
            'comments': CommentFund.objects.filter(post=post),
        }
    elif model == NonprofitEvent:
        context = {
            'post': post,
            'form': form_class(),
            'comments': CommentNonprofit.objects.filter(post=post),
        }
    elif model == VolunteerVacancy:
        context = {
            'post': post,
            'form': form_class(),
            'comments': CommentVolunteer.objects.filter(post=post),
        }
    return render(request, template_name, context)


def fundraising_campaign_view(request, fund_id, pk):
    template = 'posts/fundraising_campaign_detail.html'
    return base_post_view(
        request,
        pk,
        template,
        FundraisingCampaign,
        CommentFundForm
    )


def volunteer_vacancy_view(request, user_id, pk):
    template = 'posts/volunteer_vacancy_detail.html'
    return base_post_view(
        request,
        pk,
        template,
        VolunteerVacancy,
        CommentNonprofitForm
    )


def nonprofit_event_view(request, user_id, pk):
    template = 'posts/nonprofit_event_detail.html'
    return base_post_view(
        request,
        pk,
        template,
        NonprofitEvent,
        CommentVolunteerForm
    )


def base_post_list_view(request, template_name, model):
    if model == FundraisingCampaign:
        posts = model.objects.all().order_by('-created_at')
        page_obj = paginator(request.GET.get('page'), posts)
        return render(request, template_name, {'page_obj': page_obj})

    elif model == VolunteerVacancy:
        posts = model.objects.all().order_by('-created_at')
        page_obj = paginator(request.GET.get('page'), posts)
        return render(request, template_name, {'page_obj': page_obj})

    posts = model.objects.all().order_by('-created_at')
    page_obj = paginator(request.GET.get('page'), posts)
    return render(request, template_name, {'page_obj': page_obj})


def fundraising_campaign_list_view(request):
    return base_post_list_view(
        request,
        'main/fundraising_campaign_list.html',
        FundraisingCampaign
    )


def volunteer_vacancy_list_view(request):
    return base_post_list_view(
        request,
        'main/volunteer_vacancy_list.html',
        VolunteerVacancy
    )


def nonprofit_event_list_view(request):
    return base_post_list_view(
        request,
        'main/nonprofit_event_list.html',
        NonprofitEvent
    )


def add_comment_fund(request, fund_id, pk):
    post = FundraisingCampaign.objects.get(pk=pk)
    form = CommentFundForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.content = request.POST.get('content')
        comment.user = request.user
        comment.post = post
        comment.save()
    return redirect('main:fundraising_campaign', fund_id=fund_id, pk=pk)


def add_comment_nonprofit(request, user_id, pk):
    post = NonprofitEvent.objects.get(pk=pk)
    form = CommentNonprofitForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.content = request.POST.get('content')
        comment.user = request.user
        comment.post = post
        comment.save()
    return redirect('main:nonprofit_event', user_id=user_id, pk=pk)


def add_comment_volunteer(request, user_id, pk):
    post = VolunteerVacancy.objects.get(pk=pk)
    form = CommentVolunteerForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.content = request.POST.get('content')
        comment.user = request.user
        comment.post = post
        comment.save()
    return redirect('main:volunteer_vacancy', user_id=user_id, pk=pk)


def create_fundraising_campaign(request):
    if not request.user.is_fund:
        return redirect('main:index')
    template = 'main/create_fundraising_campaign.html'
    if request.method == 'POST':
        form = FundraisingCampaignForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.fund = request.user
            post.title = request.POST.get('title')
            post.description = request.POST.get('description')
            post.goal = request.POST.get('goal')
            post.save()
            return redirect('main:fundraising_campaign_list')
    else:
        form = FundraisingCampaignForm()
    return render(request, template, {'form': form})


def create_volunteer_vacancy(request):
    template = 'main/create_volunteer_vacancy.html'
    if request.method == 'POST':
        form = VolunteerVacancyForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.title = request.POST.get('title')
            post.description = request.POST.get('description')
            form.save()
            return redirect('main:volunteer_vacancy_list')
    else:
        form = VolunteerVacancyForm()
    return render(request, template, {'form': form})


def create_nonprofit_event(request):
    template = 'main/create_nonprofit_event.html'
    if request.method == 'POST':
        form = NonprofitEventForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.title = request.POST.get('title')
            post.description = request.POST.get('description')
            post.date = request.POST.get('date')
            post.location = request.POST.get('location')
            form.save()
            return redirect('main:nonprofit_event_list')
    else:
        form = NonprofitEventForm()
    return render(request, template, {'form': form})


def user_profile_me(request):
    template = 'main/user_profile.html'
    user = get_object_or_404(CustomUser, id=request.user.id)
    if user.is_fund:
        return redirect('main:fund_profile', fund_id=request.user.id)

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
                args=[request.user.id, post.id])
        elif isinstance(post, NonprofitEvent):
            post.show_link = True
            post.link_url = reverse(
                'main:nonprofit_event',
                args=[request.user.id, post.id])
        else:
            post.show_link = False

    return render(request, template, context)


def donate(request):
    funds = CustomUser.objects.filter(is_fund=True)

    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donate = form.save(commit=False)
            donate.user = request.user
            donate.fund = funds.get(id=request.POST.get('fund'))
            donate.amount = request.POST.get('amount')
            donate.save()
            return redirect('main:donations')
    else:
        form = DonationForm()
    return render(request, 'main/donate.html', {'form': form})


def donations(request):
    donations = Donation.objects.all().order_by('-created_at')
    context = {
        'donations': donations,
    }
    return render(request, 'main/donations.html', context)
