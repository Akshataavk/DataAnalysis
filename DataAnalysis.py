
from googleapiclient.discovery import build 
import json
import csv

# API key
api_key = 'AIzaSyDh7aJiJmKb8YD3At1CE4tiRbo9jJxmScs'
# Building the service object
youtubeService = build('youtube', 'v3', developerKey=api_key)


# Function to clean comments
def clean_comment(comment):
  # Remove HTML tags
  comment = re.sub(r'<.*?>', '', comment)

  # Remove emojis (optional, adjust the regex pattern if needed)
  comment = re.sub(r'[^\w\s]', '', comment)

  # Remove URLs
  comment = re.sub(r'http\S+', '', comment)

  # Remove extra whitespace
  comment = re.sub(r'\s+', ' ', comment).strip()

  return comment.lower()  # Convert to lowercase for case-insensitive processing

# Get the statistics of a video
def get_video_stats(video_id):
    # Calling videos().list method to retrieve details of the video
    request = youtubeService.videos().list(
        part='statistics',
        id=video_id
    )
    response = request.execute()
    # print(response)

    # Fetch statistics from the response
    if ('items' in response) and len(response['items']) > 0:
        statistics = response['items'][0]['statistics']
        return statistics
    else:
        return None
    
# Get the video comments
def get_video_comments(video_id, max_results=100):
    # Call the commentThreads.list method to retrieve comments
    request = youtubeService.commentThreads().list(
        part='snippet',
        videoId=video_id,
        maxResults=max_results
    )
    # response = request.execute()
    # jsonResponse = json.dumps(response)
    # print(jsonResponse)
    # print(jsonResponse.encode("utf-8"))

    comments = []
    while request is not None:
        response = request.execute()
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)
        # Check if there is more than one page of comments
        if ('nextPageToken') in response:
            request = youtubeService.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=max_results,
                pageToken=response['nextPageToken']
            )
        else:
            request = None

    return comments

# Get the video upload date and time
def get_video_upload_date(video_id):
    # Calling the videos().list method to retrieve the date
    request = youtubeService.videos().list(
        part='snippet',
        id=video_id,
    )
    response = request.execute()
    # jsonResponse = json.dumps(response)
    # print(jsonResponse)
     # Extract the statistics from the response
    if ('items' in response) and len(response['items']) > 0:
        snippet = response['items'][0]['snippet']
        return snippet
    else:
        return None

# Write to a csv file
def writeToFile(data, filename):
    with open(filename, mode="w", newline="") as file:        
        writer = csv.writer(file)
        writer.writerows(data)
        print(f"{filename} saved.")    


if __name__ == '__main__':
    # List of video id's
    statsList = [["Channel Id", "Video Id", "Title", "Date uploaded", "Views", "Likes", "Favorite", "Comments"]]
    commentsList = []
    video_id_list = ['7YhydjSnuL4']
    for id in video_id_list:
        statsTempList = []
        snippet = get_video_upload_date(id)
        stats = get_video_stats(id)
        if stats and snippet:
            print(f"Channel id: {snippet['channelId']}")
            statsTempList.append(snippet['channelId'])
            print(f"Video id: {id}")
            statsTempList.append(id)
            print(f"Title: {snippet['title']}")
            statsTempList.append(snippet['title'])
            print(f"Date uploaded: {snippet['publishedAt']}")
            statsTempList.append(snippet['publishedAt'])
            print(f"View count: {stats['viewCount']}")
            statsTempList.append(stats['viewCount'])
            print(f"Like count: {stats['likeCount']}")
            statsTempList.append(stats['likeCount'])
            print(f"Favorite count: {stats['favoriteCount']}")
            statsTempList.append(stats['favoriteCount'])
            print(f"Comment count: {stats['commentCount']}")
            statsTempList.append(stats['commentCount'])
            print(statsTempList)
            statsList.append(statsTempList)
            print("")
        
            # comments section

            comments = get_video_comments(id)
            header = [f"Video Id: {id}", "Cleaned Comments"]
            commentsList.append(header)
            for index, comment in enumerate(comments):
                commentsTempList = []
                commentsTempList.append(index + 1)
                commentsTempList.append(comment)
                commentsList.append(commentsTempList)
            
            else:
                print(f"Video with ID {id} not found")

    # print(statsList)
    writeToFile(statsList, "stats.csv")
    writeToFile(commentsList, "Cleanedcomments.csv")