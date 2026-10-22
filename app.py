import streamlit as st
import pandas as pd

st.set_page_config(page_title="Transform the Data", page_icon="🔄", layout="wide")

st.title("🔄 Transform the Data - Analytics Tool")
st.write("Upload your dataset to transform, rename, and filter columns instantly.")

# File uploader
uploaded_file = st.file_uploader("Upload your CSV dataset", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Original Dataset Preview")
        st.dataframe(df)
        
    with col2:
        st.subheader("⚙️ Transformation Options")
        
        # 1. Select Columns to keep
        all_columns = df.columns.tolist()
        selected_cols = st.multiselect("Select columns to keep:", all_columns, default=all_columns)
        df_transformed = df[selected_cols]

        # 2. Rename Columns
        if st.checkbox("Enable Column Renaming"):
            rename_dict = {}
            st.write("Enter new names:")
            for col in selected_cols:
                new_name = st.text_input(f"Rename '{col}' to:", value=col, key=f"rename_{col}")
                rename_dict[col] = new_name
            df_transformed = df_transformed.rename(columns=rename_dict)

        # 3. Sort Data
        numeric_cols = df_transformed.select_dtypes(include=['number']).columns.tolist()
        if numeric_cols:
            sort_by = st.selectbox("Sort data by column:", ["None"] + numeric_cols)
            if sort_by != "None":
                df_transformed = df_transformed.sort_values(by=sort_by)

    st.markdown("---")
    st.subheader("🚀 Transformed Dataset View")
    st.dataframe(df_transformed)

    # Download button for transformed data
    csv = df_transformed.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Transformed CSV 📥",
        data=csv,
        file_name="transformed_data.csv",
        mime="text/csv"
    )
else:
    st.info("💡 Please upload a CSV file to start transformation.")
                                   
