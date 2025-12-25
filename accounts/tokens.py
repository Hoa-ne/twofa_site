from django.contrib.auth.tokens import PasswordResetTokenGenerator

# Lop tao token xac thuc email tuy chinh, ke thua tu co che cua Django
class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    
    # Ham tao chuoi hash bi mat dua tren ID, thoi gian va trang thai xac thuc
    def _make_hash_value(self, user, timestamp):
        # Token se thay doi neu trang thai email_verified thay doi (tranh dung lai token cu)
        return f"{user.pk}{timestamp}{user.email_verified}"

email_verification_token = EmailVerificationTokenGenerator()