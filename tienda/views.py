from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError, transaction

# Para tomar el from desde el settings
from django.conf import settings
from django.core.mail import BadHeaderError, EmailMessage

# Importamos todos los modelos de la base de datos
from .models import *

# Create your views here.

def index(request):
	logueo = request.session.get("logueo", False)

	if logueo == False:
		next = request.GET.get("next")
		contexto = {"next": next}
		return render(request, "tienda/login/login.html", contexto)
	else:
		return redirect("inicio")


def login(request):
	if request.method == "POST":
		user = request.POST.get("correo")
		passw = request.POST.get("clave")
		# select * from Usuario where correo = "user" and clave = "passw"
		try:
			q = Usuario.objects.get(correo=user, clave=passw)
			# Crear variable de sesión
			request.session["logueo"] = {
				"id": q.id,
				"nombre": q.nombre,
				"rol": q.rol,
				"nombre_rol": q.get_rol_display()
			}
			request.session["carrito"] = []
			request.session["items"] = 0
			messages.success(request, f"Bienvenido {q.nombre}!!")
			if request.GET.get('next'):
				return HttpResponseRedirect(request.GET.get('next'))
			else:
				return redirect("inicio")
		except Exception as e:
			messages.error(request, "Error: Usuario o contraseña incorrectos...")
			return redirect("index")
	else:
		messages.warning(request, "Error: No se enviaron datos...")
		return redirect("index")


def logout(request):
	try:
		del request.session["logueo"]
		del request.session["carrito"]
		messages.success(request, "Sesión cerrada correctamente!")
		return redirect("index")
	except Exception as e:
		messages.warning(request, "No se pudo cerrar sesión...")
		return redirect("inicio")


def inicio(request):
	logueo = request.session.get("logueo", False)

	if logueo:
		categorias = Categoria.objects.all()

		cat = request.GET.get("cat")
		if cat == None:
			productos = Producto.objects.all()
		else:
			c = Categoria.objects.get(pk=cat)
			productos = Producto.objects.filter(categoria=c)

		contexto = {"data": productos, "cat": categorias}
		return render(request, "tienda/inicio.html", contexto)
	else:
		return redirect("index")


from .decorador_especial import *


@login_requerido
def categorias(request):
	q = Categoria.objects.all()
	contexto = {"data": q}
	return render(request, "tienda/categorias/categorias.html", contexto)



def categorias_form(request):
	return render(request, "tienda/categorias/categorias_form.html")


def categorias_crear(request):
	if request.method == "POST":
		nomb = request.POST.get("nombre")
		desc = request.POST.get("descripcion")
		try:
			q = Categoria(
				nombre=nomb,
				descripcion=desc
			)
			q.save()
			messages.success(request, "Guardado correctamente!!")
		except Exception as e:
			messages.error(request, f"Error: {e}")
		return redirect("categorias_listar")

	else:
		messages.warning(request, "Error: No se enviaron datos...")
		return redirect("categorias_listar")


def categorias_eliminar(request, id):
	try:
		q = Categoria.objects.get(pk=id)
		q.delete()
		messages.success(request, "Categoría eliminada correctamente!!")
	except Exception as e:
		messages.error(request, f"Error: {e}")

	return redirect("categorias_listar")


def categorias_formulario_editar(request, id):
	q = Categoria.objects.get(pk=id)
	contexto = {"data": q}
	return render(request, "tienda/categorias/categorias_formulario_editar.html", contexto)

def categorias_actualizar(request):
	if request.method == "POST":
		id = request.POST.get("id")
		nomb = request.POST.get("nombre")
		desc = request.POST.get("descripcion")
		try:
			q = Categoria.objects.get(pk=id)
			q.nombre = nomb
			q.descripcion = desc
			q.save()
			messages.success(request, "Categoría actualizada correctamente!!")
		except Exception as e:
			messages.error(request, f"Error: {e}")
	else:
		messages.warning(request, "Error: No se enviaron datos...")

	return redirect("categorias_listar")


@login_requerido
def productos(request):
	q = Producto.objects.all()
	contexto = {"data": q}
	return render(request, "tienda/productos/productos.html", contexto)


def productos_form(request):
	q = Categoria.objects.all()
	contexto = {"data": q}
	return render(request, "tienda/productos/productos_form.html", contexto)


def productos_crear(request):
	if request.method == "POST":
		nombre = request.POST.get("nombre")
		precio = request.POST.get("precio")
		inventario = request.POST.get("inventario")
		fecha_creacion = request.POST.get("fecha_creacion")
		categoria = Categoria.objects.get(pk=request.POST.get("categoria"))
		try:
			q = Producto(
				nombre=nombre,
				precio=precio,
				inventario=inventario,
				fecha_creacion=fecha_creacion,
				categoria=categoria
			)
			q.save()
			messages.success(request, "Guardado correctamente!!")
		except Exception as e:
			messages.error(request, f"Error: {e}")
		return redirect("productos_listar")

	else:
		messages.warning(request, "Error: No se enviaron datos...")
		return redirect("productos_listar")


def productos_eliminar(request, id):
	try:
		q = Producto.objects.get(pk=id)
		q.delete()
		messages.success(request, "Producto eliminada correctamente!!")
	except Exception as e:
		messages.error(request, f"Error: {e}")

	return redirect("productos_listar")


def productos_formulario_editar(request, id):
	q = Producto.objects.get(pk=id)
	c = Categoria.objects.all()
	contexto = {"data": q, "categoria": c}
	return render(request, "tienda/productos/productos_formulario_editar.html", contexto)

def productos_actualizar(request):
	if request.method == "POST":
		id = request.POST.get("id")
		nombre = request.POST.get("nombre")
		precio = request.POST.get("precio")
		inventario = request.POST.get("inventario")
		fecha_creacion = request.POST.get("fecha_creacion")
		categoria = Categoria.objects.get(pk=request.POST.get("categoria"))
		try:
			q = Producto.objects.get(pk=id)
			q.nombre = nombre
			q.precio = precio
			q.inventario = inventario
			q.fecha_creacion = fecha_creacion
			q.categoria = categoria
			q.save()
			messages.success(request, "Producto actualizado correctamente!!")
		except Exception as e:
			messages.error(request, f"Error: {e}")
	else:
		messages.warning(request, "Error: No se enviaron datos...")

	return redirect("productos_listar")


def ver_perfil(request):
	logueo = request.session.get("logueo", False)
	# Consultamos en DB por el ID del usuario logueado....
	q = Usuario.objects.get(pk=logueo["id"])
	contexto = {"data": q}
	return render(request, "tienda/login/perfil.html", contexto)


def cambio_clave_formulario(request):
	return render(request, "tienda/login/cambio_clave.html")


def cambiar_clave(request):
	if request.method == "POST":
		logueo = request.session.get("logueo", False)
		q = Usuario.objects.get(pk=logueo["id"])

		c1 = request.POST.get("nueva1")
		c2 = request.POST.get("nueva2")

		if q.clave == request.POST.get("clave"):
			if c1 == c2:
				# cambiar clave en DB
				q.clave = c1
				q.save()
				messages.success(request, "Contraseña guardada correctamente!!")
			else:
				messages.info(request, "Las contraseñas nuevas no coinciden...")
		else:
			messages.error(request, "Contraseña no válida...")
	else:
		messages.warning(request, "Error: No se enviaron datos...")

	return redirect('cc_formulario')


def carrito_add(request):
	if request.method == "POST":
		try:
			carrito = request.session.get("carrito", False)
			if not carrito:
				request.session["carrito"] = []
				request.session["items"] = 0
				carrito = []

			id_producto = int(request.POST.get("id"))
			cantidad = request.POST.get("cantidad")
			# Consulto el producto en DB...........................
			q = Producto.objects.get(pk=id_producto)
			for p in carrito:
				if p["id"] == id_producto:
					if q.inventario >= (p["cantidad"] + int(cantidad)) and int(cantidad) > 0:
						p["cantidad"] += int(cantidad)
						p["subtotal"] = p["cantidad"] * q.precio
					else:
						print("Cantidad supera inventario...")
						messages.warning(request, "Cantidad supera inventario...")
					break
			else:
				print("No existe en carrito... lo agregamos")
				if q.inventario >= int(cantidad) and int(cantidad) > 0:
					carrito.append(
						{
							"id": q.id,
							"foto": q.foto.url,
							"producto": q.nombre,
							"precio": q.precio,
							"cantidad": int(cantidad),
							"subtotal": int(cantidad) * q.precio
						}
					)
				else:
					print("Cantidad supera inventario...")
					messages.warning(request, "No se puede agregar, no hay suficiente inventario.")

			# Actualizamos variable de sesión carrito...
			request.session["carrito"] = carrito

			contexto = {
				"items": len(carrito),
				"total": sum(p["subtotal"] for p in carrito)
			}
			request.session["items"] = len(carrito)

			return render(request, "tienda/carrito/carrito.html", contexto)
		except ValueError as e:
			messages.error(request, f"Error: Digite un valor correcto para cantidad")
			return HttpResponse("Error")
		except Exception as e:
			messages.error(request, f"Ocurrió un Error: {e}")
			return HttpResponse("Error")
	else:
		messages.warning(request, "No se enviaron datos.")
		return HttpResponse("Error")


def carrito_ver(request):
	carrito = request.session.get("carrito", False)
	if not carrito:
		request.session["carrito"] = []
		request.session["items"] = 0
		contexto = {
			"items": 0,
			"total": 0
		}
	else:
		contexto = {
			"items": len(carrito),
			"total": sum(p["subtotal"] for p in carrito)
		}
		request.session["items"] = len(carrito)

	return render(request, "tienda/carrito/carrito.html", contexto)

def carrito_eliminar(request, id):
	carrito = request.session.get("carrito", False)
	for p in carrito:
		if p["id"] == id:
			carrito.remove(p)
			request.session["carrito"] = carrito
			request.session["items"] = len(carrito)
	return redirect('carrito_ver')

def vaciar_carrito(request):
	request.session["carrito"] = []
	request.session["items"] = []
	return redirect('inicio')

def actualizar_totales_carrito(request, id_producto):
	carrito = request.session.get("carrito", False)
	cantidad = request.GET.get("cantidad")

	if carrito != False:
		for i, item in enumerate(carrito):
			if item["id"] == id_producto:
				item["cantidad"] = int(cantidad)
				item["subtotal"] = int(cantidad) * item["precio"]
				break
		else:
			messages.warning(request, "No se encontró el ítem en el carrito.")

	request.session["items"] = len(carrito)
	request.session["carrito"] = carrito
	return redirect("carrito_ver")


@transaction.atomic
def crear_venta(request):
	carrito = request.session.get("carrito", False)
	logueo = request.session.get("logueo", False)
	try:
		# Genero encabezado de venta, para tener ID y guardar detalle
		r = Venta(usuario=Usuario.objects.get(pk=logueo["id"]))
		r.save()

		for i, p in enumerate(carrito):
			try:
				pro = Producto.objects.get(pk=p["id"])
				print(f"ok producto {p['producto']}")
			except Producto.DoesNotExist:
				# elimino el producto no existente del carrito...
				carrito.pop(i)
				request.session["carrito"] = carrito
				request.session["items"] = len(carrito)
				raise Exception(f"El producto '{p['producto']}' ya no existe")

			if int(p["cantidad"]) > pro.inventario:
				raise Exception(f"La cantidad del producto '{p['producto']}' supera el inventario")

			det = DetalleVenta(
				venta=r,
				producto=pro,
				cantidad=int(p["cantidad"]),
				precio_historico=int(p["precio"])
			)
			det.save()
			if not prueba_correo(r.id):
				raise Exception ("Error al enviar correo.")
	except Exception as e:
		transaction.set_rollback(True)
		messages.error(request, f"Error: {e}")

	return redirect("inicio")


def ver_ventas(request):
	logueo = request.session.get("logueo")
	user = Usuario.objects.get(pk=logueo["id"])

	if user.rol == 3:
		venta = Venta.objects.filter(usuario=user)
		contexto = {"data":venta}
		return render(request, "tienda/carrito/ventas.html", contexto)
	else:
		venta = Venta.objects.all()
		contexto = {"data":venta}
		return render(request, "tienda/carrito/ventas.html", contexto)


@login_requerido_id
def ver_detalles(request, id):
	venta = Venta.objects.get(pk=id) 
	detalles = DetalleVenta.objects.filter(venta=venta.id)
	contexto = {"data":detalles}
	return render(request, "tienda/carrito/detalles.html", contexto)


def prueba_correo(id):
	destinatario = "sayiis2005@gmail.com"
	mensaje = f"""
		<h1 style='color:blue;'>Tienda virtual</h1>
		<p>Su pedido está listo y en estado "creado".</p>
		<a href='http://127.0.0.1:8000/tienda/detalle_venta/{id}/?next=tienda/detalle_venta/{id}/'>Detalles de la venta</a>
		<p>Tienda ADSO, 2024</p>
		"""
	try:
		msg = EmailMessage("Tienda ADSO", mensaje, settings.EMAIL_HOST_USER, [destinatario])
		msg.content_subtype = "html"  # Habilitar contenido html
		msg.send()
		return HttpResponse("Correo enviado")
	except BadHeaderError:
		return HttpResponse("Encabezado no válido")
	except Exception as e:
		return HttpResponse(f"Error: {e}")




	




		
		





	



