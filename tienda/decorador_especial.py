from django.shortcuts import redirect
from django.contrib import messages


def login_requerido(vista):
    def nueva_funcion(request):
        logueo = request.session.get("logueo", False)
        # Autenticación y Autorización, ejemplo para administradores
        if logueo and logueo["rol"] == 1:
            c = vista(request)
            return c
        else:
            messages.info(request, "No está autorizado.")
            return redirect("index")

    return nueva_funcion

def login_requerido_id(vista):
    def nueva_funcion(request, id):
        logueo = request.session.get("logueo", False)
        # Autenticación y Autorización, ejemplo para administradores
        if logueo and logueo["rol"] == 1:
            c = vista(request, id)
            return c
        else:
            if request.GET.get('next'):
                return HttpResponseRedirect(reverse('index')+f"?next{request.GET.get('next')}") 
            else:
                messages.info(request, "No está autorizado.")
                return redirect("index")

    return nueva_funcion

