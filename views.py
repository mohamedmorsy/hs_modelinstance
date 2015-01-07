from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
#from django.common.decorators import render_to
from hs_core import hydroshare
from hs_core.hydroshare.hs_bagit import create_bag
from hs_core.models import ResourceFile
from django import forms
from .models import ModelInstanceResource
from django.utils.timezone import now
from ga_resources.utils import json_or_jsonp
import json
import os
from django.conf import settings
#from .metadata import parser  #I comment this line for now. it should b rechecked later
import mmap
import requests
import csv
from django.contrib.auth.models import User, Group
from mezzanine.pages.page_processors import processor_for
import os
from lxml import etree
from StringIO import StringIO
import datetime
from django.utils.timezone import now
import dateutil.parser


class DetailView(generic.DetailView):
    model = ModelInstanceResource
    template_name = 'hs_modelinstance/detail.html'#redirect to file detail.html




class CreateModelInstanceForm(forms.Form):
    title = forms.CharField(required=True)
    abstract = forms.CharField(required=False, min_length=0)
    creators = forms.CharField(required=False, min_length=0)
    contributors = forms.CharField(required=False, min_length=0)
    keywords = forms.CharField(required=False, min_length=0)
    spatial_coverage_type = forms.CharField(required=False, min_length=0)
    spatial_coverage = forms.CharField(required=False, min_length=0)
    temporal_coverage = forms.CharField(required=False, min_length=0)
    includes_output = forms.CharField(required=False, min_length=0)
    executed_by = forms.CharField(required=False, min_length=0)

@login_required
def create_model_instance(request, *args, **kwargs):
    frm = CreateModelInstanceForm(request.POST)
    if frm.is_valid():
        dcterms = [
            { 'term': 'T', 'content': frm.cleaned_data['title']},
            { 'term': 'AB', 'content': frm.cleaned_data['abstract'] or frm.cleaned_data['title']},
            { 'term': 'DTS', 'content': now().isoformat()}
        ]

        for cr in frm.cleaned_data['creators'].split(','):
            cr = cr.strip()
            dcterms.append({'term' : 'CR', 'content' : cr})

        for cn in frm.cleaned_data['contributors'].split(','):
            cn = cn.strip()
            dcterms.append({'term' : 'CN', 'content' : cn})

        spatial_coverage_type = frm.cleaned_data["spatial_coverage_type"]
        spatial_coverage = frm.cleaned_data["spatial_coverage"].split(',')
        temporal_coverage = frm.cleaned_data["temporal_coverage"].split(',')
        includes_output = frm.cleaned_data["includes_output"]
        executed_by = frm.cleaned_data["executed_by"]


        mterms = []
        if spatial_coverage_type == 'box':
            name = spatial_coverage[0]
            northlimit = spatial_coverage[1]
            eastlimit = spatial_coverage[2]
            southlimit = spatial_coverage[3]
            westlimit = spatial_coverage[4]
            uplimit = spatial_coverage[5]
            downlimit = spatial_coverage[6]
            units = spatial_coverage[7]
            zunits = spatial_coverage[8]
            projection = spatial_coverage[9]
            val = ({'name':name,'northlimit':northlimit, 'eastlimit':eastlimit, 'southlimit':southlimit, 'westlimit':westlimit, 'units':units, 'uplimit':uplimit, 'downlimit':downlimit, 'zunits':zunits, 'projection':projection})
            mterms.append({'coverage':{'type' :'box', 'value' : val}})
        elif spatial_coverage_type =='point':
            name = spatial_coverage[0]
            east = spatial_coverage[1]
            north = spatial_coverage[2]
            elevation = spatial_coverage[3]
            units = spatial_coverage[4]
            zunits = spatial_coverage[5]
            projection = spatial_coverage[6]
            val = ({'name':name, 'east':east, 'north':north, 'elevation':elevation, 'units':units, 'zunits':zunits, 'projection':projection})
            mterms.append({'coverage':{'type' :'point', 'value':val}})
        name = temporal_coverage[0]
        start_txt = temporal_coverage[1]
        end_txt = temporal_coverage[2]
        start = dateutil.parser.parse(start_txt)
        end = dateutil.parser.parse(end_txt)
        val=  ({'name':name, 'start':start_txt, 'end':end_txt})
        mterms.append({'coverage':{'type' :'period', 'value':val}})

        res = hydroshare.create_resource(
            resource_type='ModelInstanceResource',
            owner=request.user,
            title=frm.cleaned_data['title'],
            keywords=[k.strip() for k in frm.cleaned_data['keywords'].split(',')] if frm.cleaned_data['keywords'] else None,
            dublin_metadata=dcterms,
            content=frm.cleaned_data['abstract'] or frm.cleaned_data['title'],
            metadata = mterms,
            spatial_coverage=spatial_coverage,
            temporal_coverage=temporal_coverage,
            includes_output=includes_output,
            executed_by=executed_by,
            files=request.FILES.getlist('files')
        )
        return HttpResponseRedirect(res.get_absolute_url())

@processor_for(ModelInstanceResource)
def add_dublin_core(request, page):
    from dublincore import models as dc

    class DCTerm(forms.ModelForm):
        class Meta:
            model = dc.QualifiedDublinCoreElement
            fields = ['term', 'content']

    cm = page.get_content_model()
    try:
        abstract = cm.dublin_metadata.filter(term='AB').first().content
    except:
        abstract = None
    coverages = cm.metadata.coverages.all()
    return {
        'dublin_core': [t for t in cm.dublin_metadata.all().exclude(term='AB').exclude(term='DM').exclude(term='DC').exclude(term='DTS').exclude(term='T')],
        'abstract': abstract,
        'short_id': cm.short_id,
        'resource_type': cm._meta.verbose_name,
        'coverages': coverages,
        'spatial_coverage': cm.spatial_coverage,
        'temporal_coverage': cm.temporal_coverage,
        'includes_output': cm.includes_output,
        'executed_by' : cm.executed_by,
        'files': cm.files.all(),
        'dcterm_frm': DCTerm(),
        'bag': cm.bags.first(),
        'users': User.objects.all(),
        'groups': Group.objects.all(),
        'owners': set(cm.owners.all()),
        'view_users': set(cm.view_users.all()),
        'view_groups': set(cm.view_groups.all()),
        'edit_users': set(cm.edit_users.all()),
        'edit_groups': set(cm.edit_groups.all()),
    }

