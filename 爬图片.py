import requests # 爬虫必备
import time # 限制爬虫速度
import os # 新建指定存储文件夹


def get_ip():
    """获取代理IP"""
    # （注意：下面代理URL，看4.2教程换成自己的API链接）：
    url = "这里放你自己代理IP的API链接"
    while 1:
        try:
            r = requests.get(url, timeout=10)
        except:
            continue

        ip = r.text.strip()
        if '请求过于频繁' in ip:
            print('IP请求频繁')
            time.sleep(1)
            continue
        break
    proxies = {
        'https': '%s' % ip
    }

    return proxies



def get_img_url(keyword):
    """发送请求，获取接口中的数据"""
    # 接口链接
    url = 'https://image.baidu.com/search/acjson?'
    # 请求头模拟浏览器
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
    # 构造网页的params表单
    params = {
        'tn': 'resultjson_com',
        'logid': '6918515619491695441',
        'ipn': 'rj',
        'ct': '201326592',
        'is': '',
        'fp': 'result',
        'queryWord': f'{keyword}',
        'word': f'{keyword}',
        'cl': '2',
        'lm': '-1',
        'ie': 'utf-8',
        'oe': 'utf-8',
        'adpicid': '',
        'st': '-1',
        'z': '',
        'ic': '',
        'hd': '',
        'latest': '',
        'copyright': '',
        's': '',
        'se': '',
        'tab': '',
        'width': '',
        'height': '',
        'face': '0',
        'istype': '2',
        'qc': '',
        'nc': '1',
        'fr': '',
        'expermode': '',
        'force': '',
        'cg': 'girl',
        'pn': 1,
        'rn': '30',
        'gsm': '1e',
    }
    # 携带请求头和params表达发送请求
    response  = requests.get(url=url, headers=headers, params=params)
    # 设置编码格式
    response.encoding = 'utf-8'
    # 转换为json
    json_dict = response.json()
    # 定位到30个图片上一层
    data_list = json_dict['data']
    # 删除列表中最后一个空值
    del data_list[-1]
    # 用于存储图片链接的列表
    img_url_list = []
    for i in data_list:
        img_url = i['thumbURL']
        # 打印一下图片链接
        print(img_url)
        img_url_list.append(img_url)
    # 返回图片列表
    return img_url_list


def get_down_img(img_url_list,keyword):
    # 在当前路径下生成存储图片的文件夹
    os.mkdir(f'{keyword}')
    # 定义图片编号
    n = 0
    for img_url in img_url_list:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
        # 调用get_ip函数，获取代理IP
        # proxies = get_ip()
        # 每次发送请求换代理IP，获取图片，防止被封
        img_data = requests.get(url=img_url, headers=headers).content
        # 拼接图片存放地址和名字
        img_path = f'./{keyword}/' + str(n) + '.jpg'
        # 将图片写入指定位置
        with open(img_path, 'wb') as f:
            f.write(img_data)
        # 图片编号递增
        n = n + 1



if __name__ == '__main__':
    # 1. 修改关键词
    keyword = '美女头像'
    # 2. 获取指定关键词的图片链接
    img_url_list = get_img_url(keyword)
    # 3. 下载图片到指定位置
    get_down_img(img_url_list,keyword)
