import asyncio
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from admin_panel.telegram.forms import MailingForm, ReportForm
from admin_panel.telegram.models import Mailing, TgUser, Report


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
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            wet_food = form.cleaned_data['wet_food']
            dry_food = form.cleaned_data['dry_food']
            received = form.cleaned_data['received']
            photo = form.cleaned_data['photo']

            Report.objects.create(name=name,
                                  wet_food=wet_food,
                                  dry_food=dry_food,
                                  photo=photo,
                                  received=received,
                                  )
            return HttpResponse('Успешно!')
    else:
        form = ReportForm()
    return render(request, 'form_income.html', {'form': form})



