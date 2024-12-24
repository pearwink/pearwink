import urllib.request, json
import pandas as pd

# โหลดรายการกองทุนจาก Excel
fund_list = pd.read_excel("fund_list.xlsx")

try:
    date = "2023-10-31"  # แทนด้วยวันที่ที่ต้องการ

    hdr = {
        'Cache-Control': 'no-cache',
        'Ocp-Apim-Subscription-Key': '0a1bf8ae03db4c4c9b23324feb8ee1f8',
    }

    data_frames = []

    for index, row in fund_list.iterrows():
        proj_id = row['proj_id']
        fund_status = row['fund_status']

        if fund_status == 'RG':
            url = f"https://api.sec.or.th/FundDailyInfo/{proj_id}/dailynav/{date}"
            req = urllib.request.Request(url, headers=hdr)
            req.get_method = lambda: 'GET'
            response = urllib.request.urlopen(req)
            print(f"ดึงข้อมูลสำหรับ proj_id {proj_id}: {response.getcode()}")

            try:
                data = json.loads(response.read())
                if data:
                    df = pd.json_normalize(data)  # แปลง JSON เป็น DataFrame
                    df['proj_id'] = proj_id
                    data_frames.append(df)
            except json.JSONDecodeError as json_error:
                print(f"เกิดข้อผิดพลาดในการแปลง JSON สำหรับ proj_id {proj_id}: {json_error}")

    if data_frames:
        all_data = pd.concat(data_frames, ignore_index=True)
        all_data.to_excel("fund_data.xlsx", index=False)  # บันทึกเป็น Excel

except Exception as e:
    print(e)
