# graphql_django_api

### Setup local

    python -m venv env
    pip3 install -r requirements.txt
    python manage.py migrate

### Launch app

    python manage.py runserver

### URLs

- 127.0.0.1:8000/admin
- 127.0.0.1:8000/graphql

### Creating content

Create your own contacts in admin console

### Run your first query

You can run your first query with following :

    {
        listContacts {
            id
            name
            phone
            message
        }
    }

Create your contact with new query :

    mutation nameOfMutation {
        createContact(name: "New Contact", phoneNumber: "486054-850"){
            contact {
            name,
            phoneNumber
            }
        }
    }

Delete a contact : 

    mutation delete {
        deleteContact(id: 1) {
            contact {
                    id
                }
            }
    }

### Authentication

You can create a new user admin with this following query :

    mutation {
        register (
            email: "admin3@gmail.com",
            username: "admin3",
            password1: "djh46rg49390r",
            password2: "djh46rg49390r"
        ) {
            success,
            errors,
            token,
            refreshToken,
        }
    }

At the moment, the user you just created is not verified. To verify the user, copy the verification token from the email sent to the terminal when you created the new user.


![Alt text](<term_serv.png>)

After copying the token, run the command below with that token.

    mutation {
        verifyAccount(token: "eyJ1c2VybmFtZSI6ImFkbWluMyIsImFjdGlvbiI6ImFjdGl2YXRpb24ifQ:1r8i3l:O2OH-2-Tnp8aNCu8EikkDLjpQYf9i-oXdMWHk8ujqL8") {
            success
            errors
        }
    }

You can now log in by running the query below:

    mutation {
        tokenAuth(username: "admin3", password: "djh83rg49390r") {
            success,
            errors
        }
    }

![Alt text](<success_verify.png>)
