from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Question, Choice


def index(request):
    latest_question_list = get_list_or_404(Question.objects.order_by('-pub_date')[:5])
    context = {'latest_question_list': latest_question_list}
    try:
        return render(request, 'polls/index.html', context)
    except Question.DoesNotExist:
        return HttpResponse("No hay preguntas disponibles")



def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        return render(request, 'polls/detail.html', {'question': question})
    except Question.DoesNotExist:
        return HttpResponse("No hay preguntas disponibles")


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        return render(request, 'polls/results.html', {'question': question})
    except Question.DoesNotExist:
        return HttpResponse("No hay preguntas disponibles")


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

