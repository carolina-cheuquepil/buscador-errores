from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.db.models import Prefetch
from django.core.paginator import Paginator
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .dominios.catalogos import Prueba
from .dominios.errores import Error, ErrorSolucion
from .dominios.plataforma import Hardware, HardwareSistema, Modulo, Sistema
from .dominios.soluciones import Departamento, Responsable, Solucion, SolucionAsignacion
from .forms import (
    BusquedaForm,
    DepartamentoContactoFormSet,
    DepartamentoForm,
    ErrorForm,
    HardwareForm,
    PruebaForm,
    ResponsableForm,
    SistemaForm,
    SolucionForm,
    SolucionRapidaForm,
)


def _hardware_sistemas_context():
    relaciones = HardwareSistema.objects.select_related('hardware', 'sistema').values_list(
        'hardware_id',
        'sistema_id',
    )
    hardware_sistemas = {}
    for hardware_id, sistema_id in relaciones:
        hardware_sistemas.setdefault(str(hardware_id), []).append(str(sistema_id))
    return hardware_sistemas


def _sistema_modulos_context():
    modulos = Modulo.objects.values_list('sistema_id', 'id')
    sistema_modulos = {}
    for sistema_id, modulo_id in modulos:
        sistema_modulos.setdefault(str(sistema_id), []).append(str(modulo_id))
    return sistema_modulos


def lista_errores(request):
    form = BusquedaForm(request.GET or None)
    qs = Error.objects.select_related('hardware', 'frecuencia').prefetch_related(
        Prefetch(
            'errorsolucion_set',
            queryset=ErrorSolucion.objects.select_related('solucion').prefetch_related(
                Prefetch(
                    'solucion__asignaciones',
                    queryset=SolucionAsignacion.objects.select_related(
                        'responsable',
                        'departamento',
                    ).prefetch_related('departamento__contactos').filter(
                        activo=True,
                    ).order_by(
                        '-principal',
                        'responsable__nombre',
                        'departamento__nombre',
                    ),
                )
            ).order_by('orden', 'solucion__nombre'),
            to_attr='soluciones_del_error',
        )
    ).all()

    q = request.GET.get('q', '').strip()
    hardware_id = request.GET.get('hardware')
    sistema_id = request.GET.get('sistema')
    frecuencia_id = request.GET.get('frecuencia')

    if q:
        qs = qs.filter(
            Q(descripcion__icontains=q)
            | Q(causa__icontains=q)
            | Q(soluciones__nombre__icontains=q)
            | Q(soluciones__pasos__icontains=q)
            | Q(soluciones__anexos__icontains=q)
            | Q(comentarios__icontains=q)
            | Q(usuario__icontains=q)
            | Q(modulo__nombre__icontains=q)
        ).distinct()

    if hardware_id:
        qs = qs.filter(hardware_id=hardware_id)
    if sistema_id:
        qs = qs.filter(sistema_id=sistema_id)
    if frecuencia_id:
        qs = qs.filter(frecuencia_id=frecuencia_id)

    total = qs.count()
    paginator = Paginator(qs, 25)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    # Build querystring sin 'page' para mantener filtros al paginar
    params = request.GET.copy()
    params.pop('page', None)
    querystring = params.urlencode()

    return render(request, 'errores/error_list.html', {
        'form': form,
        'page_obj': page_obj,
        'total': total,
        'q': q,
        'querystring': querystring,
    })


def detalle_error(request, pk):
    error = get_object_or_404(
        Error.objects.select_related('hardware', 'sistema', 'modulo', 'frecuencia').prefetch_related(
            Prefetch(
                'errorsolucion_set',
                queryset=ErrorSolucion.objects.select_related('solucion').prefetch_related(
                    Prefetch(
                        'solucion__asignaciones',
                        queryset=SolucionAsignacion.objects.select_related(
                            'responsable',
                            'departamento',
                        ).prefetch_related('departamento__contactos').filter(
                            activo=True,
                        ).order_by(
                            '-principal',
                            'responsable__nombre',
                            'departamento__nombre',
                        ),
                    )
                ).order_by('orden', 'solucion__nombre'),
                to_attr='soluciones_del_error',
            )
        ),
        pk=pk,
    )
    soluciones_del_error = list(error.soluciones_del_error)

    return render(request, 'errores/error_detail.html', {
        'error': error,
        'soluciones_del_error': soluciones_del_error,
    })


def crear_error(request):
    if request.method == 'POST':
        form = ErrorForm(request.POST)
        if form.is_valid():
            error = form.save()
            messages.success(request, f'Error #{error.id} creado correctamente.')
            return redirect(reverse('errores:detalle', args=[error.pk]))
    else:
        form = ErrorForm()
    return render(request, 'errores/error_form.html', {
        'form': form,
        'titulo': 'Agregar nuevo error',
        'boton': 'Crear',
        'responsables_activos': Responsable.objects.filter(activo=True),
        'departamentos_activos': Departamento.objects.filter(activo=True),
        'hardware_sistemas': _hardware_sistemas_context(),
        'sistema_modulos': _sistema_modulos_context(),
    })


def editar_error(request, pk):
    error = get_object_or_404(Error, pk=pk)
    if request.method == 'POST':
        form = ErrorForm(request.POST, instance=error)
        if form.is_valid():
            form.save()
            messages.success(request, f'Error #{error.id} actualizado.')
            return redirect(reverse('errores:detalle', args=[error.pk]))
    else:
        form = ErrorForm(instance=error)
    return render(request, 'errores/error_form.html', {
        'form': form,
        'titulo': f'Editar error #{error.id}',
        'boton': 'Guardar cambios',
        'error': error,
        'responsables_activos': Responsable.objects.filter(activo=True),
        'departamentos_activos': Departamento.objects.filter(activo=True),
        'hardware_sistemas': _hardware_sistemas_context(),
        'sistema_modulos': _sistema_modulos_context(),
    })


def eliminar_error(request, pk):
    error = get_object_or_404(Error, pk=pk)
    if request.method == 'POST':
        eid = error.id
        error.delete()
        messages.success(request, f'Error #{eid} eliminado.')
        return redirect('errores:lista')
    return render(request, 'errores/error_confirm_delete.html', {'error': error})


def lista_hardware(request):
    hardware = Hardware.objects.prefetch_related('sistemas').all()
    return render(request, 'errores/plataforma/hardware_list.html', {
        'hardware_list': hardware,
    })


def crear_hardware(request):
    if request.method == 'POST':
        form = HardwareForm(request.POST)
        if form.is_valid():
            hardware = form.save()
            messages.success(request, f'Hardware "{hardware}" creado correctamente.')
            return redirect('errores:hardware_lista')
    else:
        form = HardwareForm()
    return render(request, 'errores/plataforma/form.html', {
        'form': form,
        'titulo': 'Nuevo hardware',
        'boton': 'Crear',
        'volver_url': reverse('errores:hardware_lista'),
    })


def editar_hardware(request, pk):
    hardware = get_object_or_404(Hardware, pk=pk)
    if request.method == 'POST':
        form = HardwareForm(request.POST, instance=hardware)
        if form.is_valid():
            form.save()
            messages.success(request, f'Hardware "{hardware}" actualizado.')
            return redirect('errores:hardware_lista')
    else:
        form = HardwareForm(instance=hardware)
    return render(request, 'errores/plataforma/form.html', {
        'form': form,
        'titulo': f'Editar hardware: {hardware}',
        'boton': 'Guardar',
        'volver_url': reverse('errores:hardware_lista'),
    })


def eliminar_hardware(request, pk):
    hardware = get_object_or_404(Hardware, pk=pk)
    if request.method == 'POST':
        nombre = str(hardware)
        hardware.delete()
        messages.success(request, f'Hardware "{nombre}" eliminado.')
        return redirect('errores:hardware_lista')
    return render(request, 'errores/plataforma/confirm_delete.html', {
        'objeto': hardware,
        'tipo': 'hardware',
        'volver_url': reverse('errores:hardware_lista'),
    })


def lista_sistemas(request):
    sistemas = Sistema.objects.prefetch_related('modulos').all()
    return render(request, 'errores/plataforma/sistema_list.html', {
        'sistemas': sistemas,
    })


def crear_sistema(request):
    if request.method == 'POST':
        form = SistemaForm(request.POST)
        if form.is_valid():
            sistema = form.save()
            messages.success(request, f'Sistema "{sistema}" creado correctamente.')
            return redirect('errores:sistema_lista')
    else:
        form = SistemaForm()
    return render(request, 'errores/plataforma/form.html', {
        'form': form,
        'titulo': 'Nuevo sistema',
        'boton': 'Crear',
        'volver_url': reverse('errores:sistema_lista'),
    })


def editar_sistema(request, pk):
    sistema = get_object_or_404(Sistema, pk=pk)
    if request.method == 'POST':
        form = SistemaForm(request.POST, instance=sistema)
        if form.is_valid():
            form.save()
            messages.success(request, f'Sistema "{sistema}" actualizado.')
            return redirect('errores:sistema_lista')
    else:
        form = SistemaForm(instance=sistema)
    return render(request, 'errores/plataforma/form.html', {
        'form': form,
        'titulo': f'Editar sistema: {sistema}',
        'boton': 'Guardar',
        'volver_url': reverse('errores:sistema_lista'),
    })


def eliminar_sistema(request, pk):
    sistema = get_object_or_404(Sistema, pk=pk)
    if request.method == 'POST':
        nombre = str(sistema)
        sistema.delete()
        messages.success(request, f'Sistema "{nombre}" eliminado.')
        return redirect('errores:sistema_lista')
    return render(request, 'errores/plataforma/confirm_delete.html', {
        'objeto': sistema,
        'tipo': 'sistema',
        'volver_url': reverse('errores:sistema_lista'),
    })


def lista_responsables(request):
    responsables = Responsable.objects.select_related('departamento').all()
    return render(request, 'errores/responsables/responsable_list.html', {
        'responsables': responsables,
    })


def crear_responsable(request):
    if request.method == 'POST':
        form = ResponsableForm(request.POST)
        if form.is_valid():
            responsable = form.save()
            messages.success(request, f'Responsable "{responsable}" creado correctamente.')
            return redirect('errores:responsable_lista')
    else:
        form = ResponsableForm()
    return render(request, 'errores/plataforma/form.html', {
        'form': form,
        'titulo': 'Nuevo responsable',
        'boton': 'Crear',
        'volver_url': reverse('errores:responsable_lista'),
    })


def editar_responsable(request, pk):
    responsable = get_object_or_404(Responsable, pk=pk)
    if request.method == 'POST':
        form = ResponsableForm(request.POST, instance=responsable)
        if form.is_valid():
            form.save()
            messages.success(request, f'Responsable "{responsable}" actualizado.')
            return redirect('errores:responsable_lista')
    else:
        form = ResponsableForm(instance=responsable)
    return render(request, 'errores/plataforma/form.html', {
        'form': form,
        'titulo': f'Editar responsable: {responsable}',
        'boton': 'Guardar',
        'volver_url': reverse('errores:responsable_lista'),
    })


def eliminar_responsable(request, pk):
    responsable = get_object_or_404(Responsable, pk=pk)
    if request.method == 'POST':
        nombre = str(responsable)
        responsable.delete()
        messages.success(request, f'Responsable "{nombre}" eliminado.')
        return redirect('errores:responsable_lista')
    return render(request, 'errores/plataforma/confirm_delete.html', {
        'objeto': responsable,
        'tipo': 'responsable',
        'volver_url': reverse('errores:responsable_lista'),
    })


def lista_departamentos(request):
    departamentos = Departamento.objects.prefetch_related('responsables', 'contactos').all()
    return render(request, 'errores/departamentos/departamento_list.html', {
        'departamentos': departamentos,
    })


def detalle_departamento(request, pk):
    departamento = get_object_or_404(
        Departamento.objects.prefetch_related('contactos', 'responsables'),
        pk=pk,
    )
    responsables = departamento.responsables.all()
    return render(request, 'errores/departamentos/departamento_detail.html', {
        'departamento': departamento,
        'responsables': responsables,
    })


def crear_departamento(request):
    if request.method == 'POST':
        form = DepartamentoForm(request.POST)
        contacto_formset = DepartamentoContactoFormSet(request.POST)
        if form.is_valid() and contacto_formset.is_valid():
            departamento = form.save()
            contacto_formset.instance = departamento
            contacto_formset.save()
            messages.success(request, f'Departamento "{departamento}" creado correctamente.')
            return redirect('errores:departamento_lista')
    else:
        form = DepartamentoForm()
        contacto_formset = DepartamentoContactoFormSet()
    return render(request, 'errores/plataforma/form.html', {
        'form': form,
        'contacto_formset': contacto_formset,
        'titulo': 'Nuevo departamento',
        'boton': 'Crear',
        'volver_url': reverse('errores:departamento_lista'),
    })


def editar_departamento(request, pk):
    departamento = get_object_or_404(Departamento, pk=pk)
    if request.method == 'POST':
        form = DepartamentoForm(request.POST, instance=departamento)
        contacto_formset = DepartamentoContactoFormSet(request.POST, instance=departamento)
        if form.is_valid() and contacto_formset.is_valid():
            form.save()
            contacto_formset.save()
            messages.success(request, f'Departamento "{departamento}" actualizado.')
            return redirect('errores:departamento_lista')
    else:
        form = DepartamentoForm(instance=departamento)
        contacto_formset = DepartamentoContactoFormSet(instance=departamento)
    return render(request, 'errores/plataforma/form.html', {
        'form': form,
        'contacto_formset': contacto_formset,
        'titulo': f'Editar departamento: {departamento}',
        'boton': 'Guardar',
        'volver_url': reverse('errores:departamento_lista'),
    })


def eliminar_departamento(request, pk):
    departamento = get_object_or_404(Departamento, pk=pk)
    if request.method == 'POST':
        nombre = str(departamento)
        departamento.delete()
        messages.success(request, f'Departamento "{nombre}" eliminado.')
        return redirect('errores:departamento_lista')
    return render(request, 'errores/plataforma/confirm_delete.html', {
        'objeto': departamento,
        'tipo': 'departamento',
        'volver_url': reverse('errores:departamento_lista'),
    })


def crear_responsable_departamento(request, departamento_pk):
    departamento = get_object_or_404(Departamento, pk=departamento_pk)
    if request.method == 'POST':
        form = ResponsableForm(request.POST)
        if form.is_valid():
            responsable = form.save(commit=False)
            responsable.departamento = departamento
            responsable.save()
            messages.success(request, f'Responsable "{responsable}" creado correctamente.')
            return redirect('errores:departamento_detalle', pk=departamento.pk)
    else:
        form = ResponsableForm(initial={'departamento': departamento})
    form.fields['departamento'].disabled = True
    return render(request, 'errores/plataforma/form.html', {
        'form': form,
        'titulo': f'Nuevo responsable en {departamento}',
        'boton': 'Crear',
        'volver_url': reverse('errores:departamento_detalle', args=[departamento.pk]),
    })


def editar_responsable_departamento(request, departamento_pk, pk):
    departamento = get_object_or_404(Departamento, pk=departamento_pk)
    responsable = get_object_or_404(Responsable, pk=pk, departamento=departamento)
    if request.method == 'POST':
        form = ResponsableForm(request.POST, instance=responsable)
        if form.is_valid():
            responsable = form.save(commit=False)
            responsable.departamento = departamento
            responsable.save()
            messages.success(request, f'Responsable "{responsable}" actualizado.')
            return redirect('errores:departamento_detalle', pk=departamento.pk)
    else:
        form = ResponsableForm(instance=responsable)
    form.fields['departamento'].disabled = True
    return render(request, 'errores/plataforma/form.html', {
        'form': form,
        'titulo': f'Editar responsable: {responsable}',
        'boton': 'Guardar',
        'volver_url': reverse('errores:departamento_detalle', args=[departamento.pk]),
    })


def eliminar_responsable_departamento(request, departamento_pk, pk):
    departamento = get_object_or_404(Departamento, pk=departamento_pk)
    responsable = get_object_or_404(Responsable, pk=pk, departamento=departamento)
    if request.method == 'POST':
        nombre = str(responsable)
        responsable.delete()
        messages.success(request, f'Responsable "{nombre}" eliminado.')
        return redirect('errores:departamento_detalle', pk=departamento.pk)
    return render(request, 'errores/plataforma/confirm_delete.html', {
        'objeto': responsable,
        'tipo': 'responsable',
        'volver_url': reverse('errores:departamento_detalle', args=[departamento.pk]),
    })


def lista_pruebas(request):
    pruebas = Prueba.objects.all()
    return render(request, 'errores/catalogos/prueba_list.html', {
        'pruebas': pruebas,
    })


def crear_prueba(request):
    if request.method == 'POST':
        form = PruebaForm(request.POST)
        if form.is_valid():
            prueba = form.save()
            messages.success(request, f'Prueba "{prueba}" creada correctamente.')
            return redirect('errores:prueba_lista')
    else:
        form = PruebaForm()
    return render(request, 'errores/plataforma/form.html', {
        'form': form,
        'titulo': 'Nueva prueba',
        'boton': 'Crear',
        'volver_url': reverse('errores:prueba_lista'),
    })


def editar_prueba(request, pk):
    prueba = get_object_or_404(Prueba, pk=pk)
    if request.method == 'POST':
        form = PruebaForm(request.POST, instance=prueba)
        if form.is_valid():
            form.save()
            messages.success(request, f'Prueba "{prueba}" actualizada.')
            return redirect('errores:prueba_lista')
    else:
        form = PruebaForm(instance=prueba)
    return render(request, 'errores/plataforma/form.html', {
        'form': form,
        'titulo': f'Editar prueba: {prueba}',
        'boton': 'Guardar',
        'volver_url': reverse('errores:prueba_lista'),
    })


def eliminar_prueba(request, pk):
    prueba = get_object_or_404(Prueba, pk=pk)
    if request.method == 'POST':
        descripcion = str(prueba)
        prueba.delete()
        messages.success(request, f'Prueba "{descripcion}" eliminada.')
        return redirect('errores:prueba_lista')
    return render(request, 'errores/plataforma/confirm_delete.html', {
        'objeto': prueba,
        'tipo': 'prueba',
        'volver_url': reverse('errores:prueba_lista'),
    })


def lista_soluciones(request):
    q = request.GET.get('q', '').strip()
    soluciones = Solucion.objects.prefetch_related('asignaciones__responsable', 'asignaciones__departamento').all()

    if q:
        soluciones = soluciones.filter(
            Q(nombre__icontains=q)
            | Q(pasos__icontains=q)
            | Q(anexos__icontains=q)
            | Q(asignaciones__responsable__nombre__icontains=q)
            | Q(asignaciones__responsable__cargo__icontains=q)
            | Q(asignaciones__responsable__contacto__icontains=q)
            | Q(asignaciones__departamento__nombre__icontains=q)
        ).distinct()

    return render(request, 'errores/soluciones/solucion_list.html', {
        'soluciones': soluciones,
        'q': q,
    })


def crear_solucion(request):
    if request.method == 'POST':
        form = SolucionForm(request.POST)
        if form.is_valid():
            solucion = form.save()
            messages.success(request, f'Solucion "{solucion}" creada correctamente.')
            return redirect('errores:solucion_lista')
    else:
        form = SolucionForm()
    return render(request, 'errores/plataforma/form.html', {
        'form': form,
        'titulo': 'Nueva solucion',
        'boton': 'Crear',
        'volver_url': reverse('errores:solucion_lista'),
    })


@require_POST
def crear_solucion_rapida(request):
    form = SolucionRapidaForm(request.POST)
    if not form.is_valid():
        errors = {
            field: [error['message'] for error in field_errors]
            for field, field_errors in form.errors.get_json_data().items()
        }
        return JsonResponse({'ok': False, 'errors': errors}, status=400)

    solucion = form.save()
    return JsonResponse({
        'ok': True,
        'solucion': {
            'id': solucion.pk,
            'nombre': solucion.nombre,
        },
    })


def editar_solucion_rapida(request, pk):
    solucion = get_object_or_404(Solucion, pk=pk)

    if request.method == 'GET':
        return JsonResponse({
            'ok': True,
            'solucion': {
                'id': solucion.pk,
                'nombre': solucion.nombre,
                'pasos': solucion.pasos,
                'anexos': solucion.anexos,
                'responsables': list(solucion.asignaciones.filter(
                    responsable_id__isnull=False,
                    activo=True,
                ).values_list('responsable_id', flat=True)),
                'departamentos': list(solucion.asignaciones.filter(
                    departamento_id__isnull=False,
                    activo=True,
                ).values_list('departamento_id', flat=True)),
            },
        })

    if request.method != 'POST':
        return JsonResponse({'ok': False}, status=405)

    form = SolucionRapidaForm(request.POST, instance=solucion)
    if not form.is_valid():
        errors = {
            field: [error['message'] for error in field_errors]
            for field, field_errors in form.errors.get_json_data().items()
        }
        return JsonResponse({'ok': False, 'errors': errors}, status=400)

    solucion = form.save()
    return JsonResponse({
        'ok': True,
        'solucion': {
            'id': solucion.pk,
            'nombre': solucion.nombre,
        },
    })


def editar_solucion(request, pk):
    solucion = get_object_or_404(Solucion, pk=pk)
    if request.method == 'POST':
        form = SolucionForm(request.POST, instance=solucion)
        if form.is_valid():
            form.save()
            messages.success(request, f'Solucion "{solucion}" actualizada.')
            return redirect('errores:solucion_lista')
    else:
        form = SolucionForm(instance=solucion)
    return render(request, 'errores/plataforma/form.html', {
        'form': form,
        'titulo': f'Editar solucion: {solucion}',
        'boton': 'Guardar',
        'volver_url': reverse('errores:solucion_lista'),
    })


def eliminar_solucion(request, pk):
    solucion = get_object_or_404(Solucion, pk=pk)
    if request.method == 'POST':
        nombre = str(solucion)
        solucion.delete()
        messages.success(request, f'Solucion "{nombre}" eliminada.')
        return redirect('errores:solucion_lista')
    return render(request, 'errores/plataforma/confirm_delete.html', {
        'objeto': solucion,
        'tipo': 'solucion',
        'volver_url': reverse('errores:solucion_lista'),
    })
