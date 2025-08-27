import streamlit as st
import pandas as pd

class DuplicateUI:
    """
    Streamlit UI for duplicate detection and review.
    """
    @staticmethod
    def show_duplicates(duplicates: pd.DataFrame):
        if duplicates is None or duplicates.empty:
            st.success("No duplicates found.")
            return
        st.warning(f"Found {duplicates['Order # Clean'].nunique()} duplicate order numbers ({len(duplicates)} total records)")
        if st.button("Remove All Duplicates"):
            st.info("All duplicates removed (placeholder logic).")
        if st.checkbox("Review Duplicate List"):
            st.dataframe(duplicates)
        if st.button("Keep Duplicates"):
            st.info("Proceeding with original data (duplicates kept).") 