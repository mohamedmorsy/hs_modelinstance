from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
#from django.common.decorators import render_to
from hs_core import hydroshare
from django import forms
from .models import ModelInstanceResource
from django.utils.timezone import now
from ga_resources.utils import json_or_jsonp
import json
import os
from django.conf import settings
#from .metadata import parser  #I comment this line for now. it should b rechecked later
import mmap



class DetailView(generic.DetailView):
    model = ModelInstanceResource
    #template_name = 'hydromodel/detail.html'
    template_name = 'hs_modelinstance/detail.html'


class CreateModelInstanceForm(forms.Form):
    title = forms.CharField(required=True)
    abstract = forms.CharField(required=False, min_length=0)
    creators = forms.CharField(required=False, min_length=0)
    contributors = forms.CharField(required=False, min_length=0)
    keywords = forms.CharField(required=False, min_length=0)
    # rest_url = forms.URLField(required=False)
    # wsdl_url = forms.URLField(required=False)
    #reference_type = forms.CharField(required=False, min_length=0)
    # site = forms.CharField(required=False, min_length=0)
    # variable = forms.CharField(required=False, min_length=0)
    #software_url = forms.CharField(required=False, min_length=0)


@login_required

def create_model_instance(request, *args, **kwargs):

    print 'CREATE RESOURCE'


    frm = CreateModelInstanceForm(request.POST)

    if frm.is_valid():
        dcterms = [
            { 'term': 'T', 'content': frm.cleaned_data['title']},
            { 'term': 'AB', 'content': frm.cleaned_data['abstract'] or frm.cleaned_data['title']},
            { 'term': 'DTS', 'content': now().isoformat()}
        ]

        print 'HERE'

        res = hydroshare.create_resource(
            resource_type='ModelInstanceResource',
            owner=request.user,
            title=frm.cleaned_data['title'],
            keywords=[k.strip() for k in frm.cleaned_data['keywords'].split(',')] if frm.cleaned_data['keywords'] else None,
            dublin_metadata=dcterms,
            content=frm.cleaned_data['abstract'] or frm.cleaned_data['title'],
            # reference_type=frm.cleaned_data['reference_type'],
            #software_url=frm.cleaned_data['software_url'],
            # data_site=frm.cleaned_data.get('site', ''),
            # variable=frm.cleaned_data.get('variable', ''),
            #software_rights = frm.cleaned_data['eula'],
        )
        return HttpResponseRedirect(res.get_absolute_url())