import pandas as pd



def read_csv_as_dict():
    desired_width = 1000
    pd.set_option('display.width', desired_width)
    pd.set_option('display.max_rows', 1000)
    pd.set_option('display.max_columns', 10)

    df = pd.read_csv('helpareporter_twitter_follower.csv', sep=",", encoding='utf-8')
    all_data = []
    for i in range(0, len(df)):
        input_data = df.loc[i].to_dict()
        all_data.append(input_data)
    return all_data[100:300]

def read_csv():
    desired_width = 1000
    pd.set_option('display.width', desired_width)
    pd.set_option('display.max_rows', 1000)
    pd.set_option('display.max_columns', 10)

    df = pd.read_csv('helpareporter_twitter_follower.csv')
    df.dropna(subset=['website'], how="any", inplace=True)
    list_values = df['website'].values.tolist()
    return list_values

def sample_csv():
    desired_width = 1000
    pd.set_option('display.width', desired_width)
    pd.set_option('display.max_rows', 1000)
    pd.set_option('display.max_columns', 20)

    df = pd.read_csv('helpareporter_twitter_follower.csv')
    df.dropna(subset=['website'], how="any", inplace=True)
    list_values = df['website'].values.tolist()
    return list_values[100:200]

# df = pd.read_csv('helpareporter_twitter_follower.csv')
# # df.insert(loc=8, column='Email', value='None')
# for url in sample_csv():
#     df.loc[df.website == url, "Email"] = url
#     subset = df.loc[100:200, ['website', 'Email']]
# print(df.head())
#
# print(df[:300])