#
# Takes all Friends and Follower files from 
# single tweet folders and places them all 
# in one place
#
# If two tweet folders have the same file
# then we place A u B into the global dir 
#
# Assumes you are in directory containing
# folders that each have files realted to
# one scraped tweet_id
#

import os
import shutil


def combine_networks(cur_dir = "./", all_tweet_networks = []):
  global_follower_repo = cur_dir + "/All_Followers"
  global_friend_repo = cur_dir + "/All_Friends"

  make_directory(global_friend_repo)
  make_directory(global_follower_repo)

  # Run on all:
  if(all_tweet_networks == []):
    all_tweet_networks = [f for f in os.listdir(cur_dir) if (not os.path.isfile(cur_dir + "/" + f))]
    filter_out = ["All_Followers", "All_Friends", "__pycache__", "sample", "Concatenated"]
    all_tweet_networks = list(filter(lambda x : all([w not in x for w in filter_out]), all_tweet_networks))
  
  print("Concatenating the folders.")
  for tweet_id in all_tweet_networks:
    print("Processing tweet: ", tweet_id)

    # Open friends folder
    friends_folder = cur_dir + "/" + tweet_id + "/Friends_l1_" + tweet_id
    if(not os.path.exists(friends_folder)):
      friends_folder = cur_dir + "/" + tweet_id + "/Friends_" + tweet_id
    process_folder(friends_folder, global_friend_repo)

    # Open follower folder
    followers_folder = cur_dir + "/" + tweet_id + "/Followers_l1_" + tweet_id
    if(not os.path.exists(followers_folder)):
      followers_folder = cur_dir + "/" + tweet_id + "/Followers_" + tweet_id

    process_folder(followers_folder, global_follower_repo)
  print("Concatenation finished.")
  
def process_folder(from_folder, to_folder):
  cur_targets = [f for f in os.listdir(from_folder) if os.path.isfile(from_folder + "/" + f)]
  for target in cur_targets:
    # If already exists in global repo
    if(check_file_in(target, to_folder)):
      # merge properly
      merge_files(from_folder + "/" + target, to_folder + "/" + target)
    # Else place in global directory
    else:
      shutil.copy(from_folder + "/" + target, to_folder)

def merge_files(b, a):
  tmp_dict = {}
  with open(a, 'r') as inptr:
    for line in inptr:
      tmp_dict[line] = 1
  
  with open(b, 'r') as inptr:
    for line in inptr:
      tmp_dict[line] = 1

  with open(a, 'w') as inptr:
    for string in tmp_dict.keys():
      print(string, file = inptr)

def check_file_in(to_check, in_):
  return os.path.isfile(in_ + "/" + to_check)

def make_directory(dirname):
  if not os.path.exists(dirname):
    os.makedirs(dirname)

if __name__ == '__main__':
  combine_networks()