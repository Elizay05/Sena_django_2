from django.db import models

# Create your models here.
class Categoria(models.Model):
	nombre = models.CharField(max_length=254)
	descripcion = models.TextField()

	def __str__(self):
		return self.nombre


class Producto(models.Model):
	nombre = models.CharField(max_length=254, unique=True)
	precio = models.FloatField()
	inventario = models.IntegerField()
	fecha_creacion = models.DateField()
	categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
	foto = models.ImageField(upload_to="fotos_productos/", default="fotos_productos/default.png")

	def __str__(self):
		return self.nombre


class Usuario(models.Model):
	nombre = models.CharField(max_length=254)
	correo = models.EmailField(max_length=254, unique=True)
	clave = models.CharField(max_length=254)
	ROLES = (
		(1, "Administrador"),
		(2, "Despachador"),
		(3, "Cliente"),
	)
	rol = models.IntegerField(choices=ROLES, default=3)
	foto = models.ImageField(upload_to="fotos/")

	def __str__(self):
		return self.nombre

