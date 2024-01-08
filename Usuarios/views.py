from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from .forms import UserRegisterForm, UserEditForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



@login_required
@permission_required('auth.view_user')
def list_users(request):
    users = User.objects.all().order_by('username')

    # Número de elementos por página
    elementos_por_pagina = 10  # Puedes ajustar este valor según tus necesidades

    # Crear un objeto Paginator
    paginator = Paginator(users, elementos_por_pagina)

    # Obtener el número de página desde la solicitud GET
    page = request.GET.get('page', 1)

    try:
        # Obtener la página actual
        users = paginator.page(page)
    except PageNotAnInteger:
        # Si la página no es un número entero, mostrar la primera página
        users = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera del rango (por ejemplo, 9999), mostrar la última página
        users = paginator.page(paginator.num_pages)

    context = {
        'users': users
    }

    return render(request, 'list_users.html', context)


@login_required
@permission_required('auth.add_user')
def create_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Devolver una respuesta HTML indicando éxito
            return render(request, 'create_user.html', {'success': True, 'message': f'Usuario {user.username} creado satisfactoriamente'})
        else:
            # Devolver una respuesta HTML indicando un error en el formulario
            return render(request, 'create_user.html', {'form': form, 'error_message': 'Error en el formulario'})
    else:
        form = UserRegisterForm()
    return render(request, 'create_user.html', {'form': form})


@login_required
@permission_required('auth.change_user')
def edit_user(request, user_id):
    try:
        user_instance = get_object_or_404(User, id=user_id)
    except User.DoesNotExist:
        raise Http404("El usuario no existe")
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user_instance)  # Asumiendo que tienes un formulario UserEditForm
        if form.is_valid():
            form.save()
            return render(request, 'edit_user.html', {'success': True, 'message': f'Usuario {form.instance.username} Editado satisfactoriamente'})
            # return redirect('Usuarios:list_users')
        else:
            # Devolver una respuesta HTML indicando un error en el formulario 
            return render(request, 'edit_user.html', {'form': form, 'error_message': 'Error inesperado, intente nuevamente. Asegúrese de completar correctamente todos los campos y seleccionar al menos un permiso.'})  
    else:
        form = UserEditForm(instance=user_instance)
    return render(request, 'edit_user.html', {'form': form})


@login_required
@permission_required('auth.change_user')
def edit_user(request, user_id):
    try:
        user_instance = get_object_or_404(User, id=user_id)
    except User.DoesNotExist:
        raise Http404("El usuario no existe")
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user_instance)  # Asumiendo que tienes un formulario UserEditForm
        if form.is_valid():
            form.save()
            return render(request, 'edit_user.html', {'success': True, 'message': f'Usuario {form.instance.username} Editado satisfactoriamente'})
        else:
            # Devolver una respuesta HTML indicando un error en el formulario 
            return render(request, 'edit_user.html', {'form': form, 'error_message': 'Error inesperado, intente nuevamente. Asegúrese de completar correctamente todos los campos y seleccionar al menos un permiso.'})  
    else:
        form = UserEditForm(instance=user_instance)
    return render(request, 'edit_user.html', {'form': form})


@login_required
@permission_required('auth.delete_user')
def delete_user(request, user_id):
    user_instance = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user_instance.delete()
        return render(request, 'delete_user_confirm.html', {'success': True, 'message': f'Usuario {user_instance.username} Eliminado satisfactoriamente'})
        # return redirect('Usuarios:list_users')
    return render(request, 'delete_user_confirm.html', {'user': user_instance})                                                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                                                             