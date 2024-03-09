import streamlit as st
import chatSummary
import preprocessor
import analysisHelper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose File", type="txt")
if uploaded_file is None:
    st.title("Upload a whatsapp file to analyze")
    breakpoint()

bytes_data = uploaded_file.getvalue()
string_data = bytes_data.decode("utf-8")
returned_df = preprocessor.preprocess(string_data)

# creating users list
user_list = returned_df["user"].unique().tolist()
user_list.remove("System Notification")
user_list.sort()
user_list.insert(0, "Overall")
selected_user = st.sidebar.selectbox("Show Analysis W.R.T", user_list)

# adding button for showing analysis
if st.sidebar.button("Analyze"):
    st.title("Chat Summary")
    st.header("Messages")
    user_messages = analysisHelper.filter_messages(selected_user, returned_df)
    st.dataframe(user_messages.reset_index())

    return_data = chatSummary.get_chat_summary(selected_user, returned_df)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.header("Total Messages")
        st.title(return_data[0])
    with col2:
        st.header("Total Words")
        st.title(return_data[1])
    with col3:
        st.header("Media Shared")
        st.title(return_data[2])
    with col4:
        st.header("Links Shared")
        st.title(return_data[3])

    # busiest users(group level)
    st.title("Top Statistics")
    if selected_user == "Overall":
        x, df = analysisHelper.busiest_users_helper(returned_df)
        col1, col2 = st.columns(2)
        with col1:
            st.header("Busiest Users Bar Chart")
            fig, ax = plt.subplots()
            ax.bar(x.index, x.values, color="red")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header("Busiest Users Table")
            st.dataframe(df)

    # activity timeline by month
    st.header("Activity Last Two Years")
    timeline = analysisHelper.activity_timeline_monthly_helper(selected_user, returned_df)
    fig, ax = plt.subplots()
    ax.plot(timeline['month_year'], timeline['messages'])
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    # activity timeline by day
    st.header("Last 30 Active Days")
    timeline = analysisHelper.activity_timeline_daily_helper(selected_user, returned_df)
    fig, ax = plt.subplots()
    ax.plot(timeline['day_month_year'], timeline['messages'])
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    # wordCloud
    st.header("Word Cloud")
    wc = analysisHelper.word_cloud_helper(selected_user, returned_df)
    fig, ax = plt.subplots()
    ax.imshow(wc)
    st.pyplot(fig)

    # analyze emojis
    emoji_df = analysisHelper.emoji_helper(selected_user, returned_df)

    col1, col2 = st.columns(2)
    with col1:
        st.header("Most Common Emojis")
        st.dataframe(emoji_df)
    with col2:
        st.header("Top 5 Emojis Bar Chart")
        fig, ax = plt.subplots()
        ax.bar(emoji_df[0].head(), emoji_df[1].head(), color="green")
        st.pyplot(fig)

    # most active days and months
    day_map = analysisHelper.day_activity_map(selected_user, returned_df)
    month_map = analysisHelper.month_activity_map(selected_user, returned_df)

    col1, col2 = st.columns(2)
    with col1:
        st.header("Most Busy Day")
        fig, ax = plt.subplots()
        ax.bar(day_map.index, day_map.values)
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
    with col2:
        st.header("Most Busy Month")
        fig, ax = plt.subplots()
        ax.bar(month_map.index, month_map.values, color="orange")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    # most active hour
    st.header("Activity By Hour")
    user_heatmap = analysisHelper.hour_activity_map(selected_user, returned_df)

    fig, ax = plt.subplots()
    ax = sns.heatmap(user_heatmap)
    plt.yticks(rotation="horizontal")
    st.pyplot(fig)
