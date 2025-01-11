import pytest
from unittest.mock import patch, Mock
from weather import WeatherAPI

@pytest.fixture
def weather_api():
    with patch.dict('os.environ', {'OPENWEATHERMAP_API_KEY': 'dummy_key'}):
        return WeatherAPI()

@pytest.fixture
def mock_weather_response():
    return {
        'name': 'Tokyo',
        'weather': [{'description': '晴れ'}],
        'main': {
            'temp': 20.5,
            'humidity': 65,
            'pressure': 1013
        },
        'wind': {
            'speed': 3.2
        }
    }

def test_weather_api_initialization(weather_api):
    assert weather_api.api_key == 'dummy_key'
    assert weather_api.base_url == 'http://api.openweathermap.org/data/2.5/weather'

def test_format_weather_data(weather_api, mock_weather_response):
    formatted_data = weather_api._format_weather_data(mock_weather_response)
    
    assert formatted_data['都市'] == 'Tokyo'
    assert formatted_data['天気'] == '晴れ'
    assert formatted_data['気温'] == '20.5°C'
    assert formatted_data['湿度'] == '65%'
    assert formatted_data['気圧'] == '1013hPa'
    assert formatted_data['風速'] == '3.2m/s'

@patch('requests.get')
def test_get_weather_success(mock_get, weather_api, mock_weather_response):
    mock_response = Mock()
    mock_response.json.return_value = mock_weather_response
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = weather_api.get_weather('Tokyo')
    
    assert isinstance(result, dict)
    assert result['都市'] == 'Tokyo'
    assert '天気' in result
    assert '気温' in result
    assert '湿度' in result
    assert '気圧' in result
    assert '風速' in result

    mock_get.assert_called_once()
    args, kwargs = mock_get.call_args
    assert kwargs['params']['q'] == 'Tokyo'
    assert kwargs['params']['appid'] == 'dummy_key'
    assert kwargs['params']['units'] == 'metric'
    assert kwargs['params']['lang'] == 'ja'

@patch('requests.get')
def test_get_weather_error(mock_get, weather_api):
    mock_get.side_effect = requests.exceptions.RequestException('API error')
    
    result = weather_api.get_weather('InvalidCity')
    
    assert isinstance(result, str)
    assert 'エラーが発生しました' in result

def test_default_city(weather_api):
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = mock_weather_response()
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = weather_api.get_weather()
        
        args, kwargs = mock_get.call_args
        assert kwargs['params']['q'] == 'Tokyo'  # デフォルト値のテスト