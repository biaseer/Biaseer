
from datetime import datetime, timedelta

# read cameo file, denerate dict
def getCAMEOCodes(filename, INT=False):
    fr = open(filename)
    arrayLines = fr.readlines()
    cameoEventDict = {}
    for event in arrayLines[1:]:
        if INT:
            cameoEventDict[int(event.strip().split('\t')[0])] = event.strip().split('\t')[1]
        else:
            cameoEventDict[event.strip().split('\t')[0]] = event.strip().split('\t')[1]

    return cameoEventDict

def create_date_range(inp:list, isint=False):
    result_list = []
    sta_day = datetime.strptime(str(inp[0]), '%Y%m%d')
    end_day = datetime.strptime(str(inp[1]), '%Y%m%d')
    dlt_day = (end_day - sta_day).days + 1

    for i in range(dlt_day):
        tmp_day = sta_day + timedelta(days=i)
        tmp_day_txt = tmp_day.strftime('%Y%m%d')
        if isint:
            result_list.append(int(tmp_day_txt))
        else:
            result_list.append(tmp_day_txt)

    return result_list