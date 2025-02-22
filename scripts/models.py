class User:
    def __init__(self, tel_id, name, email, context, is_blocked, is_admin, create_date, module_start_date,
                 current_module, current_lesson, last_data):
        self.tel_id = tel_id
        self.name = name
        self.email = email
        self.context = context
        self.is_blocked = is_blocked
        self.is_admin = is_admin
        self.create_date = create_date
        self.module_start_date = module_start_date
        self.current_module = current_module
        self.current_lesson = current_lesson
        self.last_data = last_data


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
