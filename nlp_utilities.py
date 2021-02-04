import requests
import multiprocessing
import pandas as pd


def resolve_url(url):
    if url is None:
        return None
    url = url.rstrip(".")
    try:
        elem = requests.head(url).headers['location']
        if(elem.startswith("https://bit.ly") or
           elem.startswith("https://cutt.ly") or
           elem.startswith("https://goo.gl") or
           elem.startswith("https://rebrand.ly") or
           elem.startswith("https://demo.polr.me") or
           elem.startswith("https://tinyurl") or
           elem.startswith("https://t2m") or
           elem.startswith("https://yourls")):
            elem = resolve_url(elem)
        return elem
    except requests.exceptions.InvalidURL:
        print("bad request", url)
        return None
    except KeyError as e:
        # print(e)
        return None
    except:
        print("generic error\n")
        return None


def find_url(line):
    for word in line.split(" "):
        if word.startswith("http"):
            return word.rstrip("\n")


def parse_match_count(df_fake_news, df_real_news, users_id,
                      pathToTimelines, pathToNewsMatched,
                      df_range=""):
    print("Checking for news sharing in Users Timelines\n")
    exception_file = open("exception.txt", "a")
    pool = multiprocessing.Pool(100)
    counter_users = 1
    total = len(users_id)
    col = {
        'user_id': [],
        'tweet_id': [],
        'text': [],
        'url': [],
        'extended_url': []
    }
    colstat = {
        'user_id': [],
        'fake_count': [],
        'real_count': [],
        'total_tweet': [],
        'percentage_fake': [],
        'percentage_real': []
    }
    dfcoll = pd.DataFrame(col).astype('object')
    dfcollr = pd.DataFrame(col).astype('object')
    dfstat = pd.DataFrame(colstat).astype('object')
    for user in users_id:
        print("Progress: " + str(counter_users) + "/" + str(total))
        counter_users = counter_users + 1
        print(str(user))
        url_list = []
        try:
            df = pd.read_csv(pathToTimelines+str(user)+".csv")
        except:
            print("impossible reading user" + str(user))
            exception_file.write("impossible reading user " + str(user) + "\n")
            continue
        df = df.fillna('0').astype('object')
        df_url = df[df.text.str.contains('http', case=False)]
        url_list = []
        for text in df_url.text:
            url_list.append(find_url(text))
        df_url['url'] = url_list
        resolved_urls = []
        for longurl in pool.map(resolve_url, url_list):
            resolved_urls.append(longurl)
        df_url['extended_url'] = resolved_urls
        df_fake_found = df_url[
            (df_url.extended_url.isin(df_fake_news["news_url"].values))
            | (df_url.extended_url.isin(df_fake_news["news_url2"].values))
            | (df_url.extended_url.isin(df_fake_news["news_url3"].values))
            | (df_url.extended_url.isin(df_fake_news["news_url4"].values))
            | (df_url.extended_url.isin(df_fake_news["news_url5"].values))
        ]
        dfcoll = dfcoll.append(df_fake_found)
        df_real_found = df_url[
            df_url.extended_url.isin(df_real_news["news_url"].values)]
        dfcollr = dfcollr.append(df_real_found)
        if df.shape[0] == 0:
            den = 1
        else:
            den = df.shape[0]

        dfstat_row = {
            'user_id': str(user),
            'fake_count': str(df_fake_found.shape[0]),
            'real_count': str(df_real_found.shape[0]),
            'total_tweet': str(df.shape[0]),
            'percentage_fake': str((df_fake_found.shape[0]/den)*100),
            'percentage_real': str((df_real_found.shape[0]/den)*100)

        }
        dfstat = dfstat.append(dfstat_row, ignore_index=True)
    dfcoll.to_csv(pathToNewsMatched+"fake_uit"+df_range+".csv", index=False)
    dfcollr.to_csv(pathToNewsMatched+"real_uit"+df_range+".csv", index=False)
    dfstat.to_csv(pathToNewsMatched+"count"+df_range+".csv", index=False)
    exception_file.close()
    print("Check and store phase complete\n")


def stance_detection_create_file(df_news, df_detected, fake=True):
    i = 1
    iloc_count = 0
    flag = 0
    f = open("gate_cloud.txt", "w")
    for url in df_detected["extended_url"]:
        flag, title = check_column("news_url", df_news, url)
        if fake is True:
            if flag == 0:
                flag, title = check_column("news_url2", df_news, url)
            if flag == 0:
                flag, title = check_column("news_url3", df_news, url)
            if flag == 0:
                flag, title = check_column("news_url4", df_news, url)
            if flag == 0:
                flag, title = check_column("news_url5", df_news, url)
        if flag == 1:
            f.write("{\"text\":\""+str(
                df_detected.iloc[iloc_count]['text']) +
                    "\",\"id_str\":\""+str(i)+"\"}\n\n")
            f.write("{\"text\":\""+str(title)+"\",\"id_str\":\""+str(i+1) +
                    "\", \"in_reply_to_status_id_str\":\""+str(i)+"\"}\n\n")
        i = i + 2
        iloc_count = iloc_count + 1
    f.close()


def check_column(column, df_news, url):
    try:
        result = df_news[df_news[column].str.contains(str(url))]
        if result.empty:
            title = None
            flag = 0
        else:
            title = result["title"].values[0]
            flag = 1
    except KeyError:
        print("Key")
        flag = 0
        return flag, None
    return flag, title
