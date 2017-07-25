from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse

# Create your models here.
class Chapter(models.Model):
    chapter_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.chapter_name

class Theme(models.Model):
    theme_name = models.CharField(max_length=100, unique=True)
    parent_chapter = models.ForeignKey(Chapter, related_name = 'child_themes')

    def __str__(self):
        return self.theme_name

class English_Entry(models.Model):
    english_word = models.CharField(max_length=100, unique=True)
    parent_theme = models.ManyToManyField(Theme, related_name = 'child_entries')
    english_related = models.ManyToManyField('self', null=True, blank=True, related_name = 'english_main')

    def __str__(self):
        return self.english_word

    def get_alternatives(self):
        alternatives = English_Alternative.objects.filter(english_original = self)
        return alternatives

    def get_spanish(self):
        spanish = Spanish_Entry.objects.filter(english_entry = self)
        return spanish

    def get_comments(self):
        comment = Comment.objects.filter(english_entry = self)
        return comment


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
    english_entry = models.ForeignKey(English_Entry, on_delete=models.CASCADE, related_name = 'comments')
    author = models.CharField(max_length=100, default = 'engtranslator')
    text = models.TextField(max_length=500, null=False, blank=False)
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=True)

    def __str__(self):
        return self.text

    def approve(self):
        self.approved_comment = True
        self.save()
