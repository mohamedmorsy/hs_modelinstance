from django.contrib.contenttypes import generic
from django.contrib.auth.models import User, Group
from django.db import models
from mezzanine.pages.models import Page, RichText
from mezzanine.core.models import Ownable
from hs_core.models import AbstractResource, resource_processor
from mezzanine.pages.page_processors import processor_for
import datetime as dt
#Models.py is used to create the new tables and attributes in the database
# To create a new resource, use these three super-classes. 
#
# create a new class which contains the specific metadata attributes for
#Model Instance Resource type
class ModelInstanceResource(Page, RichText, AbstractResource):

# these are the metadata data that will be added to the core metadata
# of Generic resource type. The core metadata for generic resource type are:
# resource type, title, creator, contributor, abstract, subject

#################################
### Model Instance attributes ###
################################

    # Spatial coverage
    spatial_coverage = models.CharField(verbose_name='Spatial Coverage ',null=False,blank=True,default='unknown',max_length=255,
                                          help_text='The spatial coverage. Maybe it is a point or box ')
    # Temporal coverage
    temporal_coverage = models.CharField(verbose_name='Temporal Coverage ',null=False,blank=True,default='unknown',max_length=255,
                                          help_text='The Temporal coverage')
    # Include output
    includes_output = models.CharField(verbose_name='Does the Model Instance include output files? ',null=False,blank=True,default=None,max_length=255,
                                          help_text='Yes or No')
    # Model Program used for Execution
    executed_by = models.CharField(verbose_name='Executed by ',null=False,blank=True,default='unknown',max_length=255,
                                          help_text='Model Program used for execution')

    class Meta:
        verbose_name = 'ModelInstance'

processor_for(ModelInstanceResource)(resource_processor)