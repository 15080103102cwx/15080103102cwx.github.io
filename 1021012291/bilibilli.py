import requests
import os
import re
import pandas as pd
import json
import chardet

def get_search(v_keyword,v_max_page,v_out_file):
    global title_list, danmaku_list, arcurl_list,bvid_list
    for page in range(1,v_max_page,1):
        print('开始爬取第{}页'.format(page))
        #请求地址（从第二页开始看）
        url = 'https://api.bilibili.com/x/web-interface/wbi/search/type'
        #请求头
        headers = {
            'accept':'application/json, text/plain, */*',
            'Accept-Encoding':'gzip, deflate, br',               'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cookie':"buvid3=27612A9A-4409-4CB8-B5A2-B5FE22F7C714148794infoc; i-wanna-go-back=-1; CURRENT_BLACKGAP=0; buvid4=2CA5ACE4-295D-7772-FB8B-C0A06A60665F90100-022020118-SK3hbof5R8mA9Ukmq5zeFp99XYPztqLVHluDnkRagNg43EzvnpXG1A%3D%3D; LIVE_BUVID=AUTO6816437129869560; buvid_fp_plain=undefined; DedeUserID=475406798; DedeUserID__ckMd5=2998e8f1222af4aa; is-2022-channel=1; b_nut=100; rpdid=|(u))kkYu|mY0J'uYYmu|mkuR; CURRENT_QUALITY=120; header_theme_version=CLOSE; b_ut=5; CURRENT_PID=2c4dbba0-cc82-11ed-a533-b3a5b2a29c1d; nostalgia_conf=-1; FEED_LIVE_VERSION=V8; home_feed_column=5; CURRENT_FNVAL=4048; fingerprint=21d70c1855e1a7049764c753e0be7da1; buvid_fp=d2827a3343fa2d5cbf6610e32e6b2218; _uuid=CAC1097BA-979F-E266-A31A-5102769986EBB70032infoc; SESSDATA=7ed367e9%2C1709375372%2C2fd35%2A92l2u1PmWvfRrYRFZDxq5Rrv4LSRorZUS5Bqf3obOCts5FPhbbQrTL62qrR7or8hjxHob91QAAYgA; bili_jct=c5158e1ef1e84f7f82b62d033ce10ecd; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTQwODI1NzMsImlhdCI6MTY5MzgyMzM3MywicGx0IjotMX0.uJ-0bTEsQrBEKOeNIY9ZRgBH-kl5W1FyzmgksColWNw; bili_ticket_expires=1694082573; b_lsid=F9410EF35_18A6A07CEC3; sid=6v9h5s2l; bp_video_offset_475406798=838211843349545064; browser_resolution=1484-742; PVID=5",
            'origin':'https://search.bilibili.com',
            'Referer':'https://search.bilibili.com/all?',
            'Sec-Ch-Ua':'"Chromium";v="116", "Not)A;Brand";v="24", "Microsoft Edge";v="116"',
            'Sec-Ch-Ua-Mobile':'?0',
            'Sec-Ch-Ua-Platform':'"Windows"',
            'Sec-Fetch-Dest':'empty',
            'Sec-Fetch-Mode':'cors',
            'Sec-Fetch-Site':'same-site',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69',
        }
        params = {
            '__refresh__': 'true',
            '_extra':' ',
            'context':' ',
            'page':page,
            'page_size': 42,
            'from_source':'',
            'from_spmid': '333.337',
            'platform': 'pc',
            'highlight': '1',
            'single_column':'0' ,
            'keyword': v_keyword,
            'qv_id': 'NJWpAA4K37OTOu7qrI4xNXsv5w4nG6pA',
            'ad_resource': '5654',
            'source_tag': '3',
            'gaia_vtoken':'',
            'category_id':'',
            'search_type': 'video',
            'dynamic_offset': 24*(page-1),
            'web_location': '1430654',
        }
        r = requests.get(url,headers=headers,params=params)
        print(r.status_code)    #查看响应码
        j_data = r.json()       #获得json文件
        data_list = j_data['data']['result']    #
        print('数据长度：',len(data_list))
        title_list = []         #标题
        danmaku_list = []       #弹幕数
        arcurl_list = []        #网址
        bvid_list = []          #bivd
        page_list = []
        for data in data_list:
            title = re.compile(r'<[^>]+>',re.S).sub('',data['title'])
            title_list.append(title)
            danmaku_list.append(data['danmaku'])
            arcurl_list.append(data['arcurl'])
            bvid_list.append(data['bvid'])
            page_list.append(page)
        danmaku_file_name = '弹幕汇总.cvs'.format()
        danmaku_file(bvid_list, danmaku_file_name)
        get_file(title_list,danmaku_list,arcurl_list,bvid_list,page_list,v_out_file)

def get_file(v_title_list,v_danmaku_list,v_arcurl_list,v_bvid_list,v_page_list,v_out_file):
    df = pd.DataFrame(
        {
            '视频标题': v_title_list,
            '弹幕数': v_danmaku_list,
            '网址': v_arcurl_list,
            'bvid': v_bvid_list,
            '页数': v_page_list
        }
    )
    csv_header = ['视频标题', '弹幕数', '网址', 'bvid','页数']
    if os.path.exists(v_out_file):
        header = None  # 如果文件存在，直接写在后面
    else:  # 如果文件不存在，需写入字段标题
        header = csv_header  # 数据保存到csv文件
    df.to_csv(v_out_file, encoding='utf_8_sig', mode='a+', index=False, header=header)

def danmaku_file(v_bvid_list,v_out_file):
    for v_bvid in v_bvid_list:
        cid = get_cid(v_bvid)
        data = get_danmaku(cid)
        get_danmaku_file(data,v_out_file)

def get_danmaku_file(data,v_file):
    with open(v_file,mode='a+',encoding='utf-8') as f:
        for i in data:
            f.write(i)
            f.write('\n')
def get_cid(v_bvid):
    cvid_url = 'https://api.bilibili.com/x/player/pagelist?bvid='+str(v_bvid)
    response = requests.get(cvid_url)
    j_data = response.json()
    return j_data["data"][0]["cid"]

def get_danmaku(v_cvid):
    danmaku_url = "https://api.bilibili.com/x/v1/dm/list.so?oid="+str(v_cvid)
    response = requests.get(danmaku_url)
    response.encoding = 'utf-8'
    data = re.findall('<d p=".*?">(.*?)</d>',response.text)
    return data

if __name__ == '__main__':
    #搜索关键词
    search_keyword = '日本核污染水排海'
    #爬取最大页数
    max_page  = 10
    #保存文件名
    result_file = 'B站视频_{}_前{}页.cvs'.format(search_keyword,max_page)
    #开始爬取
    get_search(v_keyword=search_keyword.encode('utf8'),
               v_max_page=max_page,
               v_out_file=result_file)
