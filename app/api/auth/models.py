from mongoengine import Document, StringField, EmailField, ListField, DateTimeField, BooleanField
import datetime
import bcrypt
from app.utils.jwt_utils import generate_access_token, generate_refresh_token


class User(Document):
    username = StringField(required=True, unique=True)
    email = EmailField(required=True, unique=True)
    password_hash = StringField(required=True)
    roles = ListField(StringField(), default=["user"])
    created_at = DateTimeField(default=datetime.datetime.now(datetime.timezone.utc))  # Corrected
    is_active = BooleanField(default=True)  # Changed from StringField to BooleanField

    def set_password(self, password):
        """Hash the password before saving it."""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')  # Ensure the hash is stored as a string

    def check_password(self, password):
        """Check a hashed password against a plain password."""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def generate_tokens(self):
        """Generate access and refresh tokens for the user."""
        access_token = generate_access_token(self.email, self.roles)
        refresh_token = generate_refresh_token(self.email)
        return access_token, refresh_token
