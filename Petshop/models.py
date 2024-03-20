from django.db import models

class Animal(models.Model):
    id = models.IntegerField(primary_key=True)
    tipo = models.CharField(max_length=20)
    raca = models.CharField(max_length=20)
    idade = models.SmallIntegerField()
    adotado = models.BooleanField()

    def __str__(self):
        return f"ID: {self.id}, Tipo: {self.tipo}, Raça: {self.raca}, Idade: {self.idade}, Adotado: {self.adotado}"
