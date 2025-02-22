class User:
    def __init__(self, tel_id, name, email, context, is_blocked, is_admin, last_data):
        self.tel_id = tel_id
        self.name = name
        self.email = email
        self.context = context
        self.is_blocked = is_blocked
        self.is_admin = is_admin
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
