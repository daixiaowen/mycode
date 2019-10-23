# coding:utf-8


# import hashlib
# from asmkt.com.timestamp import get_timestamp
# from asmkt.com.asmkt_businessno import get_business_no, businessno, num
#
#
# def get_md5():
#      '''
#      生成md5
#      :param businessno:业务单号
#      :param timestamp: 时间戳（10位）
#      :return:
#      '''
#      md_list = []
#      for business_no in get_business_no(businessno, num):
#           sign = "appid=ce01f096-8bd2-4d9d-a400-08d73727eeb9&activityid=d8d40708-866a-42c6-602b-08d7117a4079&" \
#                  "productid=c3d73ccb-c9e4-47c0-d401-08d6bbee46e1&quantity=1&phoneno=&businessno=" + \
#                  business_no + "&timestamp=" + str(get_timestamp()) + "&secretkey=9b2ef12f4bf747fca466e5a45da3c951"
#           str_md5 = hashlib.md5(sign.encode("utf-8")).hexdigest()
#           md_list.append(str(str_md5).upper())
#      return md_list


