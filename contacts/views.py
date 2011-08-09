# contacts/views.py

from django.views.generic import ListView, DetailView

from contacts.settings import CONTACT_MODEL, CONTACT_PAGINATE_BY

contact_model = get_model(*CONTACT_MODEL.split('.'))

class ContactDetailView(DetailView):
    model = contact_model

class ContactListView(ListView):
    model = contact_model
    paginate_by = paginate_by = CONTACT_PAGINATE_BY
    template = '/contacts/contact_list.html'
    context_object_name="contact_list",

class PersonListView(ContactListView):
    queryset = contact_model.objects.people()

class OrganizationListView(ListView):
    queryset = contact_model.objects.organizations()

class ContactTypeListView(ContactListView):
    queryset = contact_model.objects.people()