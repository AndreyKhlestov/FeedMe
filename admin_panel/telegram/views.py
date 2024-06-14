import asyncio
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from admin_panel.telegram.forms import MailingForm, ReportForm
from admin_panel.telegram.models import Mailing, Report, TradingPoint, \
    ReportImage


@login_required
def mailing(request):
    if request.method == 'POST':
        form = MailingForm(request.POST, request.FILES)
        if not form.is_valid():
            for error in form.errors.values():
                messages.error(request, error.data[0].message)
            return redirect('admin:telegram_mailing_add')

        data = form.cleaned_data
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        if data.get('schedule_checkbox'):
            date_malling = data.get('schedule_datetime')
            text_success = 'Рассылка успешно зарегистрирована'
        else:
            date_malling = timezone.now()
            text_success = 'Рассылка успешно зарегистрирована и будет запущена в течении 1 минуты.'

        Mailing.objects.create(
            media_type=data['media_type'],
            text=data['message_text'],
            date_malling=date_malling,
            file=data.get('file')
        )
        messages.success(request, text_success)
    return redirect('admin:telegram_mailing_changelist')


def report(request, user_id):
    points = TradingPoint.objects.all()
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.wet_cats = form.cleaned_data['wet_cats']
            report.dry_cats = form.cleaned_data['dry_cats']
            report.wet_dogs = form.cleaned_data['wet_dogs']
            report.dry_dogs = form.cleaned_data['dry_dogs']
            report.save()
            for file in request.FILES.getlist('images'):
                ReportImage.objects.create(report=report, image=file)
            return HttpResponse('Успешно!')
    else:
        form = ReportForm()

    return render(request, 'index.html', {'form': form, 'points': points})
