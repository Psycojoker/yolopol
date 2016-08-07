from rest_framework import (
    filters,
    viewsets,
)

from rql_filter.backend import RQLFilterBackend

from representatives.api import DefaultWebPagination

from .models import (
    DossierScore,
    Recommendation,
    RepresentativeScore,
    VoteScore
)

from .serializers import (
    DossierScoreSerializer,
    RecommendationSerializer,
    RepresentativeScoreSerializer,
    VoteScoreSerializer
)


class DossierScoreViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint to view representative score contribution for each dossier
    """
    queryset = DossierScore.objects.all()
    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        RQLFilterBackend
    )
    filter_fields = {
        'id': ['exact'],
        'dossier': ['exact'],
        'representative': ['exact'],
        'score': ['exact', 'gte', 'lte']
    }
    search_fields = ('dossier', 'representative')
    ordering_fields = ('representative', 'dossier')
    pagination_class = DefaultWebPagination
    serializer_class = DossierScoreSerializer


class RecommendationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows recommendations to be viewed.
    """
    queryset = Recommendation.objects.select_related('proposal')
    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        RQLFilterBackend
    )
    filter_fields = {
        'id': ['exact'],
        'recommendation': ['exact'],
        'title': ['exact', 'icontains'],
        'description': ['exact', 'icontains'],
        'weight': ['exact', 'gte', 'lte']
    }
    search_fields = ('title', 'description')
    ordering_fields = ('id', 'weight', 'title')
    pagination_class = DefaultWebPagination
    serializer_class = RecommendationSerializer


class RepresentativeScoreViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint to view representative scores
    """
    queryset = RepresentativeScore.objects.select_related('representative')
    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        RQLFilterBackend
    )
    filter_fields = {
        'representative': ['exact'],
        'score': ['exact', 'gte', 'lte']
    }
    search_fields = ('representative', 'score')
    ordering_fields = ('representative', 'score')
    pagination_class = DefaultWebPagination
    serializer_class = RepresentativeScoreSerializer


class VoteScoreViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint to view votes with their score impact.
    This endpoint only shows votes that have a matching recommendation.
    """
    queryset = VoteScore.objects.select_related(
        'representative',
        'proposal',
        'proposal__dossier',
        'proposal__recommendation'
    ).filter(
        proposal__recommendation__isnull=False
    )

    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        RQLFilterBackend
    )

    filter_fields = {
        'representative': ['exact'],
        'proposal': ['exact'],
        'proposal__dossier': ['exact']
    }

    pagination_class = DefaultWebPagination
    serializer_class = VoteScoreSerializer
