import urllib.request
import json
import pandas as pd

try:
    url = "https://api.sec.or.th/FundFactsheet/fund/M0204_2542/FundPort/202303"

    hdr = {
        'Cache-Control': 'no-cache',
        'Ocp-Apim-Subscription-Key': '0b181e9a224a4572bd91077cb223465a',
    }

    req = urllib.request.Request(url, headers=hdr)
    req.get_method = lambda: 'GET'
    response = urllib.request.urlopen(req)

    if response.getcode() == 200:
        data = json.loads(response.read())
        if data:
            df = pd.json_normalize(data)  # แปลง JSON เป็น DataFrame
            df.to_excel("SMARTMF.xlsx", index=False)  # บันทึกเป็น Excel

except Exception as e:
    print(e)
