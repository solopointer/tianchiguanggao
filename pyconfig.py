import py_feature_map
import py_feature_number

FEATURE_CONFIG = [
    py_feature_map.feature({'file': '/home/work/huyifeng/item_item_id.txt', 'index': 1}),
    #py_feature_map.feature({'file': '/home/work/huyifeng/item_user_id.txt', 'index': 10}),
    py_feature_map.feature({'file': '/home/work/huyifeng/item_shop_id.txt', 'index': 19}),
    py_feature_map.feature({'file': '/home/work/huyifeng/item_brand_id.txt', 'index': 4}),
    py_feature_map.feature({'file': '/home/work/huyifeng/item_city_id.txt', 'index': 5}),
    py_feature_number.feature({'index': 6}),#item_price_level
    py_feature_number.feature({'index': 7}),#item_sales_level
    py_feature_number.feature({'index': 8}),#item_collected_level
    py_feature_number.feature({'index': 9}),#item_pv_level
    py_feature_map.feature({'file': '/home/work/huyifeng/user_gender_id.txt', 'index': 11}),
    py_feature_number.feature({'index': 12}),#user_age_level
    py_feature_map.feature({'file': '/home/work/huyifeng/user_occupation_id.txt', 'index': 13}),
    py_feature_number.feature({'index': 14}),#user_star_level
    py_feature_number.feature({'index': 17}),#context_page_id
    py_feature_number.feature({'index': 20}),#shop_review_num_level
    py_feature_number.feature({'index': 21}),#shop_review_positive_rate
    py_feature_number.feature({'index': 22}),#shop_star_level
    py_feature_number.feature({'index': 23}),#shop_score_service
    py_feature_number.feature({'index': 24}),#shop_score_delivery
    py_feature_number.feature({'index': 25}),#shop_score_description
]
