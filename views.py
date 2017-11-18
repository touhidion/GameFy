from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserLoginForm
from .models import Game, Gamer, User
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)
from django.contrib.auth.decorators import login_required

def index_view(request):
    return render(request, 'gamefy/index.html')

def registration_view(request):
    logout(request)#logged out if already login

    form = UserRegistrationForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        #user.set_password is built in method for User model, otherwise pass wont be saved
        user.set_password(password)
        user.save()
        return redirect('gamefy:login')

    context = {'form':form, 'title':'User Registration', 'submit':'Register'}
    return render(request, 'gamefy/form.html', context)

def login_view(request):
    next = request.GET.get('next')#for login_requied page, mendatory

    form = UserLoginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        login(request, user)
        if next:#for login_required page, mendatory
            return redirect(next)

        return redirect('gamefy:game')

    # for login_required page, login form message, optional
    context = {'form':form, 'title':'Login Form', 'submit':'Login', 'log_require_message':'You must be logged in!'}
    if next:
        return render(request, 'gamefy/form.html', context)

    context = {'form': form, 'title': 'Login Form', 'submit': 'Login'}
    return render(request, 'gamefy/form.html', context)

def logout_view(request):
    logout(request)
    return redirect('gamefy:index')

@login_required(login_url='/gamefy/login')
def game_view(request):
    found_gamer_obj = Gamer.objects.filter(user=request.user)

    if request.method == 'POST':
        score = request.POST.get('score')
        print(score)

        if not found_gamer_obj:
            gamer_obj = Gamer(user=request.user, game_one_score=score)
            gamer_obj.save()
        else:
            gamer_obj = Gamer.objects.get(user=request.user)
            gamer_obj.game_one_score=score
            gamer_obj.save()

    previous_score = None
    if found_gamer_obj:
        previous_score = Gamer.objects.get(user=request.user).game_one_score
    else:
        previous_score = 1000#1000 is just an assumed highest value to compare high score

    return render(request, 'gamefy/games.html', {'previous_score':previous_score})

def profile_view(request):
    if request.user.is_authenticated():
        found_current_gamer_list_for_score = Gamer.objects.filter(user=request.user)
        # if gamer played at least once and made a score which is saved
        if found_current_gamer_list_for_score:
            context = {'gamer':found_current_gamer_list_for_score[0]}
            return render(request, 'gamefy/profile.html', context)
        else:
            return render(request, 'gamefy/profile.html')

    #if try to manually enter the profile without having loggedin
    return redirect('gamefy:error-404')

@login_required(login_url='/gamefy/login/')
def score_board_view(request):
    all_gamer_objrcts_list = Gamer.objects.all().order_by('game_one_score');
    context = {'all_gamers': all_gamer_objrcts_list}
    return render(request, 'gamefy/scoreboard.html', context)

def error_view(request):
    return render(request, 'gamefy/404.html')

def delete_gamer_view(request):
    try:
        to_be_deleted_user = User.objects.get(username=request.user)
        to_be_deleted_user.delete()

        print(to_be_deleted_user, 'deleted')

    except User.DoesNotExist:
        print('error1')
        return redirect('gamefy:index')

    except Exception as e:
        print('error2')
        return redirect('gamefy:index')

    return redirect('gamefy:index')