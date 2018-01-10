import graphene
from graphene_django.fields import DjangoConnectionField
from graphene_django.types import DjangoObjectType
from django.core.exceptions import ValidationError

from .models import ShortURL


class ShortURLType(DjangoObjectType):

    class Meta:
        model = ShortURL


class CreateShortURL(graphene.Mutation):
    class Arguments:
        long_url = graphene.String(required=True)

    ok = graphene.Boolean()
    url_with_code = graphene.String()
    shorturl = graphene.Field(lambda: ShortURLType)

    def mutate(self, info, long_url):
        shorturl = ShortURL(long_url=long_url)
        shorturl.full_clean(exclude=('code',))
        shorturl.save()
        url_with_code = 'http://localhost/'+shorturl.code
        ok = True
        return CreateShortURL(shorturl=shorturl, url_with_code=url_with_code, ok=ok)



class ShortURLQuery(graphene.ObjectType):
    get_shorturl = graphene.Field(ShortURLType,
                              code=graphene.String())

    all_shorturls = graphene.List(ShortURLType)

    def resolve_all_shorturls(self, info, **kwargs):
        return ShortURL.objects.all()

    def resolve_get_shorturl(self, info, **kwargs):
        code = kwargs.get('code')
        shorturl = None
        if code is not None:
            try:
                shorturl = ShortURL.objects.get(code=code)
            except ShortURL.DoesNotExist as e:
                pass
        return shorturl


class ShortURLMutations(graphene.ObjectType):
    create_shorturl = CreateShortURL.Field()

schema = graphene.Schema(query=ShortURLQuery, mutation=ShortURLMutations)
