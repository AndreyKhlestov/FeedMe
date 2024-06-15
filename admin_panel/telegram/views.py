import asyncio
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone

from admin_panel.telegram.forms import MailingForm
from admin_panel.telegram.models import (
    Mailing, TradingPoint, ReceivingReport, ReportPhoto, TgUser, Feed,
    FeedAmount, FinalDeliveryReport, TransferReport,
)


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


def create_receiving_report(request, user_id):
    """Создание отчета по получению корма с точки"""
    tg_user = get_object_or_404(TgUser, id=user_id)
    feeds = Feed.objects.all()
    points = TradingPoint.objects.all()
    if request.method == 'POST':
        data = request.POST
        trading_point = get_object_or_404(
            TradingPoint, id=data.get('trading_point')
        )
        comment = data.get('comment')
        report = ReceivingReport.objects.create(
            user=tg_user,
            comment=comment,
            trading_point=trading_point,
        )

        for feed in feeds:
            amount = int(data.get(f'feed_{feed.id}'))
            if amount > 0:
                FeedAmount.objects.create(
                    feed=feed,
                    amount=amount,
                    receiving_report=report,
                )

        for file in request.FILES.getlist('images'):
            ReportPhoto.objects.create(
                receiving_report=report, photo=file,
            )
        return redirect('tg:success')

    context = {
        'points': points,
        'feeds': feeds,
    }

    return render(request, 'take_food_report.html', context)


def create_feed_report(request, user_id):
    """Создание отчета по кормлению"""
    tg_user = get_object_or_404(TgUser, id=user_id)
    feeds = tg_user.feeds_amount.all()
    if request.method == 'POST':
        data = request.POST
        address = data.get('address')
        comment = data.get('comment')
        report = FinalDeliveryReport.objects.create(
            user=tg_user,
            comment=comment,
            address=address,
        )

        for feed in feeds:
            amount = int(data.get(f'feed_{feed.id}'))
            if amount > 0:
                FeedAmount.objects.create(
                    feed=feed.feed,
                    amount=amount,
                    delivery_report=report,
                )

        for file in request.FILES.getlist('images'):
            ReportPhoto.objects.create(
                delivery_report=report, photo=file,
            )
        return redirect('tg:success')

    context = {
        'feeds': feeds
    }

    return render(request, 'feed_food_report.html', context)


def check_phone_number(request, user_id):
    """Проверка введенного номера телефона"""
    if request.method == 'POST':
        data = request.POST
        phone_number = data.get('phone_number')
        tg_user_recipient = TgUser.objects.filter(
            phone_number=phone_number).first()

        def render_with_message(message):
            return render(request,
                          'check_phone_number.html',
                          {'data': data, 'message': message})

        if not tg_user_recipient:
            return render_with_message('Пользователь с таким номером не найден')

        if not tg_user_recipient.bot_unblocked:
            return render_with_message('Пользователь заблокировал бота')

        if not tg_user_recipient.is_unblocked:
            return render_with_message('Пользователь заблокирован администратором')

        tg_user = get_object_or_404(TgUser, id=user_id)
        # Если пользователь найден, перенаправление к следующему шагу
        return redirect('tg:transfer_report', user_id=tg_user.id, recipient_id=tg_user_recipient.id)

    return render(request, 'check_phone_number.html')


def create_transfer_report(request, user_id, recipient_id):
    """Создание отчета по передаче корма от одного пользователя к другому"""
    tg_user = get_object_or_404(TgUser, id=user_id)
    feeds = tg_user.feeds_amount.all()
    recipient = get_object_or_404(TgUser, id=recipient_id)
    if request.method == 'POST':
        data = request.POST
        comment = data.get('comment')
        report = TransferReport.objects.create(
            user=tg_user,
            recipient=recipient,
            comment=comment
        )

        for feed in feeds:
            amount = int(data.get(f'feed_{feed.id}'))
            if amount > 0:
                FeedAmount.objects.create(
                    feed=feed.feed,
                    amount=amount,
                    transfer_report=report,
                )

        for file in request.FILES.getlist('images'):
            ReportPhoto.objects.create(
                transfer_report=report, photo=file,
            )
        return redirect('tg:transfer_success', recipient_id=recipient.id)

    context = {
        'feeds': feeds,
        'recipient': recipient,
    }

    return render(request, 'transfer_food_report.html', context)


def transfer_success(request, recipient_id):
    recipient = get_object_or_404(TgUser, id=recipient_id)
    return render(request, 'transfer_success.html', {'recipient': recipient})


def success(request):
    return render(request, 'success.html')
