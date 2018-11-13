from urllib import parse, request
from pythonweb.settings import conf
import json

acess_token = conf.get('baidu', 'access_token')
def ocr(imageurl):
    data = {}
    data['url'] = imageurl
    data = parse.urlencode(data).encode('utf-8')
    header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
                   "Content-Type": "application/x-www-form-urlencoded"}
    url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=' + acess_token;
    req = request.Request(url=url, data=data, headers=header_dict)
    res = request.urlopen(req)
    res_json = res.read().decode('utf-8')
    res_json = json.loads(res_json)
    ret = ''
    for words in res_json['words_result']:
        ret = ret + words['words'] + '\n'
    return  ret


if __name__=='__main__':
    imageurl='http://mmbiz.qpic.cn/mmbiz_jpg/twZicTD718boWv1nTFtDSpPOZjAzaC2kJF5sRiap2RPBTb5263vAknOXOfF75ibeglpG8OPWoeVAiayegkibwLgLjQA/0'
    print(ocr(imageurl))
