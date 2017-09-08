from django.contrib import admin
from .models import Album,Song
from django.contrib.auth.models import User


admin.site.register(Album)
admin.site.register(Song)




user = User.objects.get(id=1)
print(user.check_password('password'))