from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    
    def __str__(self) -> str:
        """
        Retourne une représentation textuelle de l'objet CustomUser.

        Returns:
            str: L'email de l'utilisateur.
        """
        return self.email



class Task(models.Model):
    """
    Modèle représentant une tâche assignée à un utilisateur.

    Attributes:
        user (User): L'utilisateur auquel la tâche est assignée.
        title (str): Le titre de la tâche.
        description (str, optional): La description de la tâche (optionnelle).
        completed (bool): Indique si la tâche est terminée ou non.
        favoris (bool): Indique si la tâche est marquée comme favorite.
        created_at (datetime): Date et heure de création de la tâche.
        updated_at (datetime): Date et heure de la dernière mise à jour de la tâche.
    """
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)    
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    favoris = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Retourne une représentation textuelle de l'objet Task.

        Returns:
            str: Le titre de la tâche.
        """
        return self.title

    
    
    
