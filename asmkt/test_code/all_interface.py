# coding:utf-8


import json, requests
from asmkt.com.operate_csv import Operate_csv
from asmkt.com.asmkt_aes import Aes
from bs4 import BeautifulSoup
from asmkt.com.operate_yaml import OperateYaml


class AsmktOpenApi(object):

    def __init__(self, Asmkt_api_url, Lottery_url, GiftCoupon_path, Lottery_path, SubOrder_path, secreykey, appId, ActivityId, ProductId):
        self.Asmkt_api_url = Asmkt_api_url
        self.Lottery_url = Lottery_url

        self.GiftCoupon_path = GiftCoupon_path
        self.Lottery_path = Lottery_path
        self.SubOrder_path = SubOrder_path

        self.secreykey = secreykey
        self.appId = appId

        self.ActivityId = ActivityId
        self.ProductId = ProductId


    def get_code_url(self, sign_list):
        '''获取发码链接 '''
        req_urls = []
        for i in range(len(sign_list)):
              # 用来存放生成的短链
            data = {
                "appId":self.appId,
                "data": eval(sign_list[i][0])
            }
            try:
                req = requests.get(self.Asmkt_api_url+self.GiftCoupon_path, params=data)
                req_text = req.text
                req_url = list(json.loads(req_text)["data"]["coupons"].values())[0]
                if req_url:
                    req_urls.append(req_url)
            except KeyError:
                print("该业务单已存在")
        return req_urls

    def activityCode_EqulityId(self, code_url):
        '''打开链接'''
        ActivityCode = []
        EqulityId = []
        req = requests.get(code_url)
        cookies = requests.utils.dict_from_cookiejar(req.cookies)
        ActivityCode.append(cookies["ActivityCode"])
        EqulityId.append(cookies["EqulityId"])
        return ActivityCode, EqulityId
#
    def get_userCouponId_productId(self, equityId, activityCode):
        '''生成权益码链接'''
        userCouponId = []
        productId = []
        payload = {
            "equityId": equityId,
            "activityCode": activityCode,
            # "inputId": ""  # 非必填
        }
        req = requests.get(self.Lottery_url+self.Lottery_path, params=payload)
        userCouponId.append(req.json()["data"]["userCouponId"])
        productId.append(req.json()["data"]["productId"])
        return userCouponId, productId
#
    def  asmktProductId(self, productId, EqulityIds, userCouponId):
        # {productId}/{equityId}
        url = self.Lottery_url + "/Product/Detail/"+ productId + "/" + EqulityIds + "?userCouponId="+ userCouponId
        req = requests.get(url)
        html = req.text

        bf = BeautifulSoup(html, "html.parser")
        script = bf.find_all("script")
        scpirt_text = script[-1].text
        AsmktProductId = scpirt_text.split(",            ")[2].split('"')[1]
        return AsmktProductId

    def asmkt_SubOrder(self, EqulityIds, productId, AsmktProductId, userCouponId):
        '''下单接口'''
        data = {
            "EquityId": EqulityIds,
            "ProductId": productId,
            "AsmktProductId": AsmktProductId,
            "AddressId": 0,
            "Memo": "",
            "CouponIdList": userCouponId
        }
        req = requests.post(self.Lottery_url + self.SubOrder_path, params=data)
        if '"isSuccess":true'in req.text:
            pass
        return json.loads(req.text)['data']


if __name__ == '__main__':
    o = OperateYaml(r"F:\mycode\asmkt\config\urls.yaml")

    Asmkt_api_url = o.read_yaml()[0]['Asmkt_api_url']
    GiftCoupon_path = o.read_yaml()[0]['GiftCoupon_path']

    GiftCoupon_url = o.read_yaml()[1]["GiftCoupon_url"]
    Lottery_path = o.read_yaml()[1]['Lottery_path']

    SubOrder_url = o.read_yaml()[2]['SubOrder_url']
    SubOrder_path = o.read_yaml()[2]['SubOrder_path']

    secreyKey = o.read_yaml()[3]['secreykey']
    appId = o.read_yaml()[4]['appId']
    ActivityId = o.read_yaml()[5]['ActivityId']
    ProductId = o.read_yaml()[6]['ProductId']

    operate_csv = Operate_csv("sign.csv", "key", Aes(secreyKey, appId, ActivityId, ProductId).aes_list())
    operate_csv.write_csv()
    signs = operate_csv.read_csv()

    Asmkt  = AsmktOpenApi(Asmkt_api_url, GiftCoupon_url, GiftCoupon_path, Lottery_path, SubOrder_path, secreyKey, appId, ActivityId, ProductId)

    activityCode_EqulityIds = Asmkt.activityCode_EqulityId(Asmkt.get_code_url(signs)[0])
    activityCode = activityCode_EqulityIds[0][0]
    EqulityIds = activityCode_EqulityIds[1][0]

    userCouponId_productIds = Asmkt.get_userCouponId_productId(EqulityIds, activityCode)
    userCouponId = userCouponId_productIds[0][0]
    productId = userCouponId_productIds[1][0]
    AsmktProductId = Asmkt.asmktProductId(productId, EqulityIds, userCouponId)

    SubOrder = Asmkt.asmkt_SubOrder(EqulityIds, productId, AsmktProductId, userCouponId)
    print("下单成功，订单号为：", SubOrder)

