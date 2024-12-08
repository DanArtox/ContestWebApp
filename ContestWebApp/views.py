from django.shortcuts import render
import requests
from django.shortcuts import get_list_or_404
from django.views import View
from django.http import HttpResponse, JsonResponse
import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from users.models import User, Percentage, ContestPerc, CheckingDatas
from datetime import datetime, timedelta

BOT_TOKEN = '7712304947:AAFGeK1ZtRmwxyEPEH5RlWlodTX9u3Myh2E'

class GetUserChance(View):
    def get(self, request):
        uid = request.GET.get('uid')
        cid = request.GET.get('cid')
        user_percantages = Percentage.objects.filter(uid=uid, cid=cid)
        res_percantages = 0.1
        for percantages in user_percantages:
            res_percantages += percantages.percent
         

        # Формируем ответ
        data = {
            'result': user_percantages
        }

        return JsonResponse(data, status=200)
    
@method_decorator(csrf_exempt, name='dispatch')
class BotAddCheckingData(View):
    def post(self, request):
        link = request.GET.get('link')
        code = request.GET.get('code')
        ltype = request.GET.get('ltype')
        token = request.GET.get('token')

        if token == 'Web-ArtoxGroupBot':
            try:
                is_link_added = CheckingDatas.objects.get(link=link)
                return JsonResponse({'error': 'Already used!'}, status=500)
            except CheckingDatas.DoesNotExist:
                CheckingDatas.objects.create(link=link, token=code, ltype=ltype)
                return JsonResponse({'successfull': True}, status=200)
        else:
            return JsonResponse({'error': 'Invalid Token!'}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class BotAddUserChance(View):
    def post(self, request):
        user_id = request.GET.get('user_id')
        cid = request.GET.get('cid')
        chance = request.GET.get('chance')
        token = request.GET.get('token')
        link = request.GET.get('link')

        if token == 'Web-ArtoxGroupBot':
            try:
                is_link_used = ContestPerc.objects.get(uid=user_id, cid=cid, link=link)
                return JsonResponse({'error': 'Already used!'}, status=500)
            except ContestPerc.DoesNotExist:
                ContestPerc.objects.create(uid=user_id, percent=chance, cid=cid, link=link, is_done=True)
                return JsonResponse({'successfull': True}, status=200)
        else:
            return JsonResponse({'error': 'Invalid Token!'}, status=500)

class AddUserChance(View):
    def post(self, request):
        body = json.loads(request.body)
        user_id = body.get('user_id')
        cid = body.get('cid')
        chance = body.get('chance')
        token = body.get('token')
        link = body.get('link')

        if token == 'Web-ArtoxGroup':
            try:
                is_link_used = ContestPerc.objects.get(uid=user_id, cid=cid, link=link)
                return JsonResponse({'error': 'Already used!'}, status=200)
            except ContestPerc.DoesNotExist:
                ContestPerc.objects.create(uid=user_id, percent=chance, cid=cid, link=link, is_done=False)
                return JsonResponse({'successfull': True}, status=200)
        else:
            return JsonResponse({'error': 'Invalid Token!'}, status=500)

class GetRefChance(View):
    def get(self, request):
        ref_percantage = Percentage.objects.get(name='Реф')
        ref_percantage = ref_percantage.percent

        # Формируем ответ
        data = {
            'result': ref_percantage
        }

        return JsonResponse(data, status=200)

class UserStatsView(View):
    def get(self, request):
        # Получаем текущую дату
        today = datetime.now().date()

        # Рассчитываем даты для проверки
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)

        # Считаем новые записи
        count_today = User.objects.filter(reg_date=today.strftime('%d/%m/%Y')).count()
        count_week = User.objects.filter(reg_date__lte=week_ago.strftime('%d/%m/%Y')).count()
        count_month = User.objects.filter(reg_date__lte=month_ago.strftime('%d/%m/%Y')).count()
        count_all_time = User.objects.count()

        # Считаем новые записи
        count_today_act = User.objects.filter(last_act=today.strftime('%d/%m/%Y')).count()
        count_week_act = User.objects.filter(last_act__lte=week_ago.strftime('%d/%m/%Y')).count()
        count_month_act = User.objects.filter(last_act__lte=month_ago.strftime('%d/%m/%Y')).count()

        # Формируем ответ
        data = {
            'new_today': count_today,
            'new_last_week': count_week,
            'new_last_month': count_month,
            'total_records': count_all_time,
            'act_today': count_today_act,
            'act_last_week': count_week_act,
            'act_last_month': count_month_act,
        }

        return JsonResponse(data, status=200)

class UserDataBase(View):
    def get(self, request):
        # Получаем параметры uid и username из запроса
        uid = request.GET.get('uid')
        username = request.GET.get('username')

        if uid is None or username is None:
            return JsonResponse({'error': 'uid и username необходимы'}, status=400)

        try:
            # Преобразуем uid в integer
            uid = int(uid)
            if not (-2**63 <= uid <= 2**63 - 1):
                return JsonResponse({'error': 'uid выходит за пределы допустимого диапазона'}, status=400)
        except ValueError:
            return JsonResponse({'error': 'uid должен быть числом'}, status=400)

        # Форматируем текущую дату в нужный формат dd/mm/yyyy
        today_date = datetime.now().strftime('%d/%m/%Y')

        # Пытаемся создать новый объект или обновить существующий
        try:
            user_profile, created = User.objects.update_or_create(
                uid=uid,
                defaults={
                    'username': username,
                    'reg_date': today_date,
                    'last_act': today_date  # обновляем last_act только для нового профиля
                }
            )
            if not created:
                # Если объект уже существует, обновляем только last_act
                user_profile.last_act = today_date
                user_profile.save()

            return JsonResponse({
                'uid': user_profile.uid,
                'username': user_profile.username,
                'reg_date': user_profile.reg_date,
                'last_act': user_profile.last_act
            }, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class CheckParticipation(View):
    def post(self, request):
        body = json.loads(request.body)  # Прочитайте JSON-тело запроса
        user_id = body.get('user_id')  # Извлеките User ID
        channel_id = body.get('channel_id')  # Извлеките Channel ID

        # Выполните запрос к API Telegram
        try:
            response = requests.get(
                f'https://api.telegram.org/bot{BOT_TOKEN}/getChatMember',
                params={'chat_id': channel_id, 'user_id': user_id}
            )
            response_data = response.json()

            if response_data['ok']:
                status = response_data['result']['status']
                # Проверка статуса участия
                if status in ['member', 'administrator', 'creator']:
                    return JsonResponse({'is_subscribed': True})
                else:
                    return JsonResponse({'is_subscribed': False})
            else:
                return JsonResponse({'error': response_data.get('description')}, status=500)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

def index(request):
    return HttpResponse('<h1>Index</h1>')

def contest(request):
    # user_id = request.GET.get('uid')
    # channels = request.GET.get('c')
    # nc = request.GET.get('nc')

    # try:
    #     if ',' in channels:
    #         channels = channels.split(',')
    #     else:
    #         channels = [channels]
    # except:
    #     return render(request, 'failure.html')

    # context = {
    #     "channels" : channels,
    #     "nc" : nc
    # }

    # return render(request, 'contest_check.html', context=context)
    return render(request, 'contest_check.html')

def success(request):
    cid = request.GET.get('nc')
    ads = request.GET.get('ads')
    uid = request.GET.get('uid')
    
    if '_321_' in ads:
        ads_list = ads.split('_321_')
    else:
        ads_list = [ads]

    ads_f_list = []
    for ad in ads_list:
        ad : str
        if '_999_' in ad:
            ad = ad.replace('_999_', '+')
        if 'c-' in ad:
            ads_f_list.append(['Подписаться на канал', f'https://t.me/{ad[2:]}'])
        else:
            ads_f_list.append(['Запустить бота', f'https://t.me/{ad[2:]}'])

    try:
        user_ads = get_list_or_404(ContestPerc.objects.filter(uid=uid, cid=cid, is_done=False))
        for user_ad in user_ads:
            try:
                ad_info = CheckingDatas.objects.get(link=user_ad.link)
            except Exception as e:
                continue
            if ad_info.ltype == 'B':
                code = ad_info.token
                response = requests.get(f"https://api.botstat.io/checksub/{code}/{uid}")
                if response.status_code == 200:
                    user_ad.is_done = True
                    user_ad.save()
                else:
                    continue
            elif ad_info.ltype == 'BT':
                b_token = ad_info.token

                # Подготовка URL для sendChatAction
                url = f"https://api.telegram.org/bot{b_token}/sendChatAction"

                # Параметры запроса
                params = {
                    "chat_id": uid,  # Идентификатор чата
                    "action": "typing"   # Или любой другой тип действия, который вы хотите отправить
                }

                # Выполнение запроса к Telegram Bot API
                response = requests.post(url, params=params)
                if response.status_code == 200:
                    user_ad.is_done = True 
                    user_ad.save()
                else:
                    continue
            elif ad_info.ltype == 'C':
                token = ad_info.token
                try:
                    response = requests.get(
                        f'https://api.telegram.org/bot{BOT_TOKEN}/getChatMember',
                        params={'chat_id': token, 'user_id': uid}
                    )
                    response_data = response.json()

                    if response_data['ok']:
                        status = response_data['result']['status']
                        # Проверка статуса участия
                        if status in ['member', 'administrator', 'creator']:
                            user_ad.is_done = True
                            user_ad.save() 
                        else:
                            continue
                    else:
                        continue

                except Exception as e:
                    continue
    except Exception as e:
        pass

    # Получаем шанс юзера и шансы за задание
    res_chance = 0.1
    try:
        user_chance = ContestPerc.objects.filter(uid=uid, cid=cid, is_done=True)
        for percantages in user_chance:
            res_chance += percantages.percent
    except ContestPerc.DoesNotExist:
        res_chance = 0.1
    ref_chance = Percentage.objects.get(name='Реф').percent
    bot_chance = Percentage.objects.get(name='Бот').percent
    channel_chance = Percentage.objects.get(name='Канал').percent

    context = {
        'nc' : cid,
        'uid' : uid,
        'ads' : ads_f_list,
        'rc' : ref_chance,
        'bc' : bot_chance,
        'cc' : channel_chance,
        'uc' : res_chance
    }
    return render(request, 'success_test.html', context=context)

def failure(request):
    return render(request, 'failure.html')