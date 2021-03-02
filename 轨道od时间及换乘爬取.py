import pandas as pd
import urllib.request
import urllib
import json
import datetime
start_time=datetime.datetime.now()
raw=pd.read_excel(r'12344.xlsx',sheet_name='Sheet4',encoding='utf8')
print(raw.keys())
f=open(r'result.txt','w+')
start_station=raw['3上车站点'];
start_lon=raw['上车车站经度'];
start_lat=raw['上车车站纬度']
end_station=raw['3下车站点']
end_lon=raw['下车车站经度']
end_lat=raw['下车车站纬度']
output=pd.DataFrame(columns=['start_station','end_station','duration(s)','change_times'])
print(raw.ix[0,'3上车站点'])
for i in range(raw.shape[0]):
# for i in range(10):
    url_base=r'http://api.map.baidu.com/direction/v2/transit?'
    url_append=r'origin='+str(start_lat[i])+r','+str(start_lon[i])+'&'+'destination='+str(end_lat[i])+r','+str(end_lon[i])+r'&coord_type=wgs84&tactics_incity=5'+'&ak=5xe4hecLjnGio0qnot4aS1RAkpqYsGHs'
    url=url_base+url_append
    zidian = {}
    try:
        data=urllib.request.urlopen(url,timeout=1).read()
    except:
        zidian['start_station'] = raw.ix[i, '3上车站点']
        zidian['end_station'] = raw.ix[i, '3下车站点']
        zidian['duration(s)'] = 'None'
        zidian['change_times'] = 'None'
        output = output.append(zidian, ignore_index=True)
        continue
    datainfo=json.loads(data)
    # print(type(datainfo))
    # print(datainfo)
    # print('时间:',sep='\t')
    # print(datainfo['result']['routes'][0]['duration'])    #第一条路径时间
    # print('第一条路径详情:',sep='\t')
    # print(datainfo['result']['routes'][0])
    print(i)
    if ('result' in datainfo.keys()) and ('routes' in datainfo['result'].keys()):
        try:
            result_str = str(datainfo['result']['routes'][0])
            zidian['change_times'] = result_str.count('\'type\': 1') - 1
        except:
            result_str=''
            zidian['change_times'] = result_str.count('\'type\': 1') - 1
        zidian['start_station'] = raw.ix[i, '3上车站点']
        zidian['end_station'] = raw.ix[i, '3下车站点']
        try:
            zidian['duration(s)'] = datainfo['result']['routes'][0]['duration']
        except:
            zidian['change_times'] = 'None'
    else:
        zidian['start_station'] = raw.ix[i, '3上车站点']
        zidian['end_station'] = raw.ix[i, '3下车站点']
        zidian['duration(s)'] = 'None'
        zidian['change_times'] = 'None'
    output=output.append(zidian,ignore_index=True)
output.to_excel('output-type1.xlsx')
end_time=datetime.datetime.now()
print('时间：',sep='')
print(end_time-start_time)




