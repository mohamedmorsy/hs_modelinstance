from django.contrib.contenttypes import generic
from django.contrib.auth.models import User, Group
from django.db import models
from mezzanine.pages.models import Page, RichText
from mezzanine.core.models import Ownable
from hs_core.models import AbstractResource
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

    # Input/Output data format
    data_format = models.CharField(verbose_name='Data Format ',null=False,blank=True,default='Zip files',max_length=255,
                                          help_text='The Input and Output data format')
    # Related resources
    related_resources = models.TextField(verbose_name="Related Resources", null=False,default="",
                                       help_text="Notes about any resources related to Model Instance (e.g. published papers)")
    # Spatial coverage
    spatial_coverage = models.CharField(verbose_name='Spatial Coverage ',null=False,blank=True,default='unknown',max_length=255,
                                          help_text='The spatial coverage. Maybe it is a point or box ')
    # Spatial coverage resolution
    spatial_resolution = models.CharField(verbose_name='Spatial Coverage Resolution ',null=False,blank=True,default='unknown',max_length=255,
                                          help_text='The spatial coverage resolution')
    # Temporal coverage
    temporal_coverage = models.CharField(verbose_name='Temporal Coverage ',null=False,blank=True,default='unknown',max_length=255,
                                          help_text='The Temporal coverage')
    # Temporal coverage resolution
    temporal_resolution = models.CharField(verbose_name='Temporal Coverage Resolution ',null=False,blank=True,default='unknown',max_length=255,
                                          help_text='The spatial coverage resolution')
    # Include output
    includes_output = models.CharField(verbose_name='Does the Model Instance include output files? ',null=False,blank=True,default=None,max_length=255,
                                          help_text='Yes or No')
    # Model Program used for Execution
    executed_by = models.CharField(verbose_name='Executed by ',null=False,blank=True,default='unknown',max_length=255,
                                          help_text='Model Program used for execution')

    class Meta:
        verbose_name = 'ModelInstance'