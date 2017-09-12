from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.forms.formsets import formset_factory
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect

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


from django.views.generic import (View,TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)

from django.urls import reverse_lazy
from django.core.urlresolvers import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from itertools import chain
from django.db.models.functions import Lower
from glosario.namepaginator import NamePaginator
from . import forms
from django.contrib.auth.models import Group, User

class SignUpView(CreateView):
    form_class = forms.UserSingupForm
    success_url = reverse_lazy('login')
    template_name = 'glosario/registro.html'

    def form_valid(self, form):
        self.object = form.save()
        grupo_registrado = Group.objects.get(name='Registrados')
        grupo_registrado.user_set.add(self.object)

        return HttpResponseRedirect(self.get_success_url())

class IndexView(TemplateView):
    template_name = 'glosario/index.html'

class GlosarySearchView(ListView):
    template_name = 'glosario/busqueda.html'
    model = Chapter

    def get_context_data(self, **kwargs):
        query = self.request.GET.get('query_text')
        context = super(GlosarySearchView, self).get_context_data(**kwargs)
        context['Temas'] = Theme.objects.all()

        if query:
            context['echo_query'] = query

            found_in_theme = Theme.objects.filter(theme_name__iexact = query)
            found_in_english_entry = English_Entry.objects.filter(english_word__iexact = query)
            found_in_english_alternative = English_Alternative.objects.filter(english_synonym__iexact = query)
            found_in_spanish_entry = Spanish_Entry.objects.filter(spanish_word__iexact = query)
            found_in_spanish_definition = Spanish_Entry.objects.filter(spanish_definition__iexact = query)
            found_in_spanish_total = found_in_spanish_entry | found_in_spanish_definition
            found_in_spanish_alternative = Spanish_Alternative.objects.filter(spanish_synonym__iexact = query)

            if(found_in_theme or found_in_english_entry or found_in_english_alternative or
                found_in_spanish_total or found_in_spanish_alternative ):
                context['found_in_theme'] = found_in_theme
                context['found_in_english_entry'] = found_in_english_entry
                context['found_in_english_alternative'] = found_in_english_alternative
                context['found_in_spanish_total'] = found_in_spanish_total
                context['found_in_spanish_alternative'] = found_in_spanish_alternative
            else:
                not_found = True
                context['not_found'] = not_found

        return context

class ChapterCreateView(PermissionRequiredMixin,CreateView):
    permission_required = 'glosario.can_create_chapter'
    model = Chapter
    template_name = "glosario/chapter_create.html"
    fields=('chapter_name',)

class ThemeCreateView(PermissionRequiredMixin,CreateView):
    permission_required = 'glosario.can_create_theme'
    model = Theme
    template_name = "glosario/theme_create.html"
    fields=('theme_name','parent_chapter',)

class CommentCreateView(PermissionRequiredMixin,TemplateView):
    permission_required = 'glosario.can_write_comment'

    template_name = "glosario/comment_create.html"
    def get(self, request, *args, **kwargs):

        pk = self.kwargs['pk']
        this_entry = get_object_or_404(English_Entry, pk=pk)
        Comment_FormSet = inlineformset_factory(English_Entry,Comment,
            exclude=('author','approved_comment'),extra=1, can_delete=False)
        context = {'entry_detail': this_entry,
                'form_comment': Comment_FormSet()}

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        this_entry = get_object_or_404(English_Entry, pk=pk)
        Comment_FormSet = inlineformset_factory(English_Entry,Comment,
            exclude=('author',),extra=0, can_delete=False)

        form_comment = Comment_FormSet(request.POST, instance = this_entry)

        if (form_comment.is_valid()):
            form_comment.save()

        return HttpResponseRedirect(reverse("entry_detail",kwargs={'pk':this_entry.id}))


class ChaptersListView(ListView):
    model = Chapter
    context_object_name = 'chapters'
    template_name = 'glosario/chapters_list.html'

class ThemesInChapterView(TemplateView):
    template_name = 'glosario/themes_in_chapter.html'

    def get(self, request, *args, **kwargs):
        chapter = self.kwargs['chapter']
        this_chapter = get_object_or_404(Chapter, chapter_name=chapter)
        themes_set = this_chapter.child_themes.all().order_by(Lower('theme_name'))
        context = {'this_chapter': chapter,
                'themes_set': themes_set}

        return self.render_to_response(context)


class EntriesInThemeView(TemplateView):
    template_name = 'glosario/entries_in_theme.html'

    def get(self, request, *args, **kwargs):
        chapter = self.kwargs['chapter']
        theme = self.kwargs['theme']
        this_theme = get_object_or_404(Theme, theme_name=theme)
        entries_set = this_theme.child_entries.all().order_by(Lower('english_word'))
        alternatives_set = English_Alternative.objects.filter(
            english_original__parent_theme__theme_name = theme).order_by(Lower('english_synonym'))

        context = {'this_chapter': chapter,
                'this_theme': theme,
                'entries_set': entries_set,
                'alternatives_set': alternatives_set}

        return self.render_to_response(context)

class EntriesListView(ListView):
    model = English_Entry
    context_object_name = 'entries'
    template_name = 'glosario/entry_list.html'
    ordering = [Lower('english_word')]

class EntriesDetailView(DetailView):
    model = English_Entry
    context_object_name = 'entry_detail'
    template_name = 'glosario/entry_detail.html'

class EntryCreateView(PermissionRequiredMixin, TemplateView):
    permission_required = 'glosario.can_create_entry'

    template_name = 'english_entry_form.html'

    def get(self, request, *args, **kwargs):

        English_AlternativeFormSet = inlineformset_factory(English_Entry,English_Alternative,exclude=(),extra=2, can_delete=False)
        Spanish_EntryFormSet = inlineformset_factory(English_Entry,Spanish_Entry,exclude=(),extra=1, can_delete=False)
        Spanish_AlternativeFormSet = inlineformset_factory(Spanish_Entry,Spanish_Alternative,exclude=(),extra=2, can_delete=False)
        Comment_FormSet = inlineformset_factory(English_Entry,Comment,exclude=(),extra=2, can_delete=False)

        context = {'form_english_entry': English_EntryForm(),
                'form_english_alternative': English_AlternativeFormSet(),
                'form_spanish_entry': Spanish_EntryFormSet(),
                'form_spanish_alternative': Spanish_AlternativeFormSet(),
                'form_comment': Comment_FormSet()}

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):

        English_AlternativeFormSet = inlineformset_factory(English_Entry,English_Alternative,exclude=(),extra=2, can_delete=False)
        Spanish_EntryFormSet = inlineformset_factory(English_Entry,Spanish_Entry,exclude=(),extra=1, can_delete=False)
        Spanish_AlternativeFormSet = inlineformset_factory(Spanish_Entry,Spanish_Alternative,exclude=(),extra=2, can_delete=False)
        Comment_FormSet = inlineformset_factory(English_Entry,Comment,exclude=(),extra=2, can_delete=False)

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
                        form.save()

            if(inform_spanish_entry.is_valid()):
                for form in inform_spanish_entry:
                    if form.is_valid() and form.has_changed():
                        new_spanish_entry = form.save()

                    this_spanish_entry = this_entry.child_spanish
                    inform_spanish_alternative = Spanish_AlternativeFormSet(request.POST, instance = this_spanish_entry)

                    if (inform_spanish_alternative.is_valid()):
                        for sform in inform_spanish_alternative:
                            if sform.is_valid() and sform.has_changed():
                                sform.save()

            if(inform_comment.is_valid()):
                for form in inform_comment:
                    if form.is_valid() and form.has_changed():
                        form.save()

        return HttpResponseRedirect(reverse("entry_detail",kwargs={'pk':this_entry.id}))


class EntryUpdateView(PermissionRequiredMixin, TemplateView):
    permission_required = 'glosario.can_edit_entry'

    template_name = 'english_entry_update.html'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        this_entry = get_object_or_404(English_Entry, pk=pk)
        this_spanish_entry = this_entry.child_spanish

        English_AlternativeFormSet = inlineformset_factory(English_Entry,English_Alternative,exclude=(),extra=2, can_delete=False)
        Spanish_EntryFormSet = inlineformset_factory(English_Entry,Spanish_Entry,exclude=(),extra=1, can_delete=False)
        Spanish_AlternativeFormSet = inlineformset_factory(Spanish_Entry,Spanish_Alternative,exclude=(),extra=2, can_delete=False)
        Comment_FormSet = inlineformset_factory(English_Entry,Comment,exclude=(),extra=2, can_delete=False)

        context = {'form_english_entry': English_EntryForm(instance=this_entry),
                'form_english_alternative': English_AlternativeFormSet(instance=this_entry),
                'form_spanish_entry': Spanish_EntryFormSet(instance=this_entry),
                'form_spanish_alternative': Spanish_AlternativeFormSet(instance=this_spanish_entry),
                'form_comment': Comment_FormSet(instance=this_entry)}

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):

        English_AlternativeFormSet = inlineformset_factory(English_Entry,English_Alternative,exclude=(),extra=2, can_delete=False)
        Spanish_EntryFormSet = inlineformset_factory(English_Entry,Spanish_Entry,exclude=(),extra=1, can_delete=False)
        Spanish_AlternativeFormSet = inlineformset_factory(Spanish_Entry,Spanish_Alternative,exclude=(),extra=2, can_delete=False)
        Comment_FormSet = inlineformset_factory(English_Entry,Comment,exclude=(),extra=2, can_delete=False)

        pk = self.kwargs['pk']
        this_entry = get_object_or_404(English_Entry, pk=pk)
        print('antes')

        form_english_entry = English_EntryForm(request.POST, instance = this_entry)

        if(form_english_entry.is_valid()):
            print('despues')
            new_english_entry = form_english_entry.save()

            #this_entry = English_Entry.objects.get(id = new_english_entry.id)

            inform_spanish_entry = Spanish_EntryFormSet(request.POST, instance = this_entry)
            inform_english_alternative = English_AlternativeFormSet(request.POST, instance = this_entry)
            inform_comment = Comment_FormSet(request.POST, instance = this_entry)

            if(inform_english_alternative.is_valid()):
                for form in inform_english_alternative:
                    if form.is_valid() and form.has_changed():
                        form.save()

            if(inform_spanish_entry.is_valid()):
                for form in inform_spanish_entry:
                    if form.is_valid() and form.has_changed():
                        new_spanish_entry = form.save()

                    this_spanish_entry = this_entry.child_spanish
                    inform_spanish_alternative = Spanish_AlternativeFormSet(request.POST, instance = this_spanish_entry)

                    print('befor alternative')
                    if (inform_spanish_alternative.is_valid()):
                        print('spanish alternative form is valid')
                        for sform in inform_spanish_alternative:
                            if sform.is_valid() and sform.has_changed():
                                print('sform has changed')
                                sform.save()

            if(inform_comment.is_valid()):
                for form in inform_comment:
                    if form.is_valid() and form.has_changed():
                        form.save()

        return HttpResponseRedirect(reverse("entry_detail",kwargs={'pk':this_entry.id}))
