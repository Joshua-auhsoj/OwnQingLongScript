import requests
import os
import xml.etree.ElementTree as ET

cookie_value = os.getenv('COOKIE')
cookies = {cookie.split('=')[0]: cookie.split('=')[1] for cookie in cookie_value.split('; ')}


url = 'http://你的反代地址/plugin.php'
#如果使用自己的域名请使用https，如果使用CloudFlare反代，可正常裸连使用https，如果更改host裸连只能使用http

common_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cookie': cookie_value,
    'priority': 'u=0, i',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
#UA值需要随着抓取Cookie的浏览器更改

}

a_headers = common_headers.copy()
a_headers.update({
    'referer': url + '?H_name-tasks-actions-newtasks.html.html'
})

c_headers = common_headers.copy()
c_headers.update({
    'authority': 'south-plus.net',
    'method': 'GET',
    'path': '/plugin.php?H_name-tasks-actions-newtasks.html.html',
    'scheme': 'https',
    'Referer': url + '?H_name-tasks.html.html'
})

common_params = {
    'H_name': 'tasks',
    'action': 'ajax',
    'nowtime': '1717167492479',
    'verify': '5af36471',
}

ad_params = common_params.copy()
ad_params.update({
    'actions': 'job',
    'cid': '15',
})

aw_params = common_params.copy()
aw_params.update({
    'actions': 'job',
    'cid': '14',
})

cd_params = common_params.copy()
cd_params.update({
    'actions': 'job2',
    'cid': '15',
})

cw_params = common_params.copy()
cw_params.update({
    'actions': 'job2',
    'cid': '14',
})


def tasks(url, params, headers, type):
    response = requests.get(url, params=params, headers=headers)
   # print(response.text)
    response.encoding = 'utf-8'
    data = response.text

    # 解析XML数据
    root = ET.fromstring(data)
    cdata = root.text

    # 提取变量值
    values = cdata.split('\t')
    if ('申请' in type):
        value_len = 2
    else:
        value_len = 3
    if len(values) == value_len:
        message = values[1]

        print(type + message)
    else:
        raise Exception("XML格式不正确，请检查COOKIE设置")
    if ("还没超过" in message):
        return False
    else:
        return True


if (tasks(url, ad_params, a_headers, "申请-日常: ")):
    tasks(url, cd_params, c_headers, "完成-日常: ")
if (tasks(url, aw_params, a_headers, "申请-周常: ")):
    tasks(url, cw_params, c_headers, "完成-周常: ")
