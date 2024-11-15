from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import Usuario, RegistroKilometraje
from .forms import RegistroKilometrajeForm, UsuarioForm
from django.utils import timezone


def registro_usuario(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registrar_kilometraje')  # Cambia 'registrar_kilometraje' por el nombre correcto de la URL
    else:
        form = UsuarioForm()
    return render(request, 'usuarios/registro_usuario.html', {'form': form})

def registrar_kilometraje(request):
    if request.method == "POST":
        form = RegistroKilometrajeForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data['usuario']
            kilometros = form.cleaned_data['kilometros_recorridos']

            # Verificar si el usuario ya tiene registros previos de kilometraje para esa semana
            semana_actual = timezone.now().date()

            # Si ya existen registros de kilometraje para ese usuario, sumamos los nuevos kilómetros
            try:
                registro_existente = RegistroKilometraje.objects.filter(usuario=usuario, fecha=semana_actual).first()
                if registro_existente:
                    registro_existente.kilometros_recorridos += kilometros
                    registro_existente.save()
                else:
                    form.save()
            except RegistroKilometraje.DoesNotExist:
                form.save()

            return redirect('registrar_kilometraje')
    else:
        form = RegistroKilometrajeForm()

    return render(request, 'usuarios/registrar_kilometraje.html', {'form': form})
