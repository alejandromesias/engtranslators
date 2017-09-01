from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.forms.formsets import formset_factory
from django.forms import inlineformset_factory

from glosario.models import (
 Chapter,
 Theme,
 English_Entry,
 English_Alternative,
 Spanish_Entry,
 Spanish_Alternative,
 Comment
)
from glosario.forms import (
 ChapterForm,
 ThemeForm,
 English_EntryForm,
 English_AlternativeForm,
 Spanish_EntryForm,
 Spanish_AlternativeForm,
 CommentForm
)


from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

def index(request):
    return render(request, 'glosario/index.html')

def enlistar(request):
    chapters = Chapter.objects.all()
    themes = Theme.objects.all()
    e_entries = English_Entry.objects.all()

    data = {'chapters':chapters,
            'themes':themes,
            'e_entries':e_entries
            }
    return render(request, 'glosario/english_entry_list.html',data)

def enlistarTemas(request):
    chapters = Chapter.objects.all()
    themes = Theme.objects.all()
    e_entries = English_Entry.objects.all()

    data = {'chapters':chapters,
            'themes':themes,
            'e_entries':e_entries
            }
    return render(request, 'glosario/themes_list.html',data)

def create_temas(request):
    ThemeFormSet = formset_factory(ThemeForm, extra = 4)
    message = "welcome"

    if request.method == "POST":
        formset = ThemeFormSet(request.POST)

        if(formset.is_valid()):
            message = "Thank you"
            for form in formset:
                form.save()
        else:
            message = "Something went wrong"

    return render(request, 'glosario/create_temas.html', {'formset' : ThemeFormSet(), 'message' : message})

def create_entry(request):
    English_AlternativeFormSet = inlineformset_factory(English_Entry,English_Alternative,exclude=(),extra=2, can_delete=False)
    Spanish_EntryFormSet = inlineformset_factory(English_Entry,Spanish_Entry,exclude=(),extra=1, can_delete=False)
    Spanish_AlternativeFormSet = inlineformset_factory(Spanish_Entry,Spanish_Alternative,exclude=(),extra=2, can_delete=False)
    Comment_FormSet = inlineformset_factory(English_Entry,Comment,exclude=(),extra=2, can_delete=False)

    message = "status: "
    this_entry = None

    if request.method == "POST":
        form_english_entry = English_EntryForm(request.POST)

        if(form_english_entry.is_valid()):
            new_english_entry = form_english_entry.save()

            this_entry = English_Entry.objects.get(id = new_english_entry.id)

            inform_spanish_entry = Spanish_EntryFormSet(request.POST, instance = this_entry)
            inform_english_alternative = English_AlternativeFormSet(request.POST, instance = this_entry)
            inform_comment = Comment_FormSet(request.POST, instance = this_entry)

            if(inform_english_alternative.is_valid()):
                for form in inform_english_alternative:
                    if form.is_valid() and form.has_changed():
                        message += "alter, "
                        form.save()

            if(inform_spanish_entry.is_valid()):
                for form in inform_spanish_entry:
                    if form.is_valid() and form.has_changed():
                        message += "spa, "
                        new_spanish_entry = form.save()
                        this_spanish_entry = Spanish_Entry.objects.get(id = new_spanish_entry.id)
                        inform_spanish_alternative = Spanish_AlternativeFormSet(request.POST, instance = this_spanish_entry)

                        if (inform_spanish_alternative.is_valid()):
                            for sform in inform_spanish_alternative:
                                if sform.is_valid() and sform.has_changed():
                                    message += "spaAlter, "
                                    sform.save()


            if(inform_comment.is_valid()):
                for form in inform_comment:
                    if form.is_valid() and form.has_changed():
                        message += "comm, "
                        form.save()
            else:
                message = "Something went wrong"


    forms_group = {'form_english_entry': English_EntryForm(),
            'form_english_alternative': English_AlternativeFormSet(),
            'form_spanish_entry': Spanish_EntryFormSet(),
            'form_spanish_alternative': Spanish_AlternativeFormSet(),
            'form_comment': Comment_FormSet(),
            'this_entry': this_entry,
            'message' : message}

    return render(request, 'glosario/create_entry.html', forms_group )

def guardar_formulario(formulario):
    if formulario.is_valid():
        formulario.save(commit = True)
