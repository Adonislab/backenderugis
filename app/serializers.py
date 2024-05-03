from .models import CustomUser, Task
from rest_framework import serializers
from django.contrib.auth import authenticate


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer pour convertir les objets CustomUser en représentations JSON.

    Attributes:
        model (CustomUser): Le modèle utilisé pour sérialiser les données.
        fields (tuple): Les champs à inclure dans la sérialisation.
    """
    class Meta:
        """
        Méta-classe pour définir les propriétés du sérialiseur.

        Attributes:
            model (CustomUser): Le modèle à sérialiser.
            fields (tuple): Les champs à inclure dans la sérialisation.
        """
        model = CustomUser
        fields = ("id", "username", "email")



class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer pour l'inscription des utilisateurs.

    Attributes:
        password1 (str): Champ pour le premier mot de passe (écrit uniquement).
        password2 (str): Champ pour la confirmation du mot de passe (écrit uniquement).
        model (CustomUser): Le modèle utilisé pour sérialiser les données.
        fields (tuple): Les champs à inclure dans la sérialisation.
        extra_kwargs (dict): Options supplémentaires pour les champs.
    """
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        """
        Méta-classe pour définir les propriétés du sérialiseur.

        Attributes:
            model (CustomUser): Le modèle à sérialiser.
            fields (tuple): Les champs à inclure dans la sérialisation.
            extra_kwargs (dict): Options supplémentaires pour les champs.
        """
        model = CustomUser
        fields = ("id", "username", "email", "password1", "password2")
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        """
        Valide les données saisies par l'utilisateur lors de l'inscription.

        Args:
            attrs (dict): Les données entrées par l'utilisateur.

        Returns:
            dict: Les données validées.
        
        Raises:
            serializers.ValidationError: Si les mots de passe ne correspondent pas ou si le mot de passe est trop court.
        """
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas!")

        password = attrs.get("password1", "")
        if len(password) < 8:
            raise serializers.ValidationError(
                "Le mot de passe doit être d'au moins huit caractères!")

        return attrs

    def create(self, validated_data):
        """
        Crée un nouvel utilisateur à partir des données validées.

        Args:
            validated_data (dict): Les données validées.

        Returns:
            CustomUser: L'utilisateur créé.
        """
        password = validated_data.pop("password1")
        validated_data.pop("password2")

        return CustomUser.objects.create_user(password=password, **validated_data)




class UserLoginSerializer(serializers.Serializer):
    """
    Serializer pour l'authentification des utilisateurs.

    Attributes:
        email (str): Champ pour l'email de l'utilisateur.
        password (str): Champ pour le mot de passe de l'utilisateur (écrit uniquement).
    """
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        """
        Valide les données saisies par l'utilisateur lors de la connexion.

        Args:
            data (dict): Les données entrées par l'utilisateur.

        Returns:
            User: L'utilisateur authentifié.

        Raises:
            serializers.ValidationError: Si les identifiants de l'utilisateur sont incorrects.
        """
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Vos identifiants sont incorrects!")

    
class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer pour convertir les objets Task en représentations JSON.

    Attributes:
        model (Task): Le modèle utilisé pour sérialiser les données.
        fields (tuple): Les champs à inclure dans la sérialisation.
    """
    class Meta:
        """
        Méta-classe pour définir les propriétés du sérialiseur.

        Attributes:
            model (Task): Le modèle à sérialiser.
            fields (tuple): Les champs à inclure dans la sérialisation.
        """
        model = Task
        fields = ("id", "title", "description", "completed", "favoris")
       