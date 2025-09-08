from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from autos.models import Make, Auto

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

        # Ensure needed permissions on Make and Auto
        make_ct = ContentType.objects.get_for_model(Make)
        auto_ct = ContentType.objects.get_for_model(Auto)
        needed_codenames = [
            'view_make','add_make','change_make',
            'view_auto','add_auto','change_auto'
        ]
        perms = list(Permission.objects.filter(
            content_type__in=[make_ct, auto_ct],
            codename__in=needed_codenames
        ))
        user.user_permissions.add(*perms)
        user.save()
        
        self.stdout.write(
            self.style.SUCCESS(f'User {username} setup successfully with staff privileges')
        )
