import requests
import multiprocessing
import pandas as pd


def resolve_url(url):
    if url is None:
        return None

    try:
        elem = requests.head(url).headers['location']
        return elem
    except requests.exceptions.InvalidURL:
        print("bad request", url)
        return None
    except KeyError as e:
        print(e)
        return None
    except:
        print("generic error\n")
        return None


def find_url(line):
    for word in line.split(" "):
        if word.startswith("http"):
            return word.rstrip("\n")


def parse_match_count(fake_news_list, real_news_list, users_id):
    pool = multiprocessing.Pool(100)
    counter_users = 1
    total = len(users_id)
    dfcoll = pd.read_csv("fake_uit.csv") 
    dfcollr = pd.read_csv("real_uit.csv")
    dfstat = pd.read_csv("count_fake_real.csv")
    for user in users_id:
        print("Progress: " + str(counter_users) + "/" + str(total))
        print(str(user))
        counter_fake_tweets = 0.0
        counter_real_tweets = 0.0
        counter_lines_checked = 0.0
        url_list = []
        fin = open("data/tweet/"+str(user), "r")
        for line in fin.readlines():
            counter_lines_checked += 1
            columns = line.split("\t")  # tweet id and text
            url = find_url(line)
            url_list.append(url)
        resolved_urls = []
        for longurl in pool.map(resolve_url, url_list):
            resolved_urls.append(longurl)

        for url in resolved_urls:
            if url is None:
                continue
            if url in fake_news_list:
                print(user, "fake link found\n")
                counter_fake_tweets += 1  # salvare per stance detection
                dfcoll_row = {
                    'user_id': str(user),
                    'tweet_id': str(columns[0]),
                    'tweet_text': line[(len(columns[0])+1):].rstrip("\n"),
                    'url': str(url)
                }
                dfcoll = dfcoll.append(dfcoll_row, ignore_index=True)
            if url in real_news_list:
                print(user, "real link found\n")
                counter_real_tweets += 1  # salvare per stance detection
                dfcollr_row = {
                    'user_id': str(user),
                    'tweet_id': str(columns[0]),
                    'tweet_text': line[(len(columns[0])+1):].rstrip("\n"),
                    'url': str(url)
                }
                dfcollr = dfcollr.append(dfcollr_row, ignore_index=True)
        fin.close()
        if counter_lines_checked == 0:
            counter_lines_checked = 1
        dfstat_row = {
            'user_id': str(user),
            'fake_count': str(counter_fake_tweets),
            'real_count': str(counter_real_tweets),
            'total_tweet': str(counter_lines_checked),
            'percentage_fake': str((counter_fake_tweets/counter_lines_checked)*100),
            'percentage_real': str((counter_real_tweets/counter_lines_checked)*100)

        }
        dfstat = dfstat.append(dfstat_row, ignore_index=True)
        counter_users += 1
    dfcoll.to_csv("fake_uit.csv", index=False)
    dfcollr.to_csv("real_uit.csv", index=False)
    dfstat.to_csv("count_fake_real.csv", index=False)
