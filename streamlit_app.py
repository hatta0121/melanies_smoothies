# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!"""
)

# Streamlit Community Cloud (Secrets) からセッションを取得
cnx = st.connection("snowflake")
session = cnx.session()

# フルーツ一覧を取得
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# 最大5つまでの材料選択
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    # 列名のタイポを修正 (ingredienst -> ingredients)
    my_insert_stmt = f"""insert into smoothies.public.orders(ingredients) 
    values ('{ingredients_string}')"""

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

import requests  
# URL文字列のみ（純粋な https://...）を指定
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")  
# 取得したレスポンスのJSONデータを表示
#st.text(smoothiefroot_response.json())
st_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
