from django.db import models
from django_resized import ResizedImageField


# Create your models here.

class UserCadastrados(models.Model):
    nome_user = models.CharField(max_length=30)
    imagem_vinculada_user = ResizedImageField(size=[480, 480], quality=100, upload_to='media/', force_format='PNG',
                                              blank=True,
                                              null=True)

    def __str__(self):
        return self.nome_user

