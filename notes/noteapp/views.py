from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TagForm, NoteForm
from .models import Tag, Note


def main(request):
    notes = Note.objects.filter(
        user=request.user
    ).all() if request.user.is_authenticated else []
    return render(request, 'noteapp/index.html', {'notes': notes})


@login_required
def set_done(request, note_id):
    Note.objects.filter(pk=note_id, ser=request.user).update(done=True)
    return redirect(to='noteapp:main')


@login_required
def set_undone(request, note_id):
    Note.objects.filter(pk=note_id, ser=request.user).update(done=False)
    return redirect(to='noteapp:main')


@login_required
def delete_note(request, note_id):
    Note.objects.get(pk=note_id, ser=request.user).delete()
    return redirect(to='noteapp:main')


@login_required
def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save()
            tag.user = request.user
            return redirect(to='noteapp:main')
        else:
            return render(request, 'noteapp/tag.html', {'form': form})
    return render(request, 'noteapp/tag.html', {'form': TagForm()})


@login_required
def note(request):
    tags = Tag.objects.filter(user=request.user).all()

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            new_note = form.save()
            new_note.user = request.user
            choice_tags = Tag.objects.filter(
                name__in=request.POST.getlist('tags'),
                user=request.user
            )
            for tag in choice_tags:
                new_note.tags.add(tag)
        
            return redirect(to='noteapp:main')
        else:
            context = {'tags': tags, 'form': form}
            return render(request, 'noteapp/note.html', context)
    
    context = {'tags': tags, 'form': NoteForm()}
    return render(request, 'noteapp/note.html', context)


@login_required
def details(request, note_id):
    note = get_object_or_404(Note, pk=note_id, user=request.user)
    return render(request, 'noteapp/details.html', {'note': note})
