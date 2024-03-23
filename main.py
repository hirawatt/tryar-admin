import streamlit as st
import pymongo
import pandas as pd

st.set_page_config(layout="wide")
db_name = st.secrets["mongodb"]["database"]
collection_name = st.secrets["mongodb"]["collection"]

@st.cache_resource
def init_connection():
    return pymongo.MongoClient(**st.secrets["mongo"])

client = init_connection()
db = client[db_name]
collection = db[collection_name]
data = collection.count_documents(filter=None)
print(data)

# Pull data from the collection.
@st.cache_data()
def get_data():
    db = client.tryAr
    collection = db[collection_name].find({})
    return pd.DataFrame(collection)

df = get_data()
edited_df = st.data_editor(df,
                            key="my_editor",
                            use_container_width=True
                        )

if 'my_editor' in st.session_state:  # Check if editor has been used
    edited_rows = st.session_state['my_editor']['edited_rows']
    rows_list = []
    if edited_rows:  # Check if any edits were made
        for row_index, edited_values in edited_rows.items():
            rows_list.append(row_index)
    else:
        st.write("No edits have been made yet.")
        
doc_id = list(edited_df.iloc[rows_list]["_id"])
st.write(doc_id)

if st.button("Update Document", type="primary"):
    for i in doc_id:
        update_document = {"$set": {"premium": True}}
        try:
            update_result = collection.update_one({"_id": str(i)}, update_document)
            print(update_result)
        except pymongo.errors.PyMongoError as e:
            print(f"An error occurred: {e}")
        
        if update_result.matched_count == 1 and update_result.modified_count == 1:
            print("Document updated successfully!")
        elif update_result.matched_count == 1 and update_result.modified_count == 0:
            print("Document matched but no changes needed (or validation error).")
        else:
            print("Document not found or update failed.")