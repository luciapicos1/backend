from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from .models import Itinerary, Destination, Accommodation
from django.db.models import Q

def home(request):
    return render(request, 'home.html')

class ItineraryCreateView(CreateView):
    model = Itinerary
    fields = ['title', 'description', 'destination', 'start_date', 'end_date']
    # Otras opciones de filtrado y ordenamiento
    template_name = 'itinerary_create.html'
    success_url = '/itineraries/'

class DestinationListView(ListView):
    model = Destination
    template_name = 'destination_list.html'
    def get_queryset(self):
        queryset = super().get_queryset()
        pais = self.request.GET.get('pais')  # Obtener el valor del parámetro 'pais' de la URL
        if pais:
            queryset = queryset.filter(pais__icontains=pais)  # Filtrar por país (insensible a mayúsculas y minúsculas)
        return queryset


class AccommodationListView(ListView):
    model = Accommodation
    # Opciones de filtrado y ordenamiento
    template_name = 'accommodation_list.html'

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import UserProfile

from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # Autenticar y loguear al usuario automáticamente
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            User.objects.create_user(username=username, password=password)
            user = authenticate(request, username=username, password=password)
    else:
        form = UserRegistrationForm()

    context = {
        'form': form,
    }

    return render(request, 'register.html', context=context)



def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  
    else:
        form = UserLoginForm(request)
    
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home') 

@login_required
def profile_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    # Lógica adicional para manejar la vista del perfil de usuario
    return render(request, 'profile.html', {'user_profile': user_profile})
 