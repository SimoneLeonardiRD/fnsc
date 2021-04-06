import twitter_utilities as tu
import pandas as pd
import tweepy

# ----- Twitter Authenitcation ----- #
TwitterAuthData = "twitter_dev/twitterAccess.txt"
DevKeyAndSecret = "twitter_dev/consumer_api_keys.txt"
api = tu.authentication(DevKeyAndSecret, TwitterAuthData)

path = "generated_data/user_info"
dfusers = pd.read_csv("output_test/user_label_clean.csv")
users = dfusers['user_id']
# print(users)
data = {
        'location': [],
        'protected': bool,
        'verified': bool,
        'followers_count': int,
        'friends_count': int,
        'listed_count': int,
        'favourites_count': int,
        'statuses_count': int,
        'created_at': [],
        'default_profile': bool,
        'default_profile_image': bool
}
df = pd.DataFrame(data)
count = 0
for user in users:  # [101:104]:
    count += 1
    print(str(count) + "/"+str(len(users)))
    try:
        user_obj = api.get_user(id=user)
        new_row = {
            'location': user_obj.location,
            'protected': user_obj.protected,
            'verified': user_obj.verified,
            'followers_count': user_obj.followers_count,
            'friends_count': user_obj.friends_count,
            'listed_count': user_obj.listed_count,
            'favourites_count': user_obj.favourites_count,
            'statuses_count': user_obj.statuses_count,
            'created_at': user_obj.created_at,
            'default_profile': user_obj.default_profile,
            'default_profile_image': user_obj.default_profile_image
        }
    except tweepy.error.TweepError as e:
        print(user, "error", e)
        new_row = {
            'location': "-",
            'protected': False,
            'verified': False,
            'followers_count': 0,
            'friends_count': 0,
            'listed_count': 0,
            'favourites_count': 0,
            'statuses_count': 0,
            'created_at': '-',
            'default_profile': True,
            'default_profile_image': True
        }

    df = df.append(new_row, ignore_index=True)
df.to_csv("user_info.csv", index=False)
