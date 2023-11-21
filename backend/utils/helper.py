from datetime import datetime, timedelta
import json

def create_date_range(inp:list):
    result_list = []
    sta_day = datetime.strptime(str(inp[0]), '%Y%m%d')
    end_day = datetime.strptime(str(inp[1]), '%Y%m%d')
    dlt_day = (end_day - sta_day).days + 1

    for i in range(dlt_day):
        tmp_day = sta_day + timedelta(days=i)
        tmp_day_txt = tmp_day.strftime('%Y%m%d')
        result_list.append(tmp_day_txt)

    return [ele[:4] + '-' + ele[4:6] +'-'+ ele[6:] for ele in result_list]


def saveDictoJson(dictsample={'a':1}, title='a1'):
    with open(title + ".json", "w") as f:
        f.write(json.dumps(dictsample, ensure_ascii=False, indent=4, separators=(',', ':')))

def readJsontoDict(filename):
    with open(filename, 'r') as fp:
        result = json.load(fp)
    return result