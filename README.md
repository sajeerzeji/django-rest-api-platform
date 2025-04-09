# Rest API Platform in Django

This is a REST API platform developed in django with support of oauth and multi tenancy

## Installation

1. Make sure you have installed postgresql
2. Create a db called oh
3. Checkout the repository
4. Make migrations
```bash
python manage.py makemigrations tenant
```
5. Migrate schemas
```bash
python manage.py migrate_schemas
```
6. Create a super user
```bash
python manage.py createsuperuser
```
7. Create an application from [admin](http://localhost:8000/admin) portal. Make sure you selected grant type `Resource owner password-based` and client type `confidential`

## Usage

Now you can call the auth api with the credentials
`http://localhost:8000/o/token/?grant_type=password&username=sajeer&password=sajeer123&tenant=OH` and basic authentication where the client ID will be the username and secret will be the password

This will give you an access token, with that token as a bearer token, you can call the client API to create a new tenant

```json
{
	"tenant": "ozihawk",
	"username": "sajeer",
	"password": "sajeer123",
	"firstName": "Sajeer",
	"lastName": "Zeji",
	"mobile": "XXXXXXXXXX",
	"email": "example@example.com",
	"paidUntil": "2021-02-14"
}
```
