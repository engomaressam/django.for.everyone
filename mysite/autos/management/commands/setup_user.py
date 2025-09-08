from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Setup dj4e_user with staff privileges'

    def handle(self, *args, **options):
        User = get_user_model()
        username = 'dj4e_user'
        password = 'Meow_96a4a4_42'
        
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': 'dj4e_user@example.com',
                'is_staff': True,
                'is_active': True,
            }
        )
        
        if not created:
            user.is_staff = True
            user.is_active = True
            user.save()
            
        user.set_password(password)
        user.save()
        
        self.stdout.write(
            self.style.SUCCESS(f'User {username} setup successfully with staff privileges')
        )
