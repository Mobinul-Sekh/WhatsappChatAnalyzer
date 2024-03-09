import pandas as pd
from urlextract import URLExtract

extractor = URLExtract()


def get_chat_summary(selected_user: str, df: pd.DataFrame) -> list:

    if selected_user is not "Overall":
        df = df[df["user"] == selected_user]

    # total messages
    messages = df.shape[0]

    # total words
    words = []
    for message in df["messages"]:
        words.extend(message.split())

    # media file shared
    media = df[df["messages"] == "<Media omitted>\n"]

    # link shared
    urls = []
    for message in df["messages"]:
        urls.extend(extractor.find_urls(message))

    return [messages, len(words), len(media), len(urls), len(urls)]
