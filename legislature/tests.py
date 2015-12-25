# -*- coding: utf8 -*-
import re

from django.test import TestCase, Client
from django.test.utils import override_settings

class RedisplayativeDetailTest(TestCase):
    fixtures = ['one_representative.json']

    def setUp(self):
        self.client = Client()

        if not hasattr(type(self), 'response'):
            # Do it once and for all, note that this also caches content types
            # so the contenttype query used by taggit won't be counted in
            # test_num_queries.
            self.__class__.response = self.client.get(
                    '/legislature/karima-delli')
        self.response = self.__class__.response

    def assertHtmlInResult(self, expected):
        compare = re.sub('[\s"\']', '', expected)
        result = re.sub('[\s"\']', '', self.response.content)
        assert compare in result

    # Cancel out constance with TEMPLATE_CONTEXT_PROCESSORS=[]
    @override_settings(TEMPLATE_CONTEXT_PROCESSORS=[])
    def test_num_queries(self):
        with self.assertNumQueries(5):
            response = self.client.get('/legislature/karima-delli')

    def test_name_display(self):
        # When HAMLPY_ATTR_WRAPPER works, use double quotes in HTML attrs !
        assert "<h1 class='name'>Karima DELLI</h1>" in self.response.content

    def test_score_display(self):
        assert '<span class="label label-success">233</span>' in self.response.content

    def test_country_display(self):
        assert re.findall('<span class="flag-icon flag-icon-fr"></span>\s+France', self.response.content)  # noqa

    def test_current_mandate_display(self):
        assert re.findall("<a href='/legislature/group/Greens/EFA'>\s+Member of\s+Group of the Greens/European Free Alliance\s+</a>", self.response.content)  # noqa

    def test_biography_display(self):
        assert re.findall('Born in Roubaix the\s+04/03/1979\s+\(F\)', self.response.content)  # noqa

    def test_votes_display(self):
        expected = '''
          <tr>
            <td>Our first test recommendation</td>
            <td class="icon-cell">
              <i aria-label="for" class="fa fa-thumbs-up vote_positive" title="for"></i>
            </td>
            <td class="icon-cell">
              <i aria-label="for" class="fa fa-thumbs-up vote_positive" title="for"></i>
            </td>
            <td class="icon-cell">
              <span class="label label-success">4</span>


            </td>
          </tr>

          <tr>
            <td>Our second recommendation</td>
            <td class="icon-cell">
              <i aria-label="for" class="fa fa-thumbs-up vote_positive" title="for"></i>
            </td>
            <td class="icon-cell">
              <i aria-label="for" class="fa fa-thumbs-up vote_positive" title="for"></i>
            </td>
            <td class="icon-cell">
              <span class="label label-success">6</span>


            </td>
          </tr>

          <tr>
            <td>Our third recommendation</td>
            <td class="icon-cell">
              <i aria-label="for" class="fa fa-thumbs-up vote_positive" title="for"></i>
            </td>
            <td class="icon-cell">
              <i aria-label="for" class="fa fa-thumbs-up vote_positive" title="for"></i>
            </td>
            <td class="icon-cell">
              <span class="label label-success">5</span>


            </td>
          </tr>
        '''
        self.assertHtmlInResult(expected)

    def test_mandates_display(self):
        expected = '''
  <h2>Mandates</h2>

  <table class='table table-condensed mandates'>

      <tr class='mandate'>
        <td>Member</td>
        <td>
          <a href='/legislature/committee/TRAN'>
            Committee on Transport and Tourism (TRAN)
          </a>
        </td>
        <td>01/07/2014</td>
        <td>present</td>
        <td>European Parliament</td>

      </tr>

      <tr class='mandate'>
        <td>Substitute</td>
        <td>
          <a href='/legislature/committee/FEMM'>
            Committee on Women&#39;s Rights and Gender Equality (FEMM)
          </a>
        </td>
        <td>01/07/2014</td>
        <td>present</td>
        <td>European Parliament</td>

      </tr>

      <tr class='mandate'>
        <td>Substitute</td>
        <td>
          <a href='/legislature/committee/EMPL'>
            Committee on Employment and Social Affairs (EMPL)
          </a>
        </td>
        <td>01/07/2014</td>
        <td>present</td>
        <td>European Parliament</td>

      </tr>

      <tr class='mandate'>
        <td>Member</td>
        <td>
          <a href='/legislature/delegation/Delegation%20for%20relations%20with%20India'>
            Delegation for relations with India ()
          </a>
        </td>
        <td>14/07/2014</td>
        <td>present</td>
        <td>European Parliament</td>

      </tr>

      <tr class='mandate'>
        <td>Member</td>
        <td>
          <a href='/legislature/group/Greens/EFA'>
            Group of the Greens/European Free Alliance (Greens/EFA)
          </a>
        </td>
        <td>01/07/2014</td>
        <td>present</td>
        <td>European Parliament</td>

      </tr>

      <tr class='mandate'>
        <td></td>
        <td>
          <a href='/legislature/country/FR'>
            France (FR)
          </a>
        </td>
        <td>01/07/2014</td>
        <td>present</td>
        <td>Europe Écologie</td>

      </tr>

      <tr class='mandate'>
        <td>Member</td>
        <td>
          <a href='/legislature/committee/EMPL'>
            Committee on Employment and Social Affairs (EMPL)
          </a>
        </td>
        <td>19/01/2012</td>
        <td>30/06/2014</td>
        <td>European Parliament</td>

      </tr>

      <tr class='mandate'>
        <td>Substitute</td>
        <td>
          <a href='/legislature/committee/REGI'>
            Committee on Regional Development (REGI)
          </a>
        </td>
        <td>19/01/2012</td>
        <td>30/06/2014</td>
        <td>European Parliament</td>

      </tr>

      <tr class='mandate'>
        <td>Member</td>
        <td>
          <a href='/legislature/delegation/Delegation%20for%20relations%20with%20India'>
            Delegation for relations with India ()
          </a>
        </td>
        <td>16/09/2009</td>
        <td>30/06/2014</td>
        <td>European Parliament</td>

      </tr>

      <tr class='mandate'>
        <td>Member</td>
        <td>
          <a href='/legislature/group/Greens/EFA'>
            Group of the Greens/European Free Alliance (Greens/EFA)
          </a>
        </td>
        <td>14/07/2009</td>
        <td>30/06/2014</td>
        <td>European Parliament</td>

      </tr>

      <tr class='mandate'>
        <td></td>
        <td>
          <a href='/legislature/country/FR'>
            France (FR)
          </a>
        </td>
        <td>14/07/2009</td>
        <td>30/06/2014</td>
        <td>Europe Écologie</td>

      </tr>

      <tr class='mandate'>
        <td>Member</td>
        <td>
          <a href='/legislature/committee/EMPL'>
            Committee on Employment and Social Affairs (EMPL)
          </a>
        </td>
        <td>16/07/2009</td>
        <td>18/01/2012</td>
        <td>European Parliament</td>

      </tr>

      <tr class='mandate'>
        <td>Substitute</td>
        <td>
          <a href='/legislature/committee/REGI'>
            Committee on Regional Development (REGI)
          </a>
        </td>
        <td>14/09/2009</td>
        <td>18/01/2012</td>
        <td>European Parliament</td>

      </tr>

      <tr class='mandate'>
        <td>Member</td>
        <td>
          <a href='/legislature/committee/REGI'>
            Committee on Regional Development (REGI)
          </a>
        </td>
        <td>16/07/2009</td>
        <td>13/09/2009</td>
        <td>European Parliament</td>

      </tr>

  </table>
        '''
        self.assertHtmlInResult(expected)

    def test_positions_display(self):
        expected = '''
  <div class='positions'>
    <h2>Public positions</h2>

    <table class='table table-condensed'>

        <tr class='position'>
          <td>08/12/2015</td>
          <td>
            <a href='/positions/2/'>
              Validated text
            </a>
          </td>
          <td>

              <span class='label label-default'>
                acta
              </span>

              <span class='label label-default'>
                bar
              </span>

          </td>
          <td>
            <a href='http://example.com/validated'>
              http://example.com/validated

            </a>
          </td>
        </tr>

    </table>
        '''
        self.assertHtmlInResult(expected)

# group-index(kind)
# redisplayative-detail(name)
# redisplayative-detail(pk)
# redisplayative-index(group_kind)(group)
# redisplayative-index(active)
