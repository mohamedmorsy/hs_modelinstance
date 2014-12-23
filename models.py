from django.contrib.contenttypes import generic
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth.models import User, Group
from django.db import models
from mezzanine.pages.models import Page, RichText
from mezzanine.core.models import Ownable
from hs_core.models import AbstractResource, resource_processor, CoreMetaData, AbstractMetaDataElement
from mezzanine.pages.page_processors import processor_for
import datetime as dt
#Models.py is used to create the new tables and attributes in the database
# To create a new resource, use these three super-classes.
# create a new class which contains the specific metadata attributes for

# extended metadata elements for ModelInstance resource type
class ModelOutput(AbstractMetaDataElement):
    term = 'ModelOutput'
    includes_output = models.BooleanField()

    @classmethod
    def create(cls, **kwargs):
        return ModelOutput.objects.create(**kwargs)

    @classmethod
    def update(cls, element_id, **kwargs):
        model_output = ModelOutput.objects.get(id=element_id)
        if model_output:
            for key, value in kwargs.iteritems():
                setattr(model_output, key, value)

            model_output.save()
        else:
            raise ObjectDoesNotExist("No ModelOutput element was found for the provided id:%s" % kwargs['id'])

    @classmethod
    def remove(cls, element_id):
        raise ValidationError("ModelOutput element of a resource can't be deleted.")


class ExecutedBy(AbstractMetaDataElement):
    term = 'ExecutedBY'
    name = models.CharField(max_length=500)
    url = models.URLField()

    def __unicode__(self):
        self.name

    @classmethod
    def create(cls, **kwargs):
        return ExecutedBy.objects.create(**kwargs)

    @classmethod
    def update(cls, element_id, **kwargs):
        executed_by = ExecutedBy.objects.get(id=element_id)
        if executed_by:
            for key, value in kwargs.iteritems():
                setattr(executed_by, key, value)

            executed_by.save()
        else:
            raise ObjectDoesNotExist("No ExecutedBy element was found for the provided id:%s" % kwargs['id'])

    @classmethod
    def remove(cls, element_id):
        raise ValidationError("ExecutedBy element of a resource can't be deleted.")

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
    includes_output = models.BooleanField(verbose_name='includes output files? ',null=False,blank=True,default=None,max_length=255,
                                          help_text='Yes or No')
    # Model Program used for Execution
    executed_by = models.CharField(verbose_name='Executed by ',null=False,blank=True,default='unknown',max_length=255,
                                          help_text='Model Program used for execution')

    class Meta:
        verbose_name = 'Model Instance Resource'


    #@property
    #def metadata(self):
        #md = ModelInstanceMetaData()
        #return self._get_metadata(md)

processor_for(ModelInstanceResource)(resource_processor)

# metadata container class
class ModelInstanceMetaData(CoreMetaData):
    _model_output = generic.GenericRelation(ModelOutput)
    _executed_by = generic.GenericRelation(ExecutedBy)
    _model_instance_resource = generic.GenericRelation(ModelInstanceResource)

    @property
    def resource(self):
        return self._model_instance_resource.all().first()

    @property
    def model_output(self):
        return self._model_output.all().first()

    @property
    def executed_by(self):
        return self._executed_by.all().first()

    @classmethod
    def get_supported_element_names(cls):
        # get the names of all core metadata elements
        elements = super(ModelInstanceMetaData, cls).get_supported_element_names()
        # add the name of any additional element to the list
        elements.append('ModelOutput')
        elements.append('ExecutedBy')
        return elements

    def get_xml(self, pretty_print=True):
        from lxml import etree
        # get the xml string representation of the core metadata elements
        xml_string = super(ModelInstanceMetaData, self).get_xml(pretty_print=False)

        # create an etree xml object
        RDF_ROOT = etree.fromstring(xml_string)

        # get root 'Description' element that contains all other elements
        container = RDF_ROOT.find('rdf:Description', namespaces=self.NAMESPACES)

        if self.modeloutput:
            hsterms_modeloutput = etree.SubElement(container, '{%s}variable' % self.NAMESPACES['hsterms'])
            hsterms_modeloutput_rdf_Description = etree.SubElement(hsterms_modeloutput, '{%s}Description' % self.NAMESPACES['rdf'])
            hsterms_modeloutput_value = etree.SubElement(hsterms_modeloutput_rdf_Description, '{%s}ModelOutputValue' % self.NAMESPACES['hsterms'])
            hsterms_modeloutput_value.text = self.modeloutput.includes_output

        if self.executedby:
            hsterms_executedby = etree.SubElement(container, '{%s}variable' % self.NAMESPACES['hsterms'])
            hsterms_executedby_rdf_Description = etree.SubElement(hsterms_executedby, '{%s}Description' % self.NAMESPACES['rdf'])
            hsterms_executedby_name = etree.SubElement(hsterms_executedby_rdf_Description, '{%s}ModelProgramName' % self.NAMESPACES['hsterms'])
            hsterms_executedby_name.text = self.executedby.name
            hsterms_executedby_url = etree.SubElement(hsterms_executedby_rdf_Description, '{%s}ModelProgramURL' % self.NAMESPACES['hsterms'])
            hsterms_executedby_url.text = self.executedby.url

        return etree.tostring(RDF_ROOT, pretty_print=True)