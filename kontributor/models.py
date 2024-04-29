from django.db import models

# Create your models here.

class Kontributor(models.Model):
    nama = models.CharField(max_length=100)
    tipe = models.CharField(max_length=100)
    jenis_kelamin = models.CharField(max_length=50)
    kewarganegaraan = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nama
