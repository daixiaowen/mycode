# coding:utf-8


import base64, hashlib, json, time
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES


class Aes(object):
    def __init__(self, secreykey, AppId, ActivityId, ProductId):
        self.secreykey = secreykey
        self.AppId = AppId
        self.ActivityId =  ActivityId
        self.ProductId = ProductId
        self.businessno = input("请输入订单号")
        self.num = input("请输入订单数量")

    def get_timestamp(self):
        '''
        获取时间戳
        :return:
        '''
        return int(time.time())


    def get_business_no(self):
        '''
        批量生成业务单号
        :param businessno: 订单号前半部分
        :param num: 生成订单号数量
        :return:
        '''
        businessNo = []
        if self.num.isdigit():
            num = int(self.num)
            for i in range(0, num):
                s = self.businessno + str(i)
                businessNo.append(s)
        else:
            print("请输入正确的订单数量")
        return businessNo

    def get_md5(self):
        '''
        生成md5
        :param businessno:业务单号
        :param timestamp: 时间戳（10位）
        :return:
        '''
        md_list = []
        for business_no in self.get_business_no():
            sign = "appid="+ self.AppId +"&activityid="+self.ActivityId + "&" \
                   "productid="+ self.ProductId + "&quantity=1&phoneno=&businessno=" + \
                   business_no + "&timestamp=" + str(self.get_timestamp()) + "&secretkey=" + self.secreykey
            str_md5 = hashlib.md5(sign.encode("utf-8")).hexdigest()
            md_list.append(str(str_md5).upper())
        return md_list

    def aes_str(self):
        '''生成加密字符串'''
        L = []
        for i in range(len(self.get_business_no())):
            data = {
                    "AppId": self.AppId,
                    "ActivityId": self.ActivityId,
                    "ProductId": self.ProductId,
                    "Quantity": "1",
                    "PhoneNo": "",
                    "BusinessNo": self.get_business_no()[i],
                    "ExpirationDate": "2019-12-30 00:00:00",
                    "Timestamp": self.get_timestamp(),
                    "Sign": self.get_md5()[i]
                    }
            aes_str = json.dumps(data)
            L.append(aes_str)
        return L

    def aes_cipher(self):
        # 使用key,选择加密方式
        # iv = \0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0
        encrypted_text_str_list = []  # 定义一个空列表，用来存放生成的签名
        for i in self.aes_str():
            aes = AES.new(self.secreykey.encode('utf-8'), AES.MODE_CBC, iv="0000000000000000".encode())
            pad_pkcs7 = pad(i.encode('utf-8'), AES.block_size, style='pkcs7')  # 选择pkcs7补全
            encrypt_aes = aes.encrypt(pad_pkcs7)
            # 加密结果
            encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')  # 解码
            encrypted_text_str = encrypted_text.replace("\n", "")  # 此处我的输出结果老有换行符，所以用了临时方法将它剔除
            encrypted_text_str_list.append(encrypted_text_str)
        return encrypted_text_str_list

    def aes_list(self):
        return [[aes] for aes in self.aes_cipher()]
