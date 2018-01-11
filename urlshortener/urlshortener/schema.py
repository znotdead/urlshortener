import graphene

from shorturl import schema


class QueryRoot(schema.ShortURLQuery, graphene.ObjectType):
    pass


class MutationRoot(schema.ShortURLMutations, graphene.ObjectType):
    pass


schema = graphene.Schema(query=QueryRoot, mutation=MutationRoot)
