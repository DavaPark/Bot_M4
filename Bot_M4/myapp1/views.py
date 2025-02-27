import json
import traceback
from datetime import datetime

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse

from .models import Payment


@csrf_exempt
def payment_callback(request):
	if request.method != "POST":
		return JsonResponse({"status": "error", "message": "Invalid request method"}, status=200)

	try:
		data = json.loads(request.body)
	except json.JSONDecodeError:
		return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=200)

	# Проверяем наличие обязательных полей: orderReference и products (и что products не пустой)
	if "orderReference" not in data or "products" not in data or not data["products"]:
		return JsonResponse({"status": "error", "message": "Missing required fields"}, status=200)

	try:
		# Преобразуем timestamp в datetime
		created_timestamp = data.get("createdDate")
		processing_timestamp = data.get("processingDate")
		created_date = datetime.fromtimestamp(created_timestamp) if created_timestamp else None
		processing_date = datetime.fromtimestamp(processing_timestamp) if processing_timestamp else None

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
	except Exception as e:
		return JsonResponse({"status": "error", "message": "Invalid JSON or missing fields"}, status=200)

	payment = Payment.update_or_create_from_request(mapped_data)
	if payment:
		return JsonResponse(
			{"status": "success", "message": "Payment updated", "order_reference": payment.order_reference})
	else:
		return JsonResponse({"status": "error", "message": "Missing order_reference"}, status=200)
