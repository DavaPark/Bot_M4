from django.db import models
STATUSES = (('0', '🟢 Активный'), ('1', 'Архив'), ('2', '🔴 Заблокированный'))

USER_TYPE = (('superadmin', 'Суперадминистратор'),
             ('admin', 'Администратор'))


class Payment(models.Model):
    merchant_account = models.CharField(max_length=255, verbose_name="Мерчант акаунт")
    order_reference = models.CharField(max_length=255, unique=True, verbose_name="Номер замовлення")
    merchant_signature = models.CharField(max_length=255, verbose_name="Підпис мерчанта")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сума")
    currency = models.CharField(max_length=10, verbose_name="Валюта")
    auth_code = models.CharField(max_length=255, blank=True, null=True, verbose_name="Код авторизації")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    created_date = models.DateTimeField(verbose_name="Дата створення")
    processing_date = models.DateTimeField(verbose_name="Дата обробки")
    card_pan = models.CharField(max_length=20, verbose_name="PAN картки")
    card_type = models.CharField(max_length=50, verbose_name="Тип картки")
    issuer_bank_country = models.CharField(max_length=100, verbose_name="Країна банку-емітента")
    issuer_bank_name = models.CharField(max_length=255, verbose_name="Назва банку-емітента")
    rec_token = models.CharField(max_length=255, blank=True, null=True, verbose_name="Токен рекурентного платежу")
    transaction_status = models.CharField(max_length=50, verbose_name="Статус транзакції")
    reason = models.CharField(max_length=255, verbose_name="Причина відмови")
    reason_code = models.IntegerField(verbose_name="Код причини відмови")
    fee = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Комісія")
    payment_system = models.CharField(max_length=50, verbose_name="Платіжна система")
    acquirer_bank_name = models.CharField(max_length=255, verbose_name="Банк-еквайєр")
    card_product = models.CharField(max_length=50, verbose_name="Продукт картки")
    client_name = models.CharField(max_length=255, verbose_name="Ім'я клієнта")
    repay_url = models.URLField(verbose_name="URL повторного платежу")
    rrn = models.CharField(max_length=255, blank=True, null=True, verbose_name="RRN")
    terminal = models.CharField(max_length=255, verbose_name="Термінал")
    acquirer = models.CharField(max_length=255, verbose_name="Еквайєр")
    product_name = models.CharField(max_length=255, verbose_name="Назва товару")
    product_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна товару")
    product_count = models.IntegerField(verbose_name="Кількість товару")

    def __str__(self):
        return f"Payment {self.order_reference} - {self.transaction_status}"

    @classmethod
    def update_or_create_from_request(cls, data):
        order_reference = data.get("order_reference")
        if not order_reference:
            return None

        obj, created = cls.objects.update_or_create(
            order_reference=order_reference,
            defaults={
                "merchant_account": data.get("merchant_account", ""),
                "merchant_signature": data.get("merchant_signature", ""),
                "amount": data.get("amount", 0),
                "currency": data.get("currency", ""),
                "auth_code": data.get("auth_code"),
                "email": data.get("email", ""),
                "phone": data.get("phone", ""),
                "created_date": data.get("created_date"),
                "processing_date": data.get("processing_date"),
                "card_pan": data.get("card_pan", ""),
                "card_type": data.get("card_type", ""),
                "issuer_bank_country": data.get("issuer_bank_country", ""),
                "issuer_bank_name": data.get("issuer_bank_name", ""),
                "rec_token": data.get("rec_token"),
                "transaction_status": data.get("transaction_status", ""),
                "reason": data.get("reason", ""),
                "reason_code": data.get("reason_code", 0),
                "fee": data.get("fee", 0),
                "payment_system": data.get("payment_system", ""),
                "acquirer_bank_name": data.get("acquirer_bank_name", ""),
                "card_product": data.get("card_product", ""),
                "client_name": data.get("client_name", ""),
                "repay_url": data.get("repay_url", ""),
                "rrn": data.get("rrn"),
                "terminal": data.get("terminal", ""),
                "acquirer": data.get("acquirer", ""),
                "product_name": data.get("product_name", ""),
                "product_price": data.get("product_price", 0),
                "product_count": data.get("product_count", 0),
            }
        )
        return obj



# class User(models.Model):
#     id = models.IntegerField(primary_key=True, verbose_name='ID записи')
#     tel_id = models.BigIntegerField(unique=True, verbose_name='Telegram ID пользователя')
#     name = models.CharField(max_length=255, verbose_name='Имя')
#     email = models.EmailField(unique=True, verbose_name='Email')
#     context = models.TextField(blank=False, verbose_name='Контекст')
#     is_blocked = models.BooleanField(default=False, choices=STATUSES, verbose_name='Статус')
#     is_admin = models.BooleanField(default=False, choices=USER_TYPE, verbose_name='Тип пользователя')
#     create_date = models.DateTimeField(verbose_name='Дата создания')
#     module_start_date = models.DateTimeField(null=True, blank=True, verbose_name='Начало прохождения модуля')
#     current_module = models.IntegerField(default=1, verbose_name='Номер модуля')
#     current_lesson = models.IntegerField(default=1, verbose_name='Номер урока')
#     last_date = models.DateTimeField(verbose_name='Прохождение последнего урока')
#
#     class Meta:
#         verbose_name = 'Пользователи'
#         verbose_name_plural = 'Пользователи'
#         db_table = 'users'
#         managed = False
#
#
# class Archive(models.Model):
#     id = models.IntegerField(primary_key=True, verbose_name='ID записи')
#     tel_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Telegram ID пользователя')
#     name = models.ForeignKey(User, on_delete=models.CASCADE, max_length=255, verbose_name='Имя')
#     email = models.ForeignKey(User, on_delete=models.CASCADE, unique=True, verbose_name='Емеил')
#     context = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, verbose_name='Контекст')
#     is_blocked = models.ForeignKey(User, on_delete=models.CASCADE, default=False, choices=STATUSES,
#                                    verbose_name='Статус')
#     is_admin = models.ForeignKey(User, on_delete=models.CASCADE, default=False, choices=USER_TYPE,
#                                  verbose_name='Тип пользователя')
#     create_date = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Дата создания')
#     last_date = models.CharField(verbose_name='Дата добавления в архив')
#
#     class Meta:
#         verbose_name = 'Архив'
#         verbose_name_plural = 'Архив'
#         db_table = 'archive'
#         managed = False
#
#
# class Deleted(models.Model):
#     id = models.IntegerField(primary_key=True, verbose_name='ID записи')
#     tel_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Telegram ID пользователя')
#     name = models.ForeignKey(User, on_delete=models.CASCADE, max_length=255, verbose_name='Имя')
#     email = models.ForeignKey(User, on_delete=models.CASCADE, unique=True, verbose_name='Емеил')
#     context = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, verbose_name='Контекст')
#     is_blocked = models.ForeignKey(User, on_delete=models.CASCADE, default=False, choices=STATUSES,
#                                    verbose_name='Статус')
#     is_admin = models.ForeignKey(User, on_delete=models.CASCADE, default=False, choices=USER_TYPE,
#                                  verbose_name='Тип пользователя')
#     create_date = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Дата создания')
#     last_date = models.CharField(verbose_name='Дата добавления в заблокированные')
#
#     class Meta:
#         verbose_name = 'Заблокированные'
#         verbose_name_plural = 'Заблокированные'
#         db_table = 'deleted'
#         managed = False
#
#
# class Module(models.Model):
#     id = models.IntegerField(primary_key=True, blank=False, verbose_name='ID записи')
#     module_id = models.IntegerField(blank=False, verbose_name='Номер модуля')
#     title = models.CharField(max_length=100, blank=False, verbose_name='Название модуля')
#
#     class Meta:
#         verbose_name = 'Модули'
#         verbose_name_plural = 'Модули'
#         db_table = 'module'
#         managed = False
#
#
# class Lessons(models.Model):
#     id = models.IntegerField(primary_key=True, blank=False, verbose_name='ID записи')
#     lesson_id = models.IntegerField(blank=False, verbose_name='Номер урока')
#     module_id = models.ForeignKey(Module, on_delete=models.CASCADE, blank=False, verbose_name='Номер модуля')
#     title = models.CharField(max_length=100, blank=False, verbose_name='Название урока')
#     video = models.CharField(max_length=1000, blank=False, verbose_name='Ссылка на видео')
#     test_link = models.CharField(max_length=1000, blank=False, verbose_name='Ссылка на тест')
#     pass_score = models.IntegerField(blank=False, verbose_name='Минимальная оценка за тест')
#
#     class Meta:
#         verbose_name = 'Уроки'
#         verbose_name_plural = 'Уроки'
#         db_table = 'lessons'
#         managed = False
#
#
# class UserProgress(models.Model):
#     id = models.IntegerField(primary_key=True, blank=False, verbose_name='ID записи')
#     tel_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Telegram ID пользователя')
#     name = models.ForeignKey(User, on_delete=models.CASCADE, max_length=255, verbose_name='Имя')
#     email = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Емеил')
#     module_id = models.ForeignKey(Module, on_delete=models.CASCADE, blank=False, verbose_name='Номер модуля')
#     lesson_id = models.ForeignKey(Lessons, on_delete=models.CASCADE, blank=False, verbose_name='Номер урока')
#     test_score = models.IntegerField(blank=False, verbose_name='Оценка за предыдущий тест')
#     completed_at = models.CharField(blank=False, verbose_name='Дата когда перещёл на новый урок')
#
#     class Meta:
#         verbose_name = 'Прогресс пользователя'
#         verbose_name_plural = 'Прогресс пользователя'
#         db_table = 'user_progress'
#         managed = False
#
#
# class Payment(models.Model):
#     id = models.IntegerField(primary_key=True, blank=False, verbose_name='ID записи')
#     tel_id = models.BigIntegerField(blank=False, verbose_name='Telegram ID плательщика')
#     sum = models.IntegerField(blank=False, verbose_name='Сумма')
#     date = models.CharField(max_length=100, blank=False, verbose_name='Дата оплаты')
#     status = models.CharField(max_length=100, blank=False, verbose_name='Статус')
#
#     class Meta:
#         verbose_name = 'Платежи'
#         verbose_name_plural = 'Платежи'
#         db_table = 'payment'
#         managed = False
#
