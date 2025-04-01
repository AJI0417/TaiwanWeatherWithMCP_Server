from mcp.server.fastmcp import FastMCP
import requests
import os
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("MCP_Weather")


@mcp.tool()
def get_Weather(LocationName: str) -> str:
    """
    取得該縣市天氣預報
    """
    # 將台替換為臺
    LocationName = LocationName.replace("台", "臺")

    API_Key = os.getenv("openWeatherAPIKey")
    API_URL = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={API_Key}&elementName=Wx,PoP,MaxT,MinT&locationName={LocationName}"
    res = requests.get(API_URL)
    data = res.json()

    # 訪問地點資料（因為它是一個JSON，所以需要使用索引）
    location_data = data["records"]["location"][0]

    city = location_data["locationName"]

    # 獲取天氣元素
    weather_element = location_data["weatherElement"]

    wx = []
    PoP = []
    MaxT = []
    MinT = []

    StartTime = weather_element[0]["time"][0]["startTime"]
    EndTime = weather_element[0]["time"][2]["endTime"]

    for i in range(3):
        wx.append(weather_element[0]["time"][i]["parameter"]["parameterName"])
        PoP.append(weather_element[1]["time"][i]["parameter"]["parameterName"])
        MaxT.append(weather_element[2]["time"][i]["parameter"]["parameterName"])
        MinT.append(weather_element[3]["time"][i]["parameter"]["parameterName"])

    datalist = {
        "城市": city,
        "開始觀測時間": StartTime,
        "結束觀測時間": EndTime,
        "降雨機率": PoP,
        "最低溫度": MinT,
        "最高溫都": MaxT,
    }

    return datalist
