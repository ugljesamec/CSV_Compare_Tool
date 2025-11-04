import pandas as pd
import streamlit as st

st.set_page_config(page_title="CSV Compare Tool", page_icon=":bar_chart:", layout="wide")

st.title("CSV Compare Tool - created for Maja")

# --- Upload CSV files ---
col1, col2 = st.columns(2)
with col1:
    file_a = st.file_uploader("Upload CSV 1", type="csv")
with col2:
    file_b = st.file_uploader("Upload CSV 2", type="csv")

differences = []

if file_a and file_b:
    try:
        df_a = pd.read_csv(file_a)
        df_b = pd.read_csv(file_b)

        if list(df_a.columns) != list(df_b.columns):
            st.error("CSV columns do not match!")
        else:
            key_col = df_a.columns[0]  # assuming first column is ID
            df_a.set_index(key_col, inplace=True)
            df_b.set_index(key_col, inplace=True)

            # --- Rows only in A ---
            only_a_idx = df_a.index.difference(df_b.index)
            only_a = df_a.loc[only_a_idx]

            # --- Rows only in B ---
            only_b_idx = df_b.index.difference(df_a.index)
            only_b = df_b.loc[only_b_idx]

            # --- Changed rows ---
            common_idx = df_a.index.intersection(df_b.index)
            changed_rows = []
            for idx in common_idx:
                row_a = df_a.loc[idx]
                row_b = df_b.loc[idx]
                for col in df_a.columns:
                    val_a = row_a[col] if pd.notna(row_a[col]) else ""
                    val_b = row_b[col] if pd.notna(row_b[col]) else ""
                    if val_a != val_b:
                        differences.append([idx, col, val_a, val_b])
                        changed_rows.append((idx, col, val_a, val_b))

            st.subheader("Differences Found")
            st.write(f"Total differences: {len(differences)}")

            if only_a.shape[0] > 0:
                st.subheader("Rows only in CSV 1")
                st.dataframe(only_a)

            if only_b.shape[0] > 0:
                st.subheader("Rows only in CSV 2")
                st.dataframe(only_b)

            if changed_rows:
                st.subheader("Changed Values")
                df_diff = pd.DataFrame(changed_rows, columns=["id", "column", "old_value", "new_value"])
                st.dataframe(df_diff.style.applymap(lambda x: "background-color: #ffcccc", subset=["old_value", "new_value"]))

            # --- Export differences ---
            if differences:
                df_export = pd.DataFrame(differences, columns=["id", "column", "old_value", "new_value"])
                csv_export = df_export.to_csv(index=False).encode('utf-8')
                st.download_button("Export Differences", data=csv_export, file_name="differences.csv", mime="text/csv")

    except Exception as e:
        st.error(f"Failed to process CSVs: {e}")
