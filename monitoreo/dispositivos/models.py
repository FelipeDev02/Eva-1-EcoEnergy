from django.db import models

# Create your models here.
class BaseModel(models.Model):
    ESTADOS = [
        ("ACTIVO", "Activo"),
        ("INACTIVO", "Inactivo"),
    ]

    estado = models.CharField(max_length=10, choices=ESTADOS, default="ACTIVO")
    created_at = models.DateTimeField(auto_now_add=True)  # se asigna al crear
    updated_at = models.DateTimeField(auto_now=True)  # se actualiza cada vez que se guarda
    deleted_at = models.DateTimeField(null=True, blank=True)  # opcional para borrado lógico

    class Meta:
        abstract = True  # no crea tabla, solo se hereda

class Organization(BaseModel):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Zone(BaseModel):
    name = models.CharField(max_length=100)
    id_org = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Category(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Device(BaseModel):
    name = models.CharField(max_length=100)
    id_zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    id_cat = models.ForeignKey(Category, on_delete=models.CASCADE)
    id_prod = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Measurement(BaseModel):
    name = models.CharField(max_length=100)
    id_prod = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Alert(BaseModel):
    alert_type = models.CharField(max_length=100)
    severity = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.alert_type} ({self.severity})"
    
class AlertProduct(BaseModel):
    id_alert = models.ForeignKey(Alert, on_delete=models.CASCADE)
    id_prod = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"Alerta '{self.id_alert.alert_type}' sobre '{self.id_prod.name}'"