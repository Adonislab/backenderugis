from django.shortcuts import render
from rest_framework.generics import GenericAPIView, RetrieveAPIView, ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .serializers import *
from .models import Task, CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status



class UserRegistrationAPIView(GenericAPIView):
    """
    API view pour l'inscription d'un nouvel utilisateur.

    Attributes:
        permission_classes (tuple): Les classes de permissions autorisées pour cette vue.
        serializer_class: La classe de sérialiseur utilisée pour valider et traiter les données d'inscription.
    """
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer
    
    def post(self, request, *args, **kwargs):
        """
        Gère la requête POST pour l'inscription d'un nouvel utilisateur.

        Args:
            request (Request): L'objet de requête HTTP.
            *args: Arguments positionnels supplémentaires.
            **kwargs: Arguments de mot-clé supplémentaires.

        Returns:
            Response: La réponse HTTP contenant les données de l'utilisateur nouvellement inscrit et les jetons d'accès et de rafraîchissement.

        Raises:
            ValidationError: Si les données d'inscription ne sont pas valides.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user)
        data = serializer.data
        data["tokens"] = {"refresh": str(token),
                          "access": str(token.access_token)}
        return Response(data, status=status.HTTP_201_CREATED)




class UserLoginAPIView(GenericAPIView):
    """
    API view pour l'authentification d'un utilisateur.

    Attributes:
        permission_classes (tuple): Les classes de permissions autorisées pour cette vue.
        serializer_class: La classe de sérialiseur utilisée pour valider et traiter les données de connexion.
    """
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer
    
    def post(self, request, *args, **kwargs):
        """
        Gère la requête POST pour l'authentification d'un utilisateur.

        Args:
            request (Request): L'objet de requête HTTP.
            *args: Arguments positionnels supplémentaires.
            **kwargs: Arguments de mot-clé supplémentaires.

        Returns:
            Response: La réponse HTTP contenant les données de l'utilisateur authentifié et les jetons d'accès et de rafraîchissement.

        Raises:
            ValidationError: Si les données de connexion ne sont pas valides.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        serializer = CustomUserSerializer(user)
        token = RefreshToken.for_user(user)
        data = serializer.data
        data["tokens"] = {"refresh": str(token),
                          "access": str(token.access_token)}
        return Response(data, status=status.HTTP_200_OK)
    



class UserLogoutAPIView(GenericAPIView):
    """
    API view pour la déconnexion d'un utilisateur.

    Attributes:
        permission_classes (tuple): Les classes de permissions autorisées pour cette vue.
    """
    permission_classes = (IsAuthenticated,)
    
    def post(self, request, *args, **kwargs):
        """
        Gère la requête POST pour la déconnexion d'un utilisateur.

        Args:
            request (Request): L'objet de requête HTTP.
            *args: Arguments positionnels supplémentaires.
            **kwargs: Arguments de mot-clé supplémentaires.

        Returns:
            Response: La réponse HTTP avec le statut de réussite de la déconnexion.

        Raises:
            KeyError: Si le jeton de rafraîchissement n'est pas fourni dans les données de la requête.
            Exception: Toute autre erreur interne inattendue lors de la déconnexion.
        """
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except KeyError:
            return Response({"error": "Refresh token not provided"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class UserInfoAPIView(ListAPIView):
    """
    API view pour obtenir des informations sur l'utilisateur.

    Attributes:
        permission_classes (tuple): Les classes de permissions autorisées pour cette vue.
        serializer_class: La classe de sérialiseur utilisée pour sérialiser les données de l'utilisateur.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomUserSerializer
    
    def get_queryset(self):
        """
        Obtient le queryset pour cette vue.

        Returns:
            Queryset: Le queryset contenant les utilisateurs à renvoyer dans la réponse.

        Notes:
            - Si l'utilisateur est du staff, renvoie tous les utilisateurs.
            - Sinon, filtre les utilisateurs pour l'utilisateur actuel.
        """
        # Récupérer l'utilisateur authentifié
        user = self.request.user
        # Si l'utilisateur est du staff, renvoyer tous les utilisateurs
        if user.is_staff:
            return CustomUser.objects.all()
        else:
            # Sinon, filtrer les utilisateurs pour l'utilisateur actuel
            return CustomUser.objects.filter(pk=user.pk)
    
 
    


class TaskAPIView(ListCreateAPIView):
    """
    API view pour la gestion des tâches.

    Attributes:
        serializer_class: La classe de sérialiseur utilisée pour sérialiser les données des tâches.
        permission_classes (tuple): Les classes de permissions autorisées pour cette vue.
    """
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Obtient le queryset pour cette vue.

        Returns:
            Queryset: Le queryset contenant les tâches à renvoyer dans la réponse.

        Notes:
            - Si l'utilisateur est du staff, renvoie toutes les tâches.
            - Sinon, filtre les tâches pour l'utilisateur actuel.
        """
        # Récupérer l'utilisateur authentifié
        user = self.request.user
        # Si l'utilisateur est du staff, renvoyer toutes les tâches
        if user.is_staff:
            queryset = Task.objects.all()
        else:
            # Sinon, filtrer les tâches pour l'utilisateur actuel
            queryset = Task.objects.filter(user=user)
        return queryset

    def perform_create(self, serializer):
        """
        Exécute la création d'une nouvelle tâche.

        Args:
            serializer: Le sérialiseur contenant les données de la nouvelle tâche.

        Notes:
            - Associe automatiquement la nouvelle tâche à l'utilisateur actuel.
        """
        serializer.save(user=self.request.user)
        
        


class TaskDetailAPIView(ListAPIView):
    """
    API view pour obtenir les détails des tâches d'un utilisateur.

    Attributes:
        permission_classes (tuple): Les classes de permissions autorisées pour cette vue.
        serializer_class: La classe de sérialiseur utilisée pour sérialiser les données des tâches.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = TaskSerializer
    
    def get_queryset(self):
        """
        Obtient le queryset pour cette vue.

        Returns:
            Queryset: Le queryset contenant les détails des tâches à renvoyer dans la réponse.

        Notes:
            - Si l'utilisateur est du staff, renvoie toutes les tâches.
            - Sinon, filtre les tâches pour l'utilisateur actuel.
        """
        # Récupérer l'ID de l'utilisateur à partir des paramètres d'URL
        user_id = self.request.user.id
        # Si l'utilisateur est du staff, renvoyer toutes les tâches
        if self.request.user.is_staff:
            queryset = Task.objects.all()
        else:
            # Sinon, filtrer les tâches pour l'utilisateur avec l'ID spécifié
            queryset = Task.objects.filter(user_id=user_id)
        return queryset



class TaskDetailModifiactionAPIView(RetrieveUpdateDestroyAPIView):
    """
    API view pour récupérer, mettre à jour et supprimer une tâche spécifique.

    Attributes:
        permission_classes (tuple): Les classes de permissions autorisées pour cette vue.
        serializer_class: La classe de sérialiseur utilisée pour sérialiser les données des tâches.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = TaskSerializer
    
    def get_queryset(self):
        """
        Obtient le queryset pour cette vue.

        Returns:
            Queryset: Le queryset contenant la tâche spécifique à récupérer, mettre à jour ou supprimer.

        Notes:
            - Si l'utilisateur est du staff, renvoie toutes les tâches.
            - Sinon, filtre les tâches pour l'utilisateur avec l'ID spécifié.
        """
        # Récupérer l'ID de l'utilisateur à partir des paramètres d'URL
        user_id = self.request.user.id
        # Si l'utilisateur est du staff, renvoyer toutes les tâches
        if self.request.user.is_staff:
            queryset = Task.objects.all()
        else:
            # Sinon, filtrer les tâches pour l'utilisateur avec l'ID spécifié
            queryset = Task.objects.filter(user_id=user_id)
        return queryset
