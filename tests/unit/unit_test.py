from blueprints.users.resources import UserResource
from blueprints import db
from tests import reset_database
from mock import patch
from blueprints.api import CurrentWeather

class TestUnit():

  reset_database()

  def test_is_exist_function(self):
    assert UserResource.is_exist(self,'admin')==True
    assert UserResource.is_exist(self,'tidak_ada') == False
  
  @patch.object(CurrentWeather,'get')
  def test_get_temp_function(self, mock_get):
    temp = { 'temp' : 22.5 }
    mock_get.return_value = temp
    assert CurrentWeather.get() == temp
  
  # def test_get_temp_asli(self):
    # assert CurrentWeather.get(self).status_code == 200