import os
import requests
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

class WeatherAPI:
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHERMAP_API_KEY')
        self.base_url = 'http://api.openweathermap.org/data/2.5/weather'

    def get_weather(self, city='Tokyo'):
        """指定された都市の天気情報を取得する"""
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric',  # 摂氏温度で取得
            'lang': 'ja'  # 日本語で取得
        }

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            weather_data = response.json()
            return self._format_weather_data(weather_data)
        except requests.exceptions.RequestException as e:
            return f'エラーが発生しました: {str(e)}'

    def _format_weather_data(self, data):
        """天気データを見やすい形式にフォーマットする"""
        return {
            '都市': data['name'],
            '天気': data['weather'][0]['description'],
            '気温': f"{data['main']['temp']}°C",
            '湿度': f"{data['main']['humidity']}%",
            '気圧': f"{data['main']['pressure']}hPa",
            '風速': f"{data['wind']['speed']}m/s"
        }

def main():
    weather_api = WeatherAPI()
    
    # 都市名を入力
    city = input('都市名を入力してください（デフォルト: Tokyo）: ').strip() or 'Tokyo'
    
    # 天気情報を取得
    weather_info = weather_api.get_weather(city)
    
    # 結果を表示
    if isinstance(weather_info, dict):
        print('\n=== 天気情報 ===')
        for key, value in weather_info.items():
            print(f'{key}: {value}')
    else:
        print(weather_info)

if __name__ == '__main__':
    main()
