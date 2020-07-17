import requests,json
# 搜索公司
def searchCompany(str):
    response = None
    while (response == None or len(response.text) == 0):
        url = "http://app.gsxt.gov.cn/gsxt/cn/gov/saic/web/controller/PrimaryInfoIndexAppController/search?page=1"
        payload = "{\"searchword\":\""+str+"\",\"conditions\":{\"excep_tab\":\"0\",\"ill_tab\":\"0\",\"area\":\"0\",\"cStatus\":\"0\",\"xzxk\":\"0\",\"xzcf\":\"0\",\"dydj\":\"0\"},\"sourceType\":\"I\"}"
        headers = {
            'Content-Type': 'application/json;charset=utf-8',
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Html5Plus/1.0',
            'Accept-Language': 'zh-cn',
            'Accept-Encoding': 'gzip,deflate',
            'X-Requested-With': 'XMLHttpRequest',
            'Cookie': 'JSESSIONID=65E388078D2AD812DC07B3D2C30956BD; __jsluid_h=171aaf9744cb5a036917ece969b31951; SECTOKEN=7408288245531542052; tlb_cookie=172.16.12.1108080'
        }
        response = requests.request("POST", url, headers=headers, data=payload.encode('utf-8'))
    return response.text

# 查询股本情况
def searchInv(pripid,nodeNum):
    response = None
    while (response == None or len(response.text) == 0):
        url = "http://app.gsxt.gov.cn/gsxt/corp-query-entprise-info-shareholder-"+pripid+".html?nodeNum="+nodeNum+"&entType=1&start=0&sourceType=I"
        print(url)
        payload = {}
        # 需要设置UA，否则会被识别为攻击请求
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Html5Plus/1.0',
            'Cookie': 'JSESSIONID=65E388078D2AD812DC07B3D2C30956BD; __jsluid_h=171aaf9744cb5a036917ece969b31951; SECTOKEN=7408288245531542052; tlb_cookie=172.16.12.1108080'
        }
        response = requests.request("POST", url, headers=headers, data = payload)

    return response.text

def get_info(str):
    try:
        resp=searchCompany(str)
        tdict=get_comp_data(resp)
        if tdict['hasRecord']==False:
            return tdict
        resp = searchInv(tdict['pripid'], tdict['nodeNum'])
        tdict['inv']=get_inv_data(resp)
        return tdict
    except:
        return None

def get_comp_data(resp):
    print(resp)
    jsonresp=json.loads(resp)
    # 获取第一条记录
    data=jsonresp['data']['result']['data']
    if len(data)==0:
        return {'hasRecord':False}

    # 登记状态
    corpStatusString=jsonresp['data']['result']['data'][0]['corpStatusString']
    # pripid
    pripid=jsonresp['data']['result']['data'][0]['pripid']
    # 社会统一信用代码
    uniscId=jsonresp['data']['result']['data'][0]['uniscId']
    # 法人
    legelRep=jsonresp['data']['result']['data'][0]['legelRep']
    # nodenum
    nodeNum=jsonresp['data']['result']['data'][0]['nodeNum']
    # 成立日期
    estDate=jsonresp['data']['result']['data'][0]['estDate']
    # 注册资本
    regCap=str(jsonresp['data']['result']['data'][0]['regCap'])+'万人民币'

    return {'corpStatusString':corpStatusString,'uniscId':uniscId,'pripid':pripid,'legelRep':legelRep,'nodeNum':nodeNum,'estDate':estDate,'regCap':regCap,'hasRecord':True}

def get_inv_data(resp):
    print(resp)
    jsonresp = json.loads(resp)
    invlist=jsonresp['data']
    print(len(invlist))
    resStr=''
    for temp in invlist:
        resStr=resStr+temp['inv']+'\t'+temp['invType_CN']+'\t'+temp['country_CN']+'\t认缴'+str(temp['liSubConAm'])+'万元'+'\t实缴'+str(temp['liAcConAm'])+'万元\n'
    return resStr