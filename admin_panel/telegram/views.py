from datetime import datetime
import asyncio
import requests

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.db.models import Sum

from admin_panel.telegram.forms import MailingForm
from admin_panel.telegram.models import (
    Mailing, TradingPoint, ReceivingReport, ReportPhoto, TgUser, Feed,
    FeedAmount, FinalDeliveryReport, TransferReport,
)
from tg_bot.config import BOT_TOKEN


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


@login_required
def statistics(request):
    months = [
        'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
        'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
    ]

    # Получаем все торговые точки
    trading_points = TradingPoint.objects.all()

    # Создаем словарь для хранения данных
    data = []
    for point in trading_points:

        # Создаем словарь для каждой точки
        point_data = {'title': point.title, 'data': []}

        for month in range(1, 13):
            # Получаем количество корма за каждый месяц
            start_date = datetime(datetime.now().year, month, 1)
            end_date = datetime(datetime.now().year, month + 1,
                                1) if month < 12 else datetime(
                datetime.now().year + 1, 1, 1)

            feed_amount = FeedAmount.objects.filter(
                receiving_report__trading_point=point,
                receiving_report__created__range=(start_date, end_date)
            ).aggregate(total_amount=Sum('amount'))['total_amount'] or 0

            # Добавляем данные в список
            point_data['data'].append(feed_amount)

        data.append(point_data)

    data = {
        'months': months,
        'data': data,
    }
    return render(request, 'statistics.html', data)


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

        if not tg_user_recipient.id:
            return render_with_message('Пользователь не завершил регистрацию в боте')

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
        list_of_amounts = []
        for feed in feeds:
            amount = int(data.get(f'feed_{feed.id}'))
            if amount > 0:
                feed_amount = FeedAmount.objects.create(
                    feed=feed.feed,
                    amount=amount,
                    transfer_report=report,
                )
                list_of_amounts.append(feed_amount)

        for file in request.FILES.getlist('images'):
            ReportPhoto.objects.create(
                transfer_report=report, photo=file,
            )

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        feed_names = "\n".join([f"{amount.feed.name}: {amount.amount} ({amount.feed.unit_measure})" for amount in list_of_amounts])
        text = (
            f"Пользователь {tg_user.full_name} передал вам корм, подтвердите получение.\n\n"
            f"Наименование:\n{feed_names}\n"
        )
        payload = {
            'chat_id': recipient.id,
            'text': text,
            'reply_markup': {
                'inline_keyboard': [
                    [
                        {'text': 'Отклонить ❌', 'callback_data': f'cancel_report_{report.id}'},
                        {'text': 'Подтвердить ✅', 'callback_data': f'confirm_report_{report.id}'}
                    ]
                ]
            }
        }
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(url, json=payload, headers=headers)
        dict_json = response.json()

        if dict_json.get('error_code'):
            if dict_json.get('description') == 'Forbidden: bot was blocked by the user':
                recipient.bot_unblocked = False
                recipient.save()
            report.delete()
            return redirect('tg:transfer_bad_success')
        return redirect('tg:transfer_success', recipient_id=recipient.id)

    context = {
        'feeds': feeds,
        'recipient': recipient,
    }

    return render(request, 'transfer_food_report.html', context)


def bad_success(request):
    return render(request, 'bad_success.html')


def transfer_success(request, recipient_id):
    recipient = get_object_or_404(TgUser, id=recipient_id)
    return render(request, 'transfer_success.html', {'recipient': recipient})


def success(request):
    return render(request, 'success.html')
