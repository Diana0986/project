from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Events, Clubs, Services, Support, News, Zayvka
from .forms import ZayvkaForm

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
    if request.method == 'POST':
        form = ZayvkaForm(request.POST)
        if form.is_valid():
            proposal = form.save()
            messages.success(
                request, 
                f'Предложение "{proposal.initiative_name}" отправлено!'
            )
            return redirect('/supports/initiative-form/')
        else:
            # Форма содержит ошибки, они будут отображены в шаблоне
            pass
    else:
        form = ZayvkaForm()
    
    return render(request, 'main/support/form.html', {'form': form})