import json
import urllib.request

########################################
# 1.获取搜索结果关键字为lake的Metagenome id
########################################
# 初始化请求地址
url = 'http://api.metagenomics.anl.gov/metagenome'
values = {}
values['verbosity'] = 'mixs'
# 搜索关键字为lake
values['metadata'] = 'lake'
# 排序方式
values['order'] = 'created'
# 结果倒序返回
values['direction'] = 'desc'
# 一次请求列表长度 20,100 或 500
values['limit'] = 500
values['offset'] = 0

params = urllib.parse.urlencode(values)
request_url = url + "?" + params

id_list = list()
while True:
    print("请求列表地址", request_url)
    response_data = urllib.request.urlopen(request_url, data=None, timeout=10).read().decode('UTF-8')
    response_obj = json.loads(response_data)
    offset = response_obj['offset']
    # 列表数据总长度
    total_count = response_obj['total_count']
    # prev = response_obj['prev']
    data = response_obj['data']
    for each in data:
        id_list.append(each['id'])
    # 下一个请求的url
    request_url = response_obj['next']
    s_url = urllib.parse.urlparse(request_url)
    query_params = urllib.parse.parse_qs(s_url.query)
    next_offset = query_params['offset']
    if int(next_offset[0]) >= total_count:
        break

########################################
# 2.下载
########################################
download_page_url = 'http://api.metagenomics.anl.gov/annotation/similarity/'
# 下载的数据是Annotation type 为function,数据来源KEGG, 账号为...
params = 'type=function&source=KEGG&auth=mgrast%20HzMXFGDcmjSBgQtniFz5YDTXr&browser=1'
for each in id_list:
    request_url = download_page_url + each + "?" + params
    print("下载地址为", request_url)
    file_name = each
    u = urllib.request.urlopen(request_url)

    file_size_dl = 0
    block_sz = 1024 * 1024
    f = open(file_name, 'wb')
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break
        file_size_dl += len(buffer)
        f.write(buffer)
    f.close()

