import pandas as pd
import re


def extract_hour_period(df: pd.DataFrame):
    hour_period = []
    for hour in df[["day_name", "hour"]]["hour"]:
        if hour == 23:
            hour_period.append(str(hour) + "-" + "00")
        elif hour == 00:
            hour_period.append("00" + "-" + str(hour + 1))
        else:
            hour_period.append(str(hour) + "-" + str(hour + 1))

    return hour_period

def preprocess(data) -> pd.DataFrame:
    pattern = '\d{1,2}\/\d{1,2}\/\d{2}, \d{1,2}:\d{2} [APap][Mm]\s\-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({"user_messages": messages, "message_dates": dates})

    df['message_dates'] = pd.to_datetime(df['message_dates'], format='%m/%d/%y, %I:%M %p - ')

    user_names = []
    user_messages = []
    name_pattern = '([\w\W]+?):\s'
    unsaved_numbers_pattern = '\+'

    for msg in df['user_messages']:
        user_and_msg = re.split(name_pattern, msg)
        if len(user_and_msg) > 1:
            saved_numbers = re.split(unsaved_numbers_pattern, user_and_msg[1])
            if len(saved_numbers) == 1:
                user_names.append(user_and_msg[1])
                user_messages.append(user_and_msg[2])
            elif len(saved_numbers) > 1:
                user_names.append("Others")
                user_messages.append(user_and_msg[2])
        else:
            user_names.append("System Notification")
            user_messages.append(user_and_msg[0])

    df['user'] = user_names
    df['messages'] = user_messages
    df.drop(columns=['user_messages'], inplace=True)

    df['year'] = df['message_dates'].dt.year
    df['month'] = df['message_dates'].dt.month_name()
    df['month_num'] = df['message_dates'].dt.month
    df["days_in_month"] = df["message_dates"].dt.days_in_month
    df['day_name'] = df['message_dates'].dt.day_name()
    df['day'] = df['message_dates'].dt.day
    df['hour'] = df['message_dates'].dt.hour
    df['minute'] = df['message_dates'].dt.minute

    hour_period = extract_hour_period(df)
    df['hour_period'] = hour_period

    df = df[df["messages"] != "This message was deleted\n"]

    return df
