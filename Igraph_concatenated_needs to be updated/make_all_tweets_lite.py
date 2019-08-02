import os
import shutil

global_repository = './all_tweets_234/'
target_repo = './all_tweets_234_lite'

def main():
  make_directory(target_repo)

  all_tweet_networks = [f for f in os.listdir(global_repository) if (not os.path.isfile(global_repository + "/" + f))]
  filter_out = ["All_Followers", "All_Friends", "All_Incomplete_Scrapes", "__pycache__", "sample", "Concatenated"]
  all_tweet_networks = list(filter(lambda x : all([w not in x for w in filter_out]), all_tweet_networks))
  
  for net in all_tweet_networks:
    print(net)
    shutil.copy(global_repository + net + '/retweets_' + net + '.txt', target_repo)  

def make_directory(dirname):
  if not os.path.exists(dirname):
    os.makedirs(dirname)

if __name__ == '__main__':
  main()