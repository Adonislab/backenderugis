from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """
    Formulaire de création personnalisé pour les utilisateurs.

    Attributes:
        model (CustomUser): Le modèle utilisé pour créer l'utilisateur.
        fields (tuple): Les champs à inclure dans le formulaire de création.
    """
    class Meta(UserCreationForm.Meta):
        """
        Méta-classe pour définir les propriétés du formulaire.

        Attributes:
            model (CustomUser): Le modèle à utiliser dans le formulaire.
            fields (tuple): Les champs à inclure dans le formulaire.
        """
        model = CustomUser
        fields = ("email",)

class CustomUserChangeForm(UserChangeForm):
    """
    Formulaire de modification personnalisé pour les utilisateurs.

    Attributes:
        model (CustomUser): Le modèle utilisé pour modifier l'utilisateur.
        fields (tuple): Les champs à inclure dans le formulaire de modification.
    """
    class Meta:
        """
        Méta-classe pour définir les propriétés du formulaire.

        Attributes:
            model (CustomUser): Le modèle à utiliser dans le formulaire.
            fields (tuple): Les champs à inclure dans le formulaire.
        """
        model = CustomUser
        fields = ("email",)

            
          