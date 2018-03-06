#coding:utf-8
"""
huyifeng@baidu.com
"""
import os
import sys
import MySQLdb

def dump(data): 
    db = MySQLdb.connect("192.168.0.107", "root", "384259", "tianchi" )
    cursor = db.cursor()
    sql = """
insert ignore into round1_ijcai_18_train_20180301(
instance_id,item_id,item_category_list,
item_property_list,
item_brand_id,
item_city_id,
item_price_level,
item_sales_level,
item_collected_level,
item_pv_level,
user_id,
user_gender_id,
user_age_level,
user_occupation_id,
user_star_level,
context_id,
context_timestamp,
context_page_id,
predict_category_property,
shop_id,
shop_review_num_level,shop_review_positive_rate,shop_star_level,shop_score_service,shop_score_delivery,shop_score_description,is_trade)
values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
    """
    try:
       cursor.executemany(sql, data)
       db.commit()
    except Exception as e:
       print str(e)
       db.rollback()
    db.close()
    print '.',

if __name__ == '__main__': 
    data = []
    with open('train1.txt', 'r') as f: 
        for l in f.readlines(): 
            (
                instance_id, 
                item_id, 
                item_category_list,
                item_property_list, 
                item_brand_id, 
                item_city_id, 
                item_price_level,
                item_sales_level, 
                item_collected_level, 
                item_pv_level, 
                user_id,
                user_gender_id, 
                user_age_level, 
                user_occupation_id, 
                user_star_level, 
                context_id, 
                context_timestamp, 
                context_page_id, 
                predict_category_property, 
                shop_id, 
                shop_review_num_level,
                shop_review_positive_rate, 
                shop_star_level,
                shop_score_service, 
                shop_score_delivery, 
                shop_score_description, 
                is_trade) = l.strip().split(' ')
            data.append((
                int(instance_id), 
                int(item_id), 
                item_category_list,
                item_property_list, 
                int(item_brand_id), 
                int(item_city_id), 
                int(item_price_level),
                int(item_sales_level), 
                int(item_collected_level), 
                int(item_pv_level), 
                int(user_id),
                int(user_gender_id), 
                int(user_age_level), 
                int(user_occupation_id), 
                int(user_star_level), 
                int(context_id), 
                int(context_timestamp), 
                int(context_page_id), 
                predict_category_property, 
                int(shop_id), 
                int(shop_review_num_level),
                float(shop_review_positive_rate), 
                int(shop_star_level),
                float(shop_score_service), 
                float(shop_score_delivery), 
                float(shop_score_description), 
                int(is_trade)))
            if len(data) > 1000: 
                dump(data)
                data = []
    dump(data)
