import graphene
from graphene_django import DjangoObjectType
from app.models import Contact
from graphql_auth.schema import UserQuery
from graphql_auth import mutations


class ContactType(DjangoObjectType):
    # Describe the data is to be formatted into GraphQL fields
    class Meta:
        model = Contact
        fields = "__all__"


class Query(UserQuery,graphene.ObjectType):
    # Query ContactType to get list of contacts
    list_contacts = graphene.List(ContactType)
    read_contact = graphene.Field(ContactType, id=graphene.Int())

    def resolve_list_contacts(root, info):
        return Contact.objects.all()

    def resolve_read_contact(root, info, id):
        return Contact.objects.get(id=id)


class ContactMutation(graphene.Mutation):
    class Arguments:
        # Add fields you would like to create. This will corelate with the ContactType fields above
        id = graphene.ID()
        name = graphene.String()
        email = graphene.String()
        phone = graphene.String()
        message = graphene.String()

    # Define the class we are getting the fields from
    contact = graphene.Field(ContactType)

    @classmethod
    def mutate(cls, root, info, name, email, phone, message):
        # function that will save the data
        ######## CREATE ########
        contact = Contact(name=name, email=email, phone=phone, message=message)
        contact.save()


class ContactMutationUpdate(graphene.Mutation):
    class Arguments:
        # Add fields you would like to create. This will corelate with the ContactType fields above
        id = graphene.ID()
        name = graphene.String()
        email = graphene.String()
        phone = graphene.String()
        message = graphene.String()

    # Define the class we are getting the fields from
    contact = graphene.Field(ContactType)

    @classmethod
    def mutate(cls, root, info, id, name, email, phone, message):
        ######## UPDATE ########
        get_contact = Contact.objects.get(id=id)
        get_contact.name = name
        get_contact.email = email
        get_contact.phone = phone
        get_contact.message = message
        get_contact.save()
        return ContactMutation(contact=get_contact)


class ContactDelete(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    contact = graphene.Field(ContactType)

    @classmethod
    def mutate(cls, root, info, id):
        contact = Contact(id=id)
        contact.delete()


class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()  # predefined settings to register user
    verify_account = mutations.VerifyAccount.Field()  # used to verify account
    token_auth = mutations.ObtainJSONWebToken.Field()  # get jwt to log in


class Mutation(AuthMutation, graphene.ObjectType):
    # keywords that will be used to do the mutation in the frontend
    create_contact = ContactMutation.Field()
    update_contact = ContactMutationUpdate.Field()
    delete_contact = ContactDelete.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
