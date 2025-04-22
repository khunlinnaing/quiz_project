from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *
from .forms import *
from django.contrib.auth.views import LogoutView
from django.contrib.auth import logout, login
from django.contrib import messages
from django.core.paginator import Paginator

# Check if user is superuser
def is_superuser(user):
    return user.is_superuser

class CustomLogoutView(LogoutView):
    http_method_names = ['get', 'post']  # Allow GET and POST
    next_page = '/'  # Redirect to quiz list

    def dispatch(self, request, *args, **kwargs):
        logout(request)  # Log out the user
        return redirect(self.next_page)  # Redirect to /
        
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after registration
            messages.success(request, 'Registration successful! Welcome to Quiz App.')
            return redirect('quiz_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

# Admin Dashboard
@user_passes_test(is_superuser)
@login_required
def admin_dashboard(request):
    quizzes = Quiz.objects.all()
    page_obj= paginatorVal(quizzes, request.GET.get('page'), 6)
    return render(request, 'dashboard/admin_dashboard.html', {'quizzes': page_obj})

# Add Quiz
@user_passes_test(is_superuser)
@login_required
def add_quiz(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        Quiz.objects.create(title=title, description=description)
        return redirect('admin_dashboard')
    return render(request, 'quizzes/add_quiz.html')

# Add Question
@user_passes_test(is_superuser)
@login_required
def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = QuestionForm()
    return render(request, 'questions/add_question.html', {'form': form})

# User Frontend
def quiz_list(request):
    quizzes = Quiz.objects.all()
    page_obj= paginatorVal(quizzes, request.GET.get('page'), 6)
    return render(request, 'quizzes/quiz_list.html', {'quizzes': page_obj})

@user_passes_test(is_superuser)
def edit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            messages.success(request, 'Quiz updated successfully!')
            return redirect('admin_dashboard')
    else:
        form = QuizForm(instance=quiz)
    return render(request, 'quizzes/edit_quiz.html', {'form': form, 'quiz': quiz})

@user_passes_test(is_superuser)
def delete_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        quiz.delete()
        messages.success(request, 'Quiz deleted successfully!')
        return redirect('admin_dashboard')
    return render(request, 'quizzes/delete_quiz.html', {'quiz': quiz})

@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()
    paginator = Paginator(questions, 1)
    page_number = int(request.GET.get('page') or 1)
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        question = page_obj[0]
        selected_option = request.POST.get(f"question_{question.id}")

        if selected_option:
            attempt, _ = UserAttempt.objects.get_or_create(
                user=request.user,
                quiz=quiz,
                defaults={'score': 0}
            )
            userans = UserAnswer.objects.filter(attempt=attempt, question=question).first()

            if userans:
                userans.selected_option = int(selected_option)
                userans.is_correct = int(selected_option) == question.correct_option
                userans.save()
            else:
                UserAnswer.objects.create(
                    attempt=attempt,
                    question=question,
                    selected_option=int(selected_option),
                    is_correct=int(selected_option) == question.correct_option
                )

        # Redirect to next page or result
        if page_obj.has_next():
            next_page = page_obj.next_page_number()
            return redirect(f"{request.path}?page={next_page}")
        else:
            # Calculate score
            correct_count = UserAnswer.objects.filter(attempt=attempt, is_correct=True).count()
            total = quiz.questions.count()
            score = (correct_count / total) * 100
            attempt.score = score
            attempt.save()
            return redirect('quiz_result', attempt_id=attempt.id)

    return render(request, 'quizzes/quiz_detail.html', {
        'page': page_number,
        'quiz': quiz,
        'questions': page_obj,
    })


@login_required
def quiz_result(request, attempt_id):
    attempt = get_object_or_404(UserAttempt, id=attempt_id, user=request.user)
    return render(request, 'quizzes/quiz_result.html', {'attempt': attempt})


@login_required
def user_dashboard(request):
    attempts =  UserAttempt.objects.filter(user=request.user).order_by('-attempted_at')
    return render(request, 'dashboard/user_dashboard.html', {'attempts': attempts})

# Paginator
def paginatorVal(objects, page, number):
    paginator = Paginator(objects, number)
    page_number = page 
    page_obj = paginator.get_page(page_number)
    return page_obj