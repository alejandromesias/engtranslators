from django.contrib import admin
from glosario.models import (
 Chapter,
 Theme,
 English_Entry,
 English_Alternative,
 Spanish_Entry,
 Spanish_Alternative,
 Comment,
 Favorite,
)
# Register your models here.

admin.site.register(Chapter)
admin.site.register(Theme)
admin.site.register(English_Entry)
admin.site.register(English_Alternative)
admin.site.register(Spanish_Entry)
admin.site.register(Spanish_Alternative)
admin.site.register(Comment)
admin.site.register(Favorite)
