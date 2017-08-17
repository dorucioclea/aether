from django.core.exceptions import ValidationError
from django.db import IntegrityError

from . import CustomTestCase
from ..models import XForm, validate_xmldict


class ModelsTests(CustomTestCase):

    def test__validate_xmldict_no_title(self):
        self.assertRaises(
            ValidationError,
            validate_xmldict,
            '''
                <h:html>
                  <h:head>
                    <model>
                      <instance>
                      </instance>
                    </model>
                  </h:head>
                  <h:body>
                  </h:body>
                </h:html>
            '''
        )

    def test__validate_xmldict_empty_title(self):
        self.assertRaises(
            ValidationError,
            validate_xmldict,
            '''
                <h:html>
                  <h:head>
                    <h:title></h:title>
                    <model>
                      <instance id="xform-id-test">
                      </instance>
                    </model>
                  </h:head>
                  <h:body>
                  </h:body>
                </h:html>
            '''
        )

    def test__validate_xmldict_no_xform_id(self):
        self.assertRaises(
            ValidationError,
            validate_xmldict,
            '''
                <h:html>
                  <h:head>
                    <h:title>xForm - Test</h:title>
                    <model>
                      <instance>
                      </instance>
                      <instance>
                        <None></None>
                      </instance>
                    </model>
                  </h:head>
                  <h:body>
                  </h:body>
                </h:html>
            '''
        )

    def test__validate_xmldict_empty_xform_id(self):
        self.assertRaises(
            ValidationError,
            validate_xmldict,
            '''
                <h:html>
                  <h:head>
                    <h:title>xForm - Test</h:title>
                    <model>
                      <instance id="">
                      </instance>
                    </model>
                  </h:head>
                  <h:body>
                  </h:body>
                </h:html>
            '''
        )

    def test__xform__create__raises_errors(self):
        # missing required fields
        self.assertRaises(
            IntegrityError,
            XForm.objects.create,
        )
        # missing xml_data
        self.assertRaises(
            IntegrityError,
            XForm.objects.create,
            gather_core_survey_id=1,
        )
        # missing survey id
        self.assertRaises(
            IntegrityError,
            XForm.objects.create,
            xml_data=self.samples['data']['xml-ok'],
        )
        # xml_data with missing properties
        self.assertRaises(
            IntegrityError,
            XForm.objects.create,
            gather_core_survey_id=1,
            xml_data='''
                <h:html>
                  <h:head>
                    <model>
                      <instance>
                      </instance>
                    </model>
                  </h:head>
                  <h:body>
                  </h:body>
                </h:html>
            ''',
        )
        # corrupted xml_data
        self.assertRaises(
            IntegrityError,
            XForm.objects.create,
            gather_core_survey_id=1,
            xml_data='''
                <h:html
                    xmlns="http://www.w3.org/2002/xforms"
                    xmlns:ev="http://www.w3.org/2001/xml-events"
                    xmlns:h="http://www.w3.org/1999/xhtml"
                    xmlns:jr="http://openrosa.org/javarosa"
                    xmlns:orx="http://openrosa.org/xforms"
                    xmlns:xsd="http://www.w3.org/2001/XMLSchema">

                  <h:head>
            ''',
        )

    def test__xform__save(self):
        instance = XForm.objects.create(
            gather_core_survey_id=1,
            xml_data=self.samples['data']['xml-ok'],
        )
        instance.save()

        self.assertEqual(instance.form_id, 'xform-id-test')
        self.assertEqual(instance.title, 'xForm - Test')
        self.assertTrue(instance.gather_core_url.endswith('/surveys/1/responses/'))
        self.assertEqual(instance.url, '/forms/{}/form.xml'.format(instance.id))

    def test__xform__surveyors(self):
        instance = XForm.objects.create(
            gather_core_survey_id=1,
            xml_data=self.samples['data']['xml-ok'],
        )
        instance.save()
        self.assertEqual(instance.surveyors.count(), 0, 'no granted surveyors')

        self.helper_create_superuser()
        self.assertTrue(instance.is_surveyor(self.admin),
                        'superusers are always granted surveyors')

        self.helper_create_user()
        self.assertTrue(instance.is_surveyor(self.user),
                        'if not granted surveyors all users are surveyors')

        surveyor = self.helper_create_surveyor()
        instance.surveyors.add(surveyor)
        instance.save()

        self.assertEqual(instance.surveyors.count(), 1, 'one granted surveyor')
        self.assertTrue(instance.is_surveyor(surveyor))
        self.assertTrue(instance.is_surveyor(self.admin),
                        'superusers are always granted surveyors')
        self.assertFalse(instance.is_surveyor(self.user),
                         'if granted surveyors not all users are surveyors')
