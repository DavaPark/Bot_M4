from django.db import models
STATUSES = (('0', '🟢 Активный'), ('1', 'Архив'), ('2', '🔴 Заблокированный'))

USER_TYPE = (('superadmin', 'Суперадминистратор'),
             ('admin', 'Администратор'))


class User(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='ID записи')
    tel_id = models.BigIntegerField(unique=True, verbose_name='Telegram ID пользователя')
    name = models.CharField(max_length=255, verbose_name='Имя')
    email = models.EmailField(unique=True, verbose_name='Email')
    context = models.TextField(blank=False, verbose_name='Контекст')
    is_blocked = models.BooleanField(default=False, choices=STATUSES, verbose_name='Статус')
    is_admin = models.BooleanField(default=False, choices=USER_TYPE, verbose_name='Тип пользователя')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    module_start_date = models.DateTimeField(null=True, blank=True, verbose_name='Начало прохождения модуля')
    current_module = models.IntegerField(default=1, verbose_name='Номер модуля')
    current_lesson = models.IntegerField(default=1, verbose_name='Номер урока')
    last_date = models.DateTimeField(auto_now=True, verbose_name='Прохождение последнего урока')

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'
        db_table = 'users'
        managed = False


class Archive(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='ID записи')
    tel_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Telegram ID пользователя')
    name = models.ForeignKey(User, on_delete=models.CASCADE, max_length=255, verbose_name='Имя')
    email = models.ForeignKey(User, on_delete=models.CASCADE, unique=True, verbose_name='Емеил')
    context = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, verbose_name='Контекст')
    is_blocked = models.ForeignKey(User, on_delete=models.CASCADE, default=False, choices=STATUSES,
                                   verbose_name='Статус')
    is_admin = models.ForeignKey(User, on_delete=models.CASCADE, default=False, choices=USER_TYPE,
                                 verbose_name='Тип пользователя')
    create_date = models.ForeignKey(User, on_delete=models.CASCADE, auto_now_add=True, verbose_name='Дата создания')
    last_date = models.CharField(auto_now=True, verbose_name='Дата добавления в архив')

    class Meta:
        verbose_name = 'Архив'
        verbose_name_plural = 'Архив'
        db_table = 'archive'
        managed = False


class Deleted(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='ID записи')
    tel_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Telegram ID пользователя')
    name = models.ForeignKey(User, on_delete=models.CASCADE, max_length=255, verbose_name='Имя')
    email = models.ForeignKey(User, on_delete=models.CASCADE, unique=True, verbose_name='Емеил')
    context = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, verbose_name='Контекст')
    is_blocked = models.ForeignKey(User, on_delete=models.CASCADE, default=False, choices=STATUSES,
                                   verbose_name='Статус')
    is_admin = models.ForeignKey(User, on_delete=models.CASCADE, default=False, choices=USER_TYPE,
                                 verbose_name='Тип пользователя')
    create_date = models.ForeignKey(User, on_delete=models.CASCADE, auto_now_add=True, verbose_name='Дата создания')
    last_date = models.CharField(auto_now=True, verbose_name='Дата добавления в заблокированные')

    class Meta:
        verbose_name = 'Заблокированные'
        verbose_name_plural = 'Заблокированные'
        db_table = 'deleted'
        managed = False


class Module(models.Model):
    id = models.IntegerField(primary_key=True, blank=False, verbose_name='ID записи')
    module_id = models.IntegerField(blank=False, verbose_name='Номер модуля')
    title = models.CharField(max_length=100, blank=False, verbose_name='Название модуля')

    class Meta:
        verbose_name = 'Модули'
        verbose_name_plural = 'Модули'
        db_table = 'module'
        managed = False


class Lessons(models.Model):
    id = models.IntegerField(primary_key=True, blank=False, verbose_name='ID записи')
    lesson_id = models.IntegerField(blank=False, verbose_name='Номер урока')
    module_id = models.ForeignKey(Module, on_delete=models.CASCADE, blank=False, verbose_name='Номер модуля')
    title = models.CharField(max_length=100, blank=False, verbose_name='Название урока')
    video = models.CharField(max_length=1000, blank=False, verbose_name='Ссылка на видео')
    test_link = models.CharField(max_length=1000, blank=False, verbose_name='Ссылка на тест')
    pass_score = models.IntegerField(blank=False, verbose_name='Минимальная оценка за тест')

    class Meta:
        verbose_name = 'Уроки'
        verbose_name_plural = 'Уроки'
        db_table = 'lessons'
        managed = False


class UserProgress(models.Model):
    id = models.IntegerField(primary_key=True, blank=False, verbose_name='ID записи')
    tel_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Telegram ID пользователя')
    name = models.ForeignKey(User, on_delete=models.CASCADE, max_length=255, verbose_name='Имя')
    email = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Емеил')
    module_id = models.ForeignKey(Module, on_delete=models.CASCADE, blank=False, verbose_name='Номер модуля')
    lesson_id = models.ForeignKey(Lessons, on_delete=models.CASCADE, blank=False, verbose_name='Номер урока')
    test_score = models.IntegerField(blank=False, verbose_name='Оценка за предыдущий тест')
    completed_at = models.CharField(blank=False, verbose_name='Дата когда перещёл на новый урок')

    class Meta:
        verbose_name = 'Прогресс пользователя'
        verbose_name_plural = 'Прогресс пользователя'
        db_table = 'user_progress'
        managed = False


class Payment(models.Model):
    id = models.IntegerField(primary_key=True, blank=False, verbose_name='ID записи')
    tel_id = models.BigIntegerField(blank=False, verbose_name='Telegram ID плательщика')
    sum = models.IntegerField(blank=False, verbose_name='Сумма')
    date = models.CharField(max_length=100, blank=False, verbose_name='Дата оплаты')
    status = models.CharField(max_length=100, blank=False, verbose_name='Статус')

    class Meta:
        verbose_name = 'Платежи'
        verbose_name_plural = 'Платежи'
        db_table = 'payment'
        managed = False

