import graphene
from graphene_django.fields import DjangoConnectionField
from graphene_django.types import DjangoObjectType

from .models import ShortURL


class ShortURLType(DjangoObjectType):

    class Meta:
        model = ShortURL


class Query(graphene.ObjectType):
    shorturl = graphene.Field(ShortURLType,
                              code=graphene.String())

    all_shorturls = graphene.List(ShortURLType)

    def resolve_all_shorturls(self, info, **kwargs):
        return ShortURL.objects.all()

    def resolve_shorturl(self, info, **kwargs):
        code = kwargs.get('code')
        shorturl = None
        if code is not None:
            try:
                shorturl = ShortURL.objects.get(code=code)
            except ShortURL.DoesNotExist as e:
                pass
        return shorturl


schema = graphene.Schema(query=Query)
