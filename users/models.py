from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator, MaxValueValidator

# Custom manager for user creation
class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('Phone number is required')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone_number, password, **extra_fields)

# Upload paths
def student_id_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    new_name = f"student_id_{instance.phone_number}.{ext}"
    return f'student_id_photos/{instance.phone_number}/{new_name}'

def profile_picture_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    new_name = f"profile_{instance.phone_number}.{ext}"
    return f'profile_pictures/{instance.phone_number}/{new_name}'

# Custom user model
class User(AbstractUser):
    username = None  # Removing default username field

    phone_number = models.CharField(
        max_length=15,
        unique=True,
        primary_key=True,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', message="Enter a valid phone number.")]
    )
    name = models.CharField(max_length=100, default='', blank=True)
    email = models.EmailField(blank=True)
    student_id = models.CharField(max_length=20, unique=True)
    profile_picture = models.ImageField(upload_to=profile_picture_upload_path, blank=True)
    student_id_picture = models.ImageField(upload_to=student_id_upload_path)
    seller_rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[MinValueValidator(1.0), MaxValueValidator(5.0)],
        default=5.0,
        help_text="Seller rating between 1 and 5"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['student_id']

    objects = UserManager()

    def __str__(self):
        return self.phone_number
