from flask_restful import Api
from app import app
from api.user.userapi import User
from api.poem.poemapi import Poem
from api.poem.poembyidapi import PoemByID
from api.poem.poemsbyuserid import PoemsByUserID
from api.poem.poemcommentapi import PoemCommentByID
from api.musing.musingapi import Musing
from api.musing.musingbyidapi import MusingByID
from api.musing.musingsbyuserid import MusingsByUserID
from api.musing.musingcommentapi import MusingCommentByID
from api.writingprompt.promptapi import Prompt
from api.writingprompt.promptbyidapi import PromptByID
from api.writingprompt.promptsbyuserid import PromptsByUserID
from api.writingprompt.promptcommentapi import PromptCommentByID
from api.bookmark.bookmarkapi import Bookmark

restServerInstance = Api(app)

# GET     /users/{user_id}/followers           Get a list of followers of a user
# GET     /users/{user_id}/followers_count     Get the number of followers of a user
# GET     /users/{user_id}/following           Get the list of users this user is following
# GET     /users/{user_id}/following_count     Get the number of users this user follows
# GET     /users/{user_id}/posts               Get the messages sent by a user
# GET     /users/{user_id}/timeline            Get the timeline for this user
# PUT     /users/{user_id}                     Create a new user
# PUT     /users/{user_id}/following/{target}  Follow a user
# DELETE  /users/{user_id}/following/{target}  Unfollow a user
restServerInstance.add_resource(User, "/api/v1.0/users/id/<string:userID>")
restServerInstance.add_resource(Bookmark, "/api/v1.0/users/id/<string:userID>/bookmarks")
# restServerInstance.add_resource(UserRelationship, "/api/v1.0/users/relation/id/<string:userID>/<string:otherUserID>")


# add posts and get posts via pagination
restServerInstance.add_resource(Poem, "/api/v1.0/poems", endpoint='all_poems')
restServerInstance.add_resource(Musing, "/api/v1.0/musings", endpoint='all_musings')
restServerInstance.add_resource(Prompt, "/api/v1.0/prompts", endpoint='all_prompts')
restServerInstance.add_resource(Blog, "/api/v1.0/blogs", endpoint='all_blogs')

# get, edit, update, delete post by it's id
restServerInstance.add_resource(PoemByID, "/api/v1.0/poems/id/<string:poemID>", endpoint='poem_by_id')
restServerInstance.add_resource(MusingByID, "/api/v1.0/musings/id/<string:musingID>", endpoint='musing_by_id')
restServerInstance.add_resource(PromptByID, "/api/v1.0/prompts/id/<string:promptID>", endpoint='prompt_by_id')
restServerInstance.add_resource(BlogByID, "/api/v1.0/blogs/id/<string:blogID>", endpoint='blog_by_id')

# get list of all posts made by particular user
restServerInstance.add_resource(PoemsByUserID, "/api/v1.0/poems/user/id/<string:userID>", endpoint='poems_by_user_id')
restServerInstance.add_resource(MusingsByUserID, "/api/v1.0/musings/user/id/<string:userID>",
                                endpoint='musings_by_user_id')
restServerInstance.add_resource(PromptsByUserID, "/api/v1.0/prompts/user/id/<string:userID>",
                                endpoint='prompts_by_user_id')
restServerInstance.add_resource(BlogsByUserID, "/api/v1.0/blogs/user/id/<string:userID>",
                                endpoint='blogs_by_user_id')

# get, edit, update, delete comment to a particular post by it's id
restServerInstance.add_resource(PoemCommentByID, "/api/v1.0/poems/id/comments/<string:poemID>",
                                endpoint='poem_comment_by_id')
restServerInstance.add_resource(MusingCommentByID, "/api/v1.0/musings/id/comments/<string:musingID>",
                                endpoint='musing_comment_by_id')
restServerInstance.add_resource(PromptCommentByID, "/api/v1.0/prompts/id/comments/<string:promptID>",
                                endpoint='prompt_comment_by_id')
restServerInstance.add_resource(BlogCommentByID, "/api/v1.0/blogs/id/comments/<string:blogID>",
                                endpoint='blog_comment_by_id')



from api import *

restServerInstance.init_app(app)

# restServerInstance.add_resource(PoemStatsIncByID, "/api/v1.0/poems/stats/inc/id/<string:poemID>",
#                                 endpoint='poem_stats_inc_by_id')
# restServerInstance.add_resource(PoemStatsDecByID, "/api/v1.0/poems/stats/dec/id/<string:poemID>",
#                                 endpoint='poem_stats_dec_by_id')
# restServerInstance.add_resource(Poem, "/api/v1.0/prompts",endpoint='all_prompts')
# restServerInstance.add_resource(PoemByID, "/api/v1.0/prompts/id/<string:poemId>",endpoint='single_prompt')
# restServerInstance.add_resource(PoemByUserID, "/api/v1.0/prompts/id/<string:poemId>",endpoint='single_prompt')
