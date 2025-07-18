# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col,when_matched

# Write directly to the app
st.title(":cup_with_straw: Customize Smoothie Orders:cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie")

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Get the active session
cnx = st.connection("snowflake")
session = cnx.session()

# Access the fruit options table
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')).to_pandas()

# Display the dataframe (optional)
# st.dataframe(data=my_dataframe, use_container_width=True)

# Create a multiselect widget
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:', my_dataframe['FRUIT_NAME'].tolist(),max_selections=5
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smooothiefroot.com/api/fruit/" + fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
