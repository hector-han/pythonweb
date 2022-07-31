import requests
import json


TAG_MAPPING = {
    'O': '冗余',
    'POI': '兴趣点',
    'poi': '兴趣点',
    'assist': '辅助信息',
    'cellno': '单元号',
    'city': '城市',
    'community': '社区/村',
    'devzone': '开发区',
    'distance': '距离',
    'district': '区县',
    'floorno': '楼层',
    'houseno': '楼号',
    'intersection': '楼号',
    'prov': '省',
    'road': '道路',
    'roomno': '户室号',
    'subpoi': '子兴趣点',
    'town': '乡镇',
    'village_group': '村小组',
}


def get_geo_result(address: str, sep='\n') -> str:
    url = "http://localhost:8000/GeoService/Geocoding"
    data = {
        "address": address
    }
    resp = requests.post(url, json=data)
    """
    {"response":"{\"addr_analysis\":[{\"word\":\"北京市\",\"tag\":\"city\"},{\"word\":\"昌平区\",\"tag\":\"district\"}]}"}
    """
    resp = json.loads(resp.text)
    resp = json.loads(resp["response"])
    addr_analysis = resp["addr_analysis"]

    lst_pair = []
    for obj in addr_analysis:
        word, label = obj["word"], obj["tag"]
        if label in TAG_MAPPING:
            label = TAG_MAPPING[label]
        lst_pair.append((word, label))
    
    return sep.join([
        f'{pair[0]}: {pair[1]}' for pair in lst_pair
    ])

if __name__ == '__main__':
    address = "北京市昌平区"
    ret = get_geo_result(address)
    print(ret)