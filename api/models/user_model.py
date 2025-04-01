from django.db import models


class User(models.Model):
    """
    Modelo para representar usuarios en la aplicación.
    
    Nota: En un BFF típico, este modelo podría ser solo una representación
    de los datos que vienen del backend, no necesariamente una entidad
    que se persiste en la base de datos local.
    """
    
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        """Meta clase para el modelo User"""
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"
        ordering = ['-date_joined']
    
    def __str__(self):
        """Representación en string del modelo"""
        return self.username