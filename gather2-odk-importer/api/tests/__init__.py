import base64

from django.contrib.auth import get_user_model
from django.test import TransactionTestCase

from ..models import XForm


UserModel = get_user_model().objects

XLS_FILE = '/code/api/tests/files/demo-xlsform.xls'
XML_FILE = '/code/api/tests/files/demo-xlsform.xml'
XML_FILE_ERR = '/code/api/tests/files/demo-xlsform--error.xml'

XML_DATA = '''
    <h:html
        xmlns="http://www.w3.org/2002/xforms"
        xmlns:ev="http://www.w3.org/2001/xml-events"
        xmlns:h="http://www.w3.org/1999/xhtml"
        xmlns:jr="http://openrosa.org/javarosa"
        xmlns:orx="http://openrosa.org/xforms"
        xmlns:xsd="http://www.w3.org/2001/XMLSchema">

      <h:head>
        <h:title>xForm - Test</h:title>
        <model>
          <instance>
            <None id="xform-id-test">
              <starttime/>
              <endtime/>
              <deviceid/>
              <meta>
                <instanceID/>
              </meta>
            </None>
          </instance>
          <instance id="other-entry">
          </instance>
        </model>
      </h:head>
      <h:body>
      </h:body>
    </h:html>
'''

XML_DATA_ERR = '''
    <h:html
        xmlns="http://www.w3.org/2002/xforms"
        xmlns:ev="http://www.w3.org/2001/xml-events"
        xmlns:h="http://www.w3.org/1999/xhtml"
        xmlns:jr="http://openrosa.org/javarosa"
        xmlns:orx="http://openrosa.org/xforms"
        xmlns:xsd="http://www.w3.org/2001/XMLSchema">

      <h:head>
'''

XML_XFORM = '''
    <h:html
        xmlns="http://www.w3.org/2002/xforms"
        xmlns:ev="http://www.w3.org/2001/xml-events"
        xmlns:h="http://www.w3.org/1999/xhtml"
        xmlns:jr="http://openrosa.org/javarosa"
        xmlns:orx="http://openrosa.org/xforms"
        xmlns:xsd="http://www.w3.org/2001/XMLSchema">
      <h:head>
        <h:title>my-test-form</h:title>
        <model>
          <itext>
            <translation default="true()" lang="English">
              <text id="static_instance-country-0">
                <value>Cameroon</value>
              </text>
              <text id="static_instance-country-1">
                <value>Nigeria</value>
              </text>
              <text id="static_instance-region-0">
                <value>Zone 1</value>
              </text>
              <text id="static_instance-region-1">
                <value>Zone 2</value>
              </text>
              <text id="static_instance-region-2">
                <value>North</value>
              </text>
              <text id="static_instance-region-3">
                <value>South</value>
              </text>
              <text id="static_instance-option-0">
                <value>Option A</value>
              </text>
              <text id="static_instance-option-1">
                <value>Option B</value>
              </text>
              <text id="static_instance-language-0">
                <value>English</value>
              </text>
              <text id="static_instance-language-1">
                <value>French</value>
              </text>
              <text id="static_instance-language-2">
                <value>German</value>
              </text>
            </translation>
          </itext>
          <instance>
            <None id="my-test-form">
              <starttime/>
              <endtime/>
              <deviceid/>
              <country/>
              <region/>
              <name/>
              <location/>
              <image/>
              <number/>
              <number2/>
              <date/>
              <datetime/>
              <option/>
              <option_a>
                <choice_a/>
              </option_a>
              <option_b>
                <choice_b/>
              </option_b>
              <lang/>
              <iterate_count/>
              <iterate jr:template="">
                <index/>
              </iterate>
              <meta>
                <instanceID/>
              </meta>
            </None>
          </instance>
          <instance id="country">
            <root>
              <item>
                <itextId>static_instance-country-0</itextId>
                <name>CM</name>
              </item>
              <item>
                <itextId>static_instance-country-1</itextId>
                <name>NG</name>
              </item>
            </root>
          </instance>
          <instance id="region">
            <root>
              <item>
                <itextId>static_instance-region-0</itextId>
                <country>CM</country>
                <name>CM-1</name>
              </item>
              <item>
                <itextId>static_instance-region-1</itextId>
                <country>CM</country>
                <name>CM-2</name>
              </item>
              <item>
                <itextId>static_instance-region-2</itextId>
                <country>NG</country>
                <name>NG-N</name>
              </item>
              <item>
                <itextId>static_instance-region-3</itextId>
                <country>NG</country>
                <name>NG-S</name>
              </item>
            </root>
          </instance>
          <instance id="option">
            <root>
              <item>
                <itextId>static_instance-option-0</itextId>
                <name>a</name>
              </item>
              <item>
                <itextId>static_instance-option-1</itextId>
                <name>b</name>
              </item>
            </root>
          </instance>
          <instance id="language">
            <root>
              <item>
                <itextId>static_instance-language-0</itextId>
                <name>EN</name>
              </item>
              <item>
                <itextId>static_instance-language-1</itextId>
                <name>FR</name>
              </item>
              <item>
                <itextId>static_instance-language-2</itextId>
                <name>GE</name>
              </item>
            </root>
          </instance>
          <bind
                jr:preload="timestamp"
                jr:preloadParams="start"
                jr:requiredMsg="start"
                nodeset="/None/starttime"
                required="true()"
                type="dateTime"/>
          <bind
                jr:preload="timestamp"
                jr:preloadParams="end"
                jr:requiredMsg="end"
                nodeset="/None/endtime"
                required="true()"
                type="dateTime"/>
          <bind
                jr:preload="property"
                jr:preloadParams="deviceid"
                jr:requiredMsg="device"
                nodeset="/None/deviceid"
                required="true()"
                type="string"/>
          <bind nodeset="/None/country" required="false()" type="select1"/>
          <bind nodeset="/None/region" required="false()" type="select1"/>
          <bind nodeset="/None/name" required="false()" type="string"/>
          <bind nodeset="/None/location" required="false()" type="geopoint"/>
          <bind nodeset="/None/image" required="false()" type="binary"/>
          <bind nodeset="/None/number" required="false()" type="int"/>
          <bind nodeset="/None/number2" required="false()" type="decimal"/>
          <bind nodeset="/None/date" required="false()" type="date"/>
          <bind nodeset="/None/datetime" required="false()" type="dateTime"/>
          <bind jr:requiredMsg="Choice" nodeset="/None/option" required="true()" type="select1"/>
          <bind nodeset="/None/option_a" relevant=" /None/option ='a'"/>
          <bind nodeset="/None/option_a/choice_a" type="string"/>
          <bind nodeset="/None/option_b" relevant=" /None/option ='b'"/>
          <bind nodeset="/None/option_b/choice_b" type="string"/>
          <bind nodeset="/None/lang" type="select"/>
          <bind calculate="3" nodeset="/None/iterate_count" readonly="true()" type="string"/>
          <bind nodeset="/None/iterate/index" type="string"/>
          <bind
                calculate="concat('uuid:', uuid())"
                nodeset="/None/meta/instanceID"
                readonly="true()"
                type="string"/>
        </model>
      </h:head>
      <h:body>
        <select1 ref="/None/country">
          <label>Country</label>
          <item>
            <label>Cameroon</label>
            <value>CM</value>
          </item>
          <item>
            <label>Nigeria</label>
            <value>NG</value>
          </item>
        </select1>
        <select1 ref="/None/region">
          <label>Region</label>
          <itemset nodeset="instance('region')/root/item[country =  /None/country ]">
            <value ref="name"/>
            <label ref="jr:itext(itextId)"/>
          </itemset>
        </select1>
        <input ref="/None/name">
          <label>What is your name?</label>
        </input>
        <input ref="/None/location">
          <label>Collect your GPS coordinates</label>
        </input>
        <upload mediatype="image/*" ref="/None/image">
          <label>Take a picture</label>
        </upload>
        <input ref="/None/number">
          <label>How many?</label>
        </input>
        <input ref="/None/number2">
          <label>Percentage</label>
        </input>
        <input ref="/None/date">
          <label>When?</label>
        </input>
        <input ref="/None/datetime">
          <label>At?</label>
        </input>
        <select1 ref="/None/option">
          <label>Choice (A/B)</label>
          <item>
            <label>Option A</label>
            <value>a</value>
          </item>
          <item>
            <label>Option B</label>
            <value>b</value>
          </item>
        </select1>
        <group ref="/None/option_a">
          <label>Option A</label>
          <input ref="/None/option_a/choice_a">
            <label>Choice A</label>
          </input>
        </group>
        <group ref="/None/option_b">
          <label>Option B</label>
          <input ref="/None/option_b/choice_b">
            <label>Choice B</label>
          </input>
        </group>
        <select ref="/None/lang">
          <label>Spoken languages</label>
          <item>
            <label>English</label>
            <value>EN</value>
          </item>
          <item>
            <label>French</label>
            <value>FR</value>
          </item>
          <item>
            <label>German</label>
            <value>GE</value>
          </item>
        </select>
        <group ref="/None/iterate">
          <label></label>
          <repeat jr:count=" /None/iterate_count " nodeset="/None/iterate">
            <input ref="/None/iterate/index">
              <label>Index</label>
            </input>
          </repeat>
        </group>
      </h:body>
    </h:html>
'''


class CustomTestCase(TransactionTestCase):

    def setUp(self):
        self.samples = {
            'data': {
                'xml-ok': XML_DATA,
                'xml-err': XML_DATA_ERR,

                'file-ok': XML_FILE,
                'file-err': XML_FILE_ERR,
            },

            'xform': {
                'xml': XML_XFORM,
                'file-xls': XLS_FILE,
            },
        }

    def tearDown(self):
        self.client.logout()

    def helper_create_superuser(self):
        username = 'admin'
        email = 'admin@example.com'
        password = 'adminadmin'
        basic = b'admin:adminadmin'

        self.admin = UserModel.create_superuser(username, email, password)
        self.headers_admin = {
            'HTTP_AUTHORIZATION': 'Basic ' + base64.b64encode(basic).decode('ascii')
        }
        self.assertTrue(self.client.login(username=username, password=password))

    def helper_create_user(self):
        username = 'test'
        email = 'test@example.com'
        password = 'testtest'
        basic = b'test:testtest'

        self.user = UserModel.create_user(username, email, password)
        self.headers_user = {
            'HTTP_AUTHORIZATION': 'Basic ' + base64.b64encode(basic).decode('ascii')
        }

    def helper_create_surveyor(self):
        username = 'surveyor'
        email = username + '@example.com'
        password = 'surveyorsurveyor'
        return UserModel.create_superuser(username, email, password)

    def helper_create_xform(self, surveyor=None, survey_id=1):
        xform = XForm.objects.create(
            description='test',
            gather_core_survey_id=survey_id,
            xml_data=self.samples['xform']['xml'],
        )

        if surveyor:
            xform.surveyors.add(surveyor)
            xform.save()

        return xform
