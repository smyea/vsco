import requests
import pandas as pd
import time
import os
import json

from sqlalchemy import create_engine, text

####################
#  AUTHENTICATION  #
####################

def get_reddit_access_token(client_auth, post_data, headers):

    # From their documentation, this is the endpoint we need
    ACCESS_TOKEN_ENDPOINT = "https://www.reddit.com/api/v1/access_token"

    # we send a HTTP POST, convert the response to json and return the token
    response = requests.post(ACCESS_TOKEN_ENDPOINT, auth=client_auth, data=post_data, headers=headers)
    print(response.status_code)
    reddit_response = response.json()
    return reddit_response['access_token']

#####################################
#  REDDIT API SUBREDDIT DATA FETCH  #
#####################################

# function which fetches subreddit metadata from a list of subreddits
def fetch_subreddit_info(subreddits, headers):
    subreddit_info = []  # Store results

    # looping through subreddits
    for sub in subreddits:
        url = f"https://oauth.reddit.com/r/{sub}/about"
        response = requests.get(url, headers=headers)

        # if the response is successful we take in only the data we want into the list 
        if response.status_code == 200:
            subreddit_info.append(response.json()["data"]) 
            
        else:
            print(f"Error {response.status_code} fetching r/{sub} info")

    return subreddit_info  # Return list after collecting all subreddit data


################################
#  REDDIT API POST DATA FETCH  #
################################


def fetch_recent_posts(subreddits, headers, days=100, max_pages=90):

    since_timestamp = int(time.time()) - (days * 86400)  # Convert days to seconds into an integer

    # initialise a list to hold the post data 
    all_posts = []

    # looping over all elements of list
    for sub in subreddits: 
        # for the first API call we want to start from the beginning for each subreddit 
        after = None

        for _ in range(max_pages):  # Fetch multiple pages using a for loop 
            params = {'limit': 100}  # Max allowed per request default is 25, the limit parameter lets us call 100 

            # if after is not None, start from searching from the last known location 
            if after: 
                params['after'] = after

            response = requests.get(f"https://oauth.reddit.com/r/{sub}/new", headers=headers, params=params)

            if response.status_code == 200:
                output = response.json()

                # access the data dictionary and within that the children list, and store under posts
                posts = output['data']['children']

                # Filter posts by timestamp and retain data within the data dictionary 
                filtered_posts = [p['data'] for p in posts if p['data']['created_utc'] >= since_timestamp]

                # extend the post list 
                all_posts.extend(filtered_posts)

                after = output['data']['after']  # Get next page token 
                # print(f" {sub}| After: {after}") # check that our token is changing every loop 

                if not after:  # Stop if we run out of new posts
                    break 
            else:
                print(f"Error: {response.status_code}")
                break

        print(f"Total posts fetched: {len(all_posts)} | Last sub accessed: r/{sub}")
    return all_posts


###################################
#  REDDIT API COMMENT DATA FETCH  #
###################################

def fetch_comments_from_post(row, headers, max_pages=90, max_retries=5):
    """
    This function sends a series of get requests to the Reddit API to fetch 
    comments from a specific post in a given subreddit. It handles pagination 
    and rate limiting by using exponential backoff.

    It takes in a df row, and has defaults for max pages of comments to fetch 
    and max retry attempts in the case of rate limiting. It returns a list of 
    comments (which are dicts)
    """

    all_comments = []
    subreddit = row["subreddit"] # assign respective values from row to variables
    post_id = row["id"] 
    after = None

    retry_attempts = 0  # Track retries for exponential backoff for rate limiting

    for _ in range(max_pages):  
        params = {'limit': 100}  
        if after:
            params['after'] = after

        url = f"https://oauth.reddit.com/r/{subreddit}/comments/{post_id}.json"

        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            retry_attempts = 0  # Reset retries on success
            output = response.json()
            if output and len(output) > 1:

                # go in data[1] since data[0] stores the metadata and doesn't include comments
                comments_data = output[1]['data']['children']
                all_comments.extend(comments_data)

                # assign after to continue from position after loop restarts
                after = output[1]['data']['after'] 
                if not after:  
                    break  # Stop if no more comments

        # if rate limited initiate backoff         
        elif response.status_code == 429:
            retry_attempts += 1
            # ensure retries are limited
            if retry_attempts > max_retries:
                print(f"Max retries ({max_retries}) reached. Stopping.")
                break
            
            wait_time = 5 ** retry_attempts  # Exponential backoff by a multiple of 5 
            print(f"Rate limited! Retrying after {wait_time} seconds...")
            time.sleep(wait_time) # call backoff
            
        else: # handling other errors 
            print(f"Error fetching post {post_id}: {response.status_code}, {response.text}")
            break  

        time.sleep(2)  # Prevent hitting rate limits proactively 

    # print(f"Fetched {len(all_comments)} comments from post {post_id}")
    return all_comments


#########################################
#  REDDIT API COMMENT REPLY EXTRACTION  #
#########################################

def extract_comment_data_helper(comment_data):
    return {
        "comment_id": comment_data["id"] if "id" in comment_data else None,
        "post_id": comment_data["link_id"] if "link_id" in comment_data else None,
        "author": comment_data["author_fullname"] if "author_fullname" in comment_data else None,
        "created_utc": comment_data["created_utc"] if "created_utc" in comment_data else None,
        "score": comment_data["score"] if "score" in comment_data else 0,
        "body": comment_data["body"] if "body" in comment_data else "",
        "ups": comment_data["ups"] if "ups" in comment_data else 0,
        "parent_id": comment_data["parent_id"] if "parent_id" in comment_data else None,
    }

def extract_comments(comment_list, comments_output_list=None):
    if comments_output_list is None:
        comments_output_list = []

    for item in comment_list:
        if item["kind"] == "t1":  # Ensure it's a comment
            comment_data = item["data"]  # Direct access to 'data'
            comments_output_list.append(extract_comment_data_helper(comment_data))  # Extract comment fields add it to list 
            
            # Directly access 'replies' and check its type, 
            if "replies" in comment_data and isinstance(comment_data["replies"], dict):

                # recursively call the extract_comments function to process the reply and all other replies within the reply 
                extract_comments(comment_data["replies"]["data"]["children"], comments_output_list)

    return comments_output_list


#############################
#  DATABASE TABLE CREATION  #
#############################

# Create a database engine using SQLAlchemy
engine = create_engine('sqlite:///../data/database.db', echo=False, isolation_level="AUTOCOMMIT")

# the database is created when we make a connection with the engine
with engine.connect() as conn:
    pass

def create_table(table_name, columns_text):
    # Construct the CREATE TABLE statement
    create_statement = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        {columns_text}
    );
    """

    # Execute the statements 
    with engine.connect() as conn:
        conn.execute(text(f'DROP TABLE IF EXISTS {table_name}'))  
        conn.execute(text(create_statement)) 

#####################
# Post agggregation #
#####################

def aggregate_posts(posts_df, group_by_columns):
    """
    We using the ```.agg``` method to aggregate our data. 
    We count the number of post id's, add the post upvotes together using sum, 
    and use first for subscribers since it is categorical and we don't want to collect it in any way. 
    """

    grouped_df = posts_df.groupby(group_by_columns).agg({
        "post_id": "count",  
        "post_upvotes": "sum",  
        "subscribers": "first"  
    }).reset_index()

    return grouped_df

########################
# Comment agggregation #
########################

# used in the same spirit as the post aggregation
def aggregate_comments(comments_df, group_by_columns):
    grouped_df = comments_df.groupby(group_by_columns).agg({
        "comment_id": "count",  # Count comments
        "comment_upvotes": "sum",  # Sum of comment upvotes
    }).reset_index()

    return grouped_df


################################
# Comment scaling by 100k subs #
################################


def scale_columns_per_100k(df, columns):
    """
    Scales multiple columns per 100,000 subscribers.
    The double asterisk allows us to unpack the dictionary in the assign method and pass multiple key word arguments
    A flexible number of columns are created using a dictionary comprehension
    the dictionary comprehension is created from the function argument columns, which is a list
    """
    return df.assign(**{f"{col}_per_100k_subs": df[col] / df["subscribers"] * 100000 for col in columns})