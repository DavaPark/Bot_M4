class User:
    def __init__(self, tel_id, name, email, context, is_blocked, is_admin, create_date, module_start_date,
                 current_module, current_lesson, last_date, phone, region, denomination, role, username, open_module):
        self.tel_id = tel_id
        self.name = name
        self.email = email
        self.context = context
        self.is_blocked = is_blocked
        self.is_admin = is_admin
        self.create_date = create_date
        self.module_start_date = module_start_date
        self.current_lesson = current_lesson
        self.last_date = last_date
        self.current_module = current_module
        self.phone = phone
        self.region = region
        self.denomination = denomination
        self.role = role
        self.username = username
        self.open_module = open_module


class Archive:
    def __init__(self, tel_id, name, email, context, is_blocked, is_admin, last_data):
        self.tel_id = tel_id
        self.name = name
        self.email = email
        self.context = context
        self.is_blocked = is_blocked
        self.is_admin = is_admin
        self.last_data = last_data


class Deleted:
    def __init__(self, tel_id, name, email, context, is_blocked, is_admin, last_data):
        self.tel_id = tel_id
        self.name = name
        self.email = email
        self.context = context
        self.is_blocked = is_blocked
        self.is_admin = is_admin
        self.last_data = last_data


class Module:
    def __init__(self, module_id, title):
        self.module_id = module_id
        self.title = title


class Lessons:
    def __init__(self, lesson_id, module_id, title, video, test_link, pass_score):
        self.lesson_id = lesson_id
        self.module_id = module_id
        self.title = title
        self.video = video.split(',')
        self.test_link = test_link.split(',')
        self.pass_score = pass_score


class UserProgress:
    def __init__(self, id, tel_id, name, email, select_module, select_lesson, test_score, completed_at, progress):
        self.id = id
        self.tel_id = tel_id
        self.name = name
        self.email = email
        self.select_module = select_module
        self.select_lesson = select_lesson
        self.test_score = test_score
        self.completed_at = completed_at
        self.progress = progress
