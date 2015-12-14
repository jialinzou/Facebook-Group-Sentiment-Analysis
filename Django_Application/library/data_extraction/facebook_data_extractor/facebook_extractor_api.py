# facebook_extractor_api.py contains APIs that are required to get group post information

# Facebook API for getting data from a group
# 3 Parameters:
#   1. Group ID or Name
#   2. Limit number of results returned
#   3. Access Token
group_url = "https://graph.facebook.com/%s/?fields=feed.limit(%s){from,message}&access_token=%s"