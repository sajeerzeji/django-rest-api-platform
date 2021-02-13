import datetime
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import capfirst
from django.core import exceptions
from django.contrib.auth.models import Group, User

from tenant.persistence.model.tenant_model import Tenant

REQUIRED_FIELDS = (
    {'field': 'tenant_name', 'message': 'Please enter the tenant name'},
    {'field': 'username', 'message': 'Please enter the username'},
    {'field': 'password', 'message': 'Please enter the password'},
    {'field': 'schema_name', 'message': 'Please enter the schema name'}
    )

# FIELDS = ('tenant_name', 'username', 'password', 'paid_until', 'schema_name')

class Command(BaseCommand):
    help = 'Create a client'

    def add_arguments(self, parser):
        """
        Args:
            parser:
        Returns:
        """
        for field in REQUIRED_FIELDS:
            parser.add_argument('--%s' % field['field'], action='append',
                                help='Specifies the %s for the superuser.' % field['field'], )

    def handle(self, *args, **options):
        user_data = {}
        tenantName = input('Enter tenant name: ')
        username = input('Enter username: ')
        password = input('Enter password: ')
        paidUntil = input('You are paid until? (YYYY-MM-DD) : ')
        schemaName = input('Enter schema name')

        user_data['tenant_name'] = tenantName
        user_data['paid_until'] = paidUntil
        user_data['on_trial'] = False
        user_data['schema_name'] = schemaName

        tenant = Tenant.objects.create(**user_data)
        tenant.save()
        if options['verbosity'] >= 1:
            self.stdout.write("Client created successfully.")

        # user_data = {}
        # for required_field in REQUIRED_FIELDS:
        #     user_data[required_field['field']] = options[required_field['field']]
        #     while user_data[required_field['field']] is None:
        #         message = self._get_input_message(required_field['message'])
        #         input_value = self.get_input_data(required_field['message'], message)
        #         user_data[required_field['field']] = input_value

        # tenant = Client.objects.create(**user_data)
        # tenant.save()
        # if options['verbosity'] >= 1:
        #     self.stdout.write("Client created successfully.")

    def get_input_data(self, field, message, default=None):
        """
        Override this method if you want to customize data inputs or
        validation exceptions.
        """
        raw_value = input(message)
        if default and raw_value == '':
            raw_value = default
        try:
            val = field.clean(raw_value, None)
        except exceptions.ValidationError as e:
            self.stderr.write("Error: %s" % '; '.join(e.messages))
            val = None

        return val

    @staticmethod
    def _get_input_message(field, default=None):
        return field + ': '
        # return '%s%s%s: ' % (
        #     capfirst(field.verbose_name),
        #     " (leave blank to use '%s')" % default if default else '',
        #     ' (%s.%s)' % (
        #         field.remote_field.model._meta.object_name,
        #         field.m2m_target_field_name() if field.many_to_many else field.remote_field.field_name,
        #     ) if field.remote_field else '',
        # )