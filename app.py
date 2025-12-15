import streamlit as st

from llm_router import route_user_input
from db import run_sql, rank_results
from bot_detector import is_bot
from serpapi_search import search_online
from missing_data_logger import log_missing_query

st.set_page_config(page_title="Business Finder", page_icon="🔍")
st.title("🔍 Business Finder Assistant")

if "user_id" not in st.session_state:
    st.session_state.user_id = str(id(st))

user_input = st.text_input("Ask me anything...")

if user_input:
    if is_bot(st.session_state.user_id, user_input):
        st.error("🚫 Automated activity detected. Request blocked.")
        st.stop()

    with st.spinner("Thinking..."):
        result = route_user_input(user_input)

    st.markdown(f"💬 **Assistant:** {result['response']}")

    if result["intent"] == "sql_search":
        rows = run_sql(result["sql"])

        if rows:
            ranked_rows = rank_results(rows, top_n=10)

            st.subheader("Best Matches for You")

            for r in ranked_rows:
                st.markdown(
                    f"""
                    **{r['name']}**  
                    ⭐ {r['reviews_average']} rating from {r['reviews_count']} reviews  
                    📍 {r['address']}  
                    📞 {r['phone_number'] or 'N/A'}  
                    🌐 {r['website'] or 'N/A'}
                    """
                )
        else:
            st.info("I couldn’t find matches in my database. Searching online…")
            online_results = search_online(user_input)
            log_missing_query(user_input, online_results)

            if not online_results:
                st.warning("No reliable online results found.")
            else:
                st.subheader("Popular Businesses Online")
                for r in online_results[:5]:
                    st.markdown(
                        f"""
                        **{r.get('title','Unknown')}**  
                        ⭐ {r.get('rating','N/A')}  
                        📍 {r.get('address','N/A')}  
                        📞 {r.get('phone','N/A')}
                        """
                    )
