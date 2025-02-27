import asyncio
import json
import traceback
from datetime import datetime

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from django.views.decorators.csrf import csrf_exempt
from django.http import  JsonResponse
from django.utils.dateparse import parse_datetime


from .models import *
from .way4pay import WayForPay


@csrf_exempt
def payment_callback(request):
	if request.method != "POST":
		return JsonResponse({"status": "error", "message": "Invalid request method"}, status=200)

	try:
		data = json.loads(request.body)
		print(data)
	except json.JSONDecodeError:
		return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=200)

	# Проверяем наличие обязательных полей: orderReference и products (и что products не пустой)
	if "orderReference" not in data or "products" not in data or not data["products"]:
		return JsonResponse({"status": "error", "message": "Missing required fields"}, status=200)

	try:
		created_timestamp = data.get("createdDate")
		processing_timestamp = data.get("processingDate")
		created_date = datetime.fromtimestamp(created_timestamp) if created_timestamp else None
		processing_date = datetime.fromtimestamp(processing_timestamp) if processing_timestamp else None

		if data["transactionStatus"] == 'Approved':
			pm = Payment.objects.filter(orderReference=data["orderReference"]).first()
			if pm is None:
				mapped_data = {
					"merchant_account": data.get("merchantAccount", ""),
					"order_reference": data.get("orderReference", ""),
					"merchant_signature": data.get("merchantSignature", ""),
					"amount": data.get("amount", 0),
					"currency": data.get("currency", ""),
					"auth_code": data.get("authCode", ""),
					"email": data.get("email", ""),
					"phone": data.get("phone", ""),
					"created_date": created_date,
					"processing_date": processing_date,
					"card_pan": data.get("cardPan", ""),
					"card_type": data.get("cardType", ""),
					"issuer_bank_country": data.get("issuerBankCountry", ""),
					"issuer_bank_name": data.get("issuerBankName", ""),
					"rec_token": data.get("recToken", ""),
					"transaction_status": data.get("transactionStatus", ""),
					"reason": data.get("reason", ""),
					"reason_code": data.get("reasonCode", 0),
					"fee": data.get("fee", 0),
					"payment_system": data.get("paymentSystem", ""),
					"acquirer_bank_name": data.get("acquirerBankName", ""),
					"card_product": data.get("cardProduct", ""),
					"client_name": data.get("clientName", ""),
					"rrn": data.get("rrn", ""),
					"terminal": data.get("terminal", ""),
					"acquirer": data.get("acquirer", ""),
					"product_name": data["products"][0].get("name", ""),
					"product_price": data["products"][0].get("price", 0),
					"product_count": data["products"][0].get("count", 0),
				}
				payment = Payment.update_or_create_from_request(mapped_data)
				if payment:
					bot = Bot("7581915348:AAHUlNsTShmtD6tzRpVX_1dJwTz9RF4rC64",
					          default=DefaultBotProperties(parse_mode="HTML"))
					video_id = 'BAACAgIAAxkBAAPFZ8Bu8ajHtoaignWxQ97udddTYCwAAq5hAAJXDAhKFdXY_cFCbyE2BA'
					menu_buttons_keyboard = ReplyKeyboardMarkup(
						keyboard=[
							[KeyboardButton(text="Навчання 📚"), KeyboardButton(text="Стань частиною М4")],
							[KeyboardButton(text="Спільнота"), KeyboardButton(text="Питання-відповіді")],
							[KeyboardButton(text="Корисне"), KeyboardButton(text="Підтримка")],
						],
						resize_keyboard=True
					)
					asyncio.run(bot.send_video(int(data["orderReference"].split("-")[1]), video_id,
					                           reply_markup=menu_buttons_keyboard))
					return JsonResponse(
						{"status": "success", "message": "Payment updated", "order_reference": payment.order_reference})
			else:
				return JsonResponse({"status": "error", "message": "Missing order_reference"}, status=200)
		else:
			products = data.get("products", [{}])[0]
			created_timestamp = data.get("createdDate")
			processing_timestamp = data.get("processingDate")
			created_date = datetime.fromtimestamp(created_timestamp) if created_timestamp else None
			processing_date = datetime.fromtimestamp(processing_timestamp) if processing_timestamp else None

			payment = Payment.objects.create(
				merchant_account=data.get("merchantAccount"),
				order_reference=data.get("orderReference"),
				merchant_signature=data.get("merchantSignature"),
				amount=data.get("amount"),
				currency=data.get("currency"),
				auth_code=data.get("authCode", None),
				email=data.get("email"),
				phone=data.get("phone"),
				created_date=created_date,
				processing_date=processing_date,
				card_pan=data.get("cardPan", None),
				card_type=data.get("cardType", None),
				issuer_bank_country=data.get("issuerBankCountry", None),
				issuer_bank_name=data.get("issuerBankName", None),
				rec_token=data.get("recToken", None),
				transaction_status=data.get("transactionStatus"),
				reason=data.get("reason", None),
				reason_code=data.get("reasonCode", None),
				fee=data.get("fee", None),
				payment_system=data.get("paymentSystem", None),
				acquirer_bank_name=data.get("acquirerBankName", None),
				card_product=data.get("cardProduct", None),
				client_name=data.get("clientName", None),
				repay_url=data.get("repayUrl", None),
				rrn=data.get("rrn", None),
				terminal=data.get("terminal", None),
				acquirer=data.get("acquirer", None),
				product_name=products.get("name", None),
				product_price=products.get("price", None),
				product_count=products.get("count", None)
			)
			payment.save()
			bot = Bot("7581915348:AAHUlNsTShmtD6tzRpVX_1dJwTz9RF4rC64",
			          default=DefaultBotProperties(parse_mode="HTML"))
			text = """⚠️ <b>Оплата не пройшла</b>


Схоже, сталася помилка під час оплати. Не хвилюйся – спробуй ще раз)


📌 Що робити? 

1️⃣ Переконайся, що на картці достатньо коштів та вона підтримує онлайн-платежі. 
2️⃣ Спробуй ще раз натиснути "Оплатити" та повторити платіж. 
3️⃣ Якщо проблема залишається – натисни "Підтримка" і ми допоможемо.


💡 <b>Ти вже так близько! Заверши оплату та отримай доступ до навчання.</b>
"""
			W4P_KEY = 'flk3409refn54t54t*FNJRET'
			MERCHANT_ACCOUNT = 'test_merch_n1'
			DOMAIN_NAME = 'https://m4ready.org/ukraine/'
			wfp = WayForPay(key=W4P_KEY, domain_name=DOMAIN_NAME)
			res = wfp.create_invoice(
				merchantAccount=MERCHANT_ACCOUNT,
				merchantAuthType='SimpleSignature',
				amount='500',
				currency='UAH',
				productNames=["Оплата за курс M4"],
				productPrices=[500],
				productCounts=[1],
				orderID=f'M4-{data["orderReference"].split("-")[1]}-{int(data["orderReference"].split("-")[2])+1}'
			)
			link = res.invoiceUrl
			print(res.json())
			ik = InlineKeyboardMarkup(inline_keyboard=[
				[InlineKeyboardButton(text='💳 Оплатити', url=link)]
			])
			asyncio.run(bot.send_message(int(data["orderReference"].split("-")[1]), text, parse_mode='html',
			                             reply_markup=ik))
	except Exception as e:
		print(traceback.format_exc())
		return JsonResponse({"status": "error", "message": "Invalid JSON or missing fields"}, status=200)

	return JsonResponse(
		{"status": "success", "message": "Payment updated", "order_reference": payment.order_reference},
		status=200)



@csrf_exempt
def registrationForm(request):
	data = json.loads(request.body)

	user = User.objects.filter(email=data["email"]).first()
	if user is None:
		user = User.objects.filter(username=str(data["Ваш нікнейм у Телеграм (наприклад @PProtopopov)"]).replace("@", '')).first()
	if user is not None:
		user.phone = data["Ваш номер телефону (до якого прив'язаний Телеграм)"]
		user.role = data['Оберіть основну вашу роль у служінні зараз?  ']
		user.denomination = data['До якої деномінації належить ваша церква? \n\n(За потреби вкажіть іншу деномінацію знизу)']
		user.region = data['В якій області ви зараз служите?  ']
		user.save()
	return JsonResponse({"status": "success"})


# {'merchantAccount': 'test_merch_n1', 'orderReference': 'M4-420404892-0', 'merchantSignature': '742415d0a1bc04ad29e14bf330d81e27', 'amount': 1, 'currency': 'UAH', 'authCode': '', 'email': 'adlkjhcnakajdbf@gmail.com', 'phone': '380998765432', 'createdDate': 1740684838, 'processingDate': 1740684933, 'cardPan': '54****5454', 'cardType': 'MasterCard', 'issuerBankCountry': None, 'issuerBankName': None, 'recToken': '', 'transactionStatus': 'Declined', 'reason': 'Fraud transaction', 'reasonCode': 1114, 'fee': 0, 'paymentSystem': 'card', 'acquirerBankName': 'WayForPay', 'cardProduct': '', 'clientName': 'ANDRII GONCHAROV', 'products': [{'name': 'Оплата за курс M4', 'price': 1, 'count': 1}], 'rrn': '', 'terminal': '', 'acquirer': ''}