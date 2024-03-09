import pandas as pd
from wordcloud import WordCloud
import emoji
from collections import Counter


def filter_messages(selected_user: str, df: pd.DataFrame) -> pd.DataFrame:
    if selected_user is not "Overall":
        df = df[df["user"] == selected_user]
    return df


def busiest_users_helper(df: pd.DataFrame) -> list:
    df = df[df["user"] != "System Notification"]
    x = df["user"].value_counts().head()
    df = round((df["user"].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={"index": "user", "user": "percentage"})
    return [x, df]


def word_cloud_helper(selected_user: str, df: pd.DataFrame):
    df = filter_messages(selected_user, df)

    df = df[df["messages"] != "<Media omitted>\n"]
    df = df[df["user"] != "System Notification"]
    df["messages"] = df["messages"].apply(lambda s: emoji.replace_emoji(s, ''))

    wc = WordCloud(height=500, width=500, background_color='white')
    messages_wc = wc.generate(df["messages"].str.cat(sep=" "))
    return messages_wc


def emoji_helper(selected_user: str, df: pd.DataFrame):
    df = filter_messages(selected_user, df)

    emojis = []
    for message in df["messages"]:
        if len(emoji.emoji_list(message)) != 0:
            list_emoji = emoji.emoji_list(message)
            for m in list_emoji:
                emojis.append(m['emoji'])

    return pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))


def activity_timeline_monthly_helper(selected_user: str, df: pd.DataFrame):
    df = filter_messages(selected_user, df)

    timeline = df.groupby(["year", "month_num", "month"]).count()["messages"].reset_index()

    month_year = []
    current_month_index = timeline.shape[0]
    previous_months_index = 0
    if current_month_index >= 24:
        previous_months_index = current_month_index - 24

    for i in range(current_month_index):
        month_year.append(timeline['month'][i] + '-' + str(timeline['year'][i]))
    timeline["month_year"] = month_year

    return timeline[previous_months_index:]


def activity_timeline_daily_helper(selected_user: str, df: pd.DataFrame):
    df = filter_messages(selected_user, df)

    timeline = df.groupby(["year", "month_num", "month", "day"]).count()["messages"].reset_index()

    day_month_year = []
    current_day_index = timeline.shape[0]
    if current_day_index >= 30:
        timeline = timeline[current_day_index-30:].reset_index()

    for i in range(timeline.shape[0]):
        day_month_year.append(
            str(timeline['day'][i]) + '-' + str(timeline['month'][i]) + '-' + str(timeline['year'][i]))

    timeline["day_month_year"] = day_month_year
    return timeline


def day_activity_map(selected_user: str, df: pd.DataFrame):
    df = filter_messages(selected_user, df)

    return df["day_name"].value_counts()


def month_activity_map(selected_user: str, df: pd.DataFrame):
    df = filter_messages(selected_user, df)

    return df["month"].value_counts()


def hour_activity_map(selected_user: str, df: pd.DataFrame):
    df = filter_messages(selected_user, df)

    return df.pivot_table(index="day_name", columns="hour_period", values="messages", aggfunc="count").fillna(0)