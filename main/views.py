from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Events, Clubs, Services, Support, News
from .forms import ZayvkaForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

def popular_list(request):
    news = News.objects.order_by('-created_at')[:3]
    return render(request,
                  'main/index/index.html',
                  {'news': news})

def new_detail(request, slug):
    new = get_object_or_404(News,
                                slug=slug)
    return render(request,
                  'main/news/detail.html',
                  {'new': new})
def new_list(request):
    news_list = News.objects.all().order_by('-created_at')
    paginator = Paginator(news_list, 3)
    page = request.GET.get('page', 1)
    current_page = paginator.page(int(page))
    return render(request,
                  'main/news/list.html',
                  {'news': current_page})
    
def events_list(request):
    events = Events.objects.all().order_by('order')
    return render(request,
                  'main/events/list.html',
                  {'events': events})

def clubs_list(request):
    clubs = Clubs.objects.all()
    return render(request,
                  'main/clubs/list.html',
                  {'clubs': clubs})

def services_list(request):
    services = Services.objects.all()
    return render(request,
                  'main/services/list.html',
                  {'services': services})

def support_list(request):
    supports = Support.objects.all()
    return render(request,
                  'main/support/list.html',
                  {'supports': supports})

def initiative_form(request):
    initial_data = {}
    
    if request.user.is_authenticated:
        user = request.user
        
        # Формируем ФИО из отдельных полей
        full_name_parts = []
        
        if user.last_name:  # Фамилия
            full_name_parts.append(user.last_name)
        
        if user.first_name:  # Имя
            full_name_parts.append(user.first_name)
        
        if user.middle_name:  # Отчество (если есть)
            full_name_parts.append(user.middle_name)
        
        # Объединяем через пробел
        full_name = ' '.join(full_name_parts) if full_name_parts else ''
        
        initial_data = {
            'full_name': full_name,
            'email': user.email,
            'phone': user.phone if hasattr(user, 'phone') else '',
            'birth_date': user.birthday if hasattr(user, 'birthday') else None,
            'vk_link': user.link_vk if hasattr(user, 'link_vk') else '',
        }
    
    if request.method == 'POST':
        form = ZayvkaForm(request.POST, initial=initial_data)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.id = None  # ← ЭТО РЕШАЕТ ПРОБЛЕМУ
            proposal.save()
            messages.success(
                request, 
                f'Предложение "{proposal.initiative_name}" отправлено!'
            )
            return redirect('/supports/initiative-form/')
    else:
        # GET-запрос
        form = ZayvkaForm(initial=initial_data)
    
    return render(request, 'main/support/form.html', {'form': form})