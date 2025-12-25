from django.apps import AppConfig

# Cau hinh thiet lap cho ung dung accounts trong du an
class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"