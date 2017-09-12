from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib import auth

class User(auth.models.User,auth.models.PermissionsMixin):
    def __str__(self):
        return "@{}".format(self.username)

# Create your models here.
class Chapter(models.Model):
    class Meta:
        permissions = (("can_create_chapter","Can create chapter"),)

    chapter_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.chapter_name

    def get_absolute_url(self):
        return reverse("chapters_list")

class Theme(models.Model):
    class Meta:
        permissions = (("can_create_theme","Can create theme"),)

    theme_name = models.CharField(max_length=100, unique=True)
    parent_chapter = models.ForeignKey(Chapter, related_name = 'child_themes')

    def __str__(self):
        return self.theme_name

    def get_absolute_url(self):
        return reverse("chapter_detail",kwargs={'chapter':self.parent_chapter})

class English_Entry(models.Model):
    class Meta:
        permissions = (("can_create_entry","Can create entry"),
                ("can_edit_entry","Can edit entry"),)

    english_word = models.CharField(max_length=100, unique=True)
    parent_theme = models.ManyToManyField(Theme, related_name = 'child_entries')
    english_related = models.ManyToManyField('self', null=True, blank=True, related_name = 'english_main')

    def __str__(self):
        return self.english_word

    def get_absolute_url(self):
        return reverse("entry_detail",kwargs={'pk':self.pk})


class English_Alternative(models.Model):
    english_synonym = models.CharField(max_length=100, null=False, blank=False)
    english_original = models.ForeignKey(English_Entry, on_delete=models.CASCADE, related_name = 'english_alternatives')

    def __str__(self):
        return self.english_synonym

class Spanish_Entry(models.Model):
    english_entry = models.OneToOneField(English_Entry, on_delete=models.CASCADE, related_name = 'child_spanish')
    spanish_word = models.CharField(max_length=100, unique=True, null=False, blank=False)
    spanish_definition = models.TextField(max_length=1000, null=True, blank=True)
    spanish_included = models.ManyToManyField('self', symmetrical=False, null=True, blank=True, related_name = 'spanish_main')

    def __str__(self):
        return self.spanish_word

    def get_alternatives(self):
        alternatives = Spanish_Alternative.objects.filter(spanish_original = self)
        return alternatives

class Spanish_Alternative(models.Model):
    spanish_synonym = models.CharField(max_length=100, null=False, blank=False)
    spanish_original = models.ForeignKey(Spanish_Entry, on_delete=models.CASCADE, related_name = 'spanish_alternatives')

    def __str__(self):
        return self.spanish_synonym

class Comment(models.Model):
    class Meta:
        permissions = (("can_write_comment","Can write comment"),)

    english_entry = models.ForeignKey(English_Entry, on_delete=models.CASCADE, related_name = 'comments')
    author = models.CharField(max_length=100, default = 'engtranslator')
    text = models.TextField(max_length=500, null=False, blank=False)
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=True)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse("entry_detail",kwargs={'pk':self.english_entry.pk})

    def approve(self):
        self.approved_comment = True
        self.save()
