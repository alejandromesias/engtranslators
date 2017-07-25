from django import forms

from glosario.models import (
 Chapter,
 Theme,
 English_Entry,
 English_Alternative,
 Spanish_Entry,
 Spanish_Alternative,
 Comment
)


class ChapterForm(forms.ModelForm):

    class Meta:
        model = Chapter
        fields = '__all__'


class ThemeForm(forms.ModelForm):

    class Meta:
        model = Theme
        fields = '__all__'

class English_EntryForm(forms.ModelForm):

    class Meta:
        model = English_Entry
        fields = '__all__'

class English_AlternativeForm(forms.ModelForm):

    class Meta:
        model = English_Alternative
        fields = '__all__'

class Spanish_EntryForm(forms.ModelForm):

    class Meta:
        model = Spanish_Entry
        fields = '__all__'

class Spanish_AlternativeForm(forms.ModelForm):

    class Meta:
        model = Spanish_Alternative
        fields = '__all__'

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = '__all__'
