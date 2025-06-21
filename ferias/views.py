
# Create your views here.

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Feria
from .forms import FeriaForm

def registrar_feria(request):
    """Vista para mostrar y procesar el formulario de registro de feria"""
    if request.method == 'POST':
        form = FeriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Feria registrada exitosamente!')
            return redirect('registrar_feria')  # Redirige al mismo formulario limpio
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = FeriaForm()
    
    return render(request, 'ferias/registro_feria.html', {'form': form})

def listar_ferias(request):
    """Vista para listar todas las ferias registradas"""
    ferias = Feria.objects.all().order_by('-fecha_creacion')
    return render(request, 'ferias/listar_ferias.html', {'ferias': ferias})
