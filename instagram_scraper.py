import instaloader

def get_insta_reels_stat(username):

    # # Create Instaloader instance
    L = instaloader.Instaloader()

    # # Get profile from username or profile link
    profile = instaloader.Profile.from_username(L.context, username)
    Followers = profile.followers
    max = 10
    i=0
    likes = 0
    views = 0

    for post in profile.get_posts():
        if i < max and post.video_view_count != None:
            i+=1
            likes+=post.likes
            views+=post.video_view_count
    avg_views = views/10
    Client_engagement = Followers/likes if likes>0 else 0
    return{
        'Channel Name': username,
        'Total Views': views,
        'Total Likes': likes,
        'Average views':avg_views,
        'Client Engagement':Client_engagement
    }