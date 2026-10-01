from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Cliente, Vehiculo, VehiculoVendido, Perfil
from .decorators import usuario_required
from .forms import VehiculoVendidoForm, ClienteForm, VehiculoBasicoForm

# Solo los usuarios autenticados pueden acceder a la vista
@usuario_required
def index(request):
    # Obtiene usuario e id de la sesión
    usuario = User.objects.get(id=request.session['usuario_id'])
    return render(request, 'appgestion/index.html', {'usuario': usuario})

def login(request):
    error = None
    if request.method == 'POST':
        # Limpia el RUT capturado
        rut_input = request.POST.get('rut', '').replace('.', '').replace(' ', '').upper().strip()
        clave_input = request.POST.get('password', '')

        try:
            # Busca el perfil y compara la contraseña ingresada del user
            perfil = Perfil.objects.get(rut=rut_input)
            if perfil.user.check_password(clave_input):
                # Si es correcto, guarda el usuario_id en la sesión, con tal de no tener que ingresar las credenciales otra vez
                request.session['usuario_id'] = perfil.user.id
                return redirect('index')
            else:
                error = "RUT o contraseña incorrectos."
        except Perfil.DoesNotExist:
            error = "RUT o contraseña incorrectos."

    return render(request, 'appgestion/login.html', {'error': error})

def logout(request):
    request.session.flush()
    return redirect('login')

@usuario_required
def agregar_cliente_vehiculo(request):
    if request.method == 'POST':
        form_cliente = ClienteForm(request.POST)
        form_vehiculo = VehiculoBasicoForm(request.POST)

        if form_cliente.is_valid() and form_vehiculo.is_valid():
            rut_input = form_cliente.cleaned_data['rut'].replace('.', '').replace(' ', '').upper().strip()

            # Busca un cliente ya existente
            # Si no lo encuentra, entonces lo ingresa en la base de datos
            cliente, creado = Cliente.objects.get_or_create(
                rut=rut_input,
                defaults={
                    'nombre': form_cliente.cleaned_data['nombre'],
                    'apellidos': form_cliente.cleaned_data['apellidos']
                }
            )

            # Asocia el vehiculo con el cliente y lo guarda
            vehiculo = form_vehiculo.save(commit=False)
            vehiculo.cliente = cliente
            vehiculo.save()
            return redirect('listar_clientes_vehiculos')
    else:
        form_cliente = ClienteForm()
        form_vehiculo = VehiculoBasicoForm()

    return render(request, 'appgestion/agregar_cliente_vehiculo.html', {
        'form_cliente': form_cliente,
        'form_vehiculo': form_vehiculo
    })

@usuario_required
def agregar_venta(request):
    if request.method == 'POST':
        # Si los datos ingresados son válidos, los almacena en la base de datos
        form = VehiculoVendidoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_ventas')
    else:
        form = VehiculoVendidoForm()
    return render(request, 'appgestion/agregar_venta.html', {'form': form})

@usuario_required
def listar_clientes_vehiculos(request):
    # Lista los nombres de los clientes y los datos de los vehículos asociados
    vehiculos = Vehiculo.objects.select_related('cliente').all()
    return render(request, 'appgestion/listar_clientes_vehiculos.html', {'vehiculos': vehiculos})

@usuario_required
def buscar_cliente(request):
    # Utiliza GET para buscar un cliente en específico y sus vehículos a través del RUT
    rut_busqueda = request.GET.get('rut')
    cliente_encontrado = None
    vehiculos = None
    if rut_busqueda:
        try:
            cliente_encontrado = Cliente.objects.get(rut=rut_busqueda)
            vehiculos = Vehiculo.objects.filter(cliente=cliente_encontrado)
        except Cliente.DoesNotExist:
            pass
    return render(request, 'appgestion/buscar_cliente.html', {'cliente': cliente_encontrado, 'vehiculos': vehiculos})

@usuario_required
def listar_ventas(request):
    ventas = VehiculoVendido.objects.select_related('vehiculo').all()
    return render(request, 'appgestion/listar_ventas.html', {'ventas': ventas})

@usuario_required
def eliminar_vehiculo(request, id_vehiculo):
    try:
        # Busca un vehículo a través de su id y luego lo elimina (junto a las asociaciones del objeto)
        vehiculo = Vehiculo.objects.get(id_vehiculo=id_vehiculo)
        vehiculo.delete()
    except Vehiculo.DoesNotExist:
        pass
    return redirect('listar_clientes_vehiculos')