from django.contrib.contenttypes import generic
from django.contrib.auth.models import User, Group
from django.db import models
from mezzanine.pages.models import Page, RichText
from mezzanine.core.models import Ownable
from hs_core.models import AbstractResource
import datetime as dt
#
# To create a new resource, use these three super-classes. 
#

#class ModelInstanceResource(Page, RichText, AbstractResource):


