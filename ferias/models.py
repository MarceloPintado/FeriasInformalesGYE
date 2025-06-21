from django.db import models

# Create your models here.
class Feria(models.Model):
    HORARIO_CHOICES = [
        ('manana', 'Mañana'),
        ('tarde', 'Tarde'),
        ('completo', 'Completo'),
    ]
    
    TIPO_FERIA_CHOICES = [
        ('artesanias', 'Artesanías'),
        ('alimentos', 'Alimentos'),
        ('ropa', 'Ropa'),
        ('mixto', 'Mixto'),
        ('otros', 'Otros'),
    ]
    
    ESTADO_CHOICES = [
        ('programada', 'Programada'),
        ('en_curso', 'En curso'),
        ('finalizada', 'Finalizada'),
        ('cancelada', 'Cancelada'),
    ]
    
    FORMA_INSCRIPCION_CHOICES = [
        ('presencial', 'Presencial'),
        ('online', 'Online'),
        ('ambos', 'Ambos'),
    ]
    
    SERVICIOS_CHOICES = [
        ('electricidad', 'Electricidad'),
        ('agua', 'Agua'),
        ('seguridad', 'Seguridad'),
        ('otros', 'Otros'),
    ]
    
    # Campos del modelo
    id_feria = models.CharField(max_length=50, unique=True, verbose_name="ID de la Feria")
    nombre_feria = models.CharField(max_length=200, verbose_name="Nombre de la Feria")
    fecha_inicio = models.DateField(verbose_name="Fecha de Inicio")
    fecha_fin = models.DateField(verbose_name="Fecha de Fin")
    horario = models.CharField(max_length=20, choices=HORARIO_CHOICES, verbose_name="Horario")
    ubicacion = models.CharField(max_length=200, verbose_name="Ubicación / Zona")
    capacidad = models.IntegerField(verbose_name="Capacidad Máxima")
    tipo_feria = models.CharField(max_length=20, choices=TIPO_FERIA_CHOICES, verbose_name="Tipo de Feria")
    costo_participacion = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Costo Participación (USD)")
    responsable = models.CharField(max_length=100, verbose_name="Responsable")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, verbose_name="Estado")
    fecha_limite = models.DateField(null=True, blank=True, verbose_name="Fecha Límite Inscripción")
    forma_inscripcion = models.CharField(max_length=20, choices=FORMA_INSCRIPCION_CHOICES, null=True, blank=True, verbose_name="Forma de Inscripción")
    num_permisos = models.IntegerField(null=True, blank=True, verbose_name="# Permisos Emitidos")
    servicios = models.CharField(max_length=200, blank=True, verbose_name="Servicios Disponibles")
    normas = models.TextField(blank=True, verbose_name="Requisitos / Normas")
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    
    # Campos automáticos
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Feria"
        verbose_name_plural = "Ferias"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.nombre_feria} ({self.id_feria})"
