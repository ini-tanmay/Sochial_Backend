from flask_restful import Api
from app import app
from api.user.userapi import User
from api.post.postapi import Post
from api.post.postbyidapi import PostByID
from api.post.postsbyuserid import PostsByUserID
from api.bookmark.bookmarkapi import Bookmark
from api.comment.postcommentapi import PostCommentByID
from api.comment.commentreplyapi import CommentReplyByID
from api.snippet.snippetsbypromptid import SnippetsByPromptID

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
restServerInstance.add_resource(User, "/api/v1.0/user/id/<string:userID>")
restServerInstance.add_resource(Bookmark, "/api/v1.0/user/id/<string:userID>/bookmarks")
restServerInstance.add_resource(Post, "/api/v1.0/<string:type>s", endpoint='all_posts')
restServerInstance.add_resource(SnippetsByPromptID, "/api/v1.0/snippets/<string:promptID>", endpoint='get_snippets_by_id')
restServerInstance.add_resource(PostByID, "/api/v1.0/<string:type>/id/<string:postID>", endpoint='post_by_id')
restServerInstance.add_resource(PostCommentByID, "/api/v1.0/<string:type>/id/<string:postID>/comments",
                                endpoint='post_comments_by_id')
restServerInstance.add_resource(CommentReplyByID, "/api/v1.0/<string:type>/id/<string:postID>/comment/<int:timeStamp>",
                                endpoint='post_comment_reply_by_id')
restServerInstance.add_resource(PostsByUserID, "/api/v1.0/<string:type>s/user/id/<string:userID>",
                                endpoint='posts_by_user_id')

# restServerInstance.add_resource(UserRelationship, "/api/v1.0/users/relation/id/<string:userID>/<string:otherUserID>")


# add posts and get posts via pagination
# restServerInstance.add_resource(Musing, "/api/v1.0/musings", endpoint='all_musings')
# restServerInstance.add_resource(Prompt, "/api/v1.0/prompts", endpoint='all_prompts')
# restServerInstance.add_resource(Blog, "/api/v1.0/blogs", endpoint='all_blogs')

# get, edit, update, delete post by it's id
# restServerInstance.add_resource(MusingByID, "/api/v1.0/musings/id/<string:musingID>", endpoint='musing_by_id')
# restServerInstance.add_resource(PromptByID, "/api/v1.0/prompts/id/<string:promptID>", endpoint='prompt_by_id')
# restServerInstance.add_resource(BlogByID, "/api/v1.0/blogs/id/<string:blogID>", endpoint='blog_by_id')

# get list of all posts made by particular user
# restServerInstance.add_resource(MusingsByUserID, "/api/v1.0/musings/user/id/<string:userID>",
#                                 endpoint='musings_by_user_id')
# restServerInstance.add_resource(PromptsByUserID, "/api/v1.0/prompts/user/id/<string:userID>",
#                                 endpoint='prompts_by_user_id')
# restServerInstance.add_resource(BlogsByUserID, "/api/v1.0/blogs/user/id/<string:userID>",
#                                 endpoint='blogs_by_user_id')

# get, edit, update, delete comment to a particular post by it's id


from api import *

restServerInstance.init_app(app)

# restServerInstance.add_resource(PostStatsIncByID, "/api/v1.0/posts/stats/inc/id/<string:postID>",
#                                 endpoint='post_stats_inc_by_id')
# restServerInstance.add_resource(PostStatsDecByID, "/api/v1.0/posts/stats/dec/id/<string:postID>",
#                                 endpoint='post_stats_dec_by_id')
# restServerInstance.add_resource(Post, "/api/v1.0/prompts",endpoint='all_prompts')
# restServerInstance.add_resource(PostByID, "/api/v1.0/prompts/id/<string:postId>",endpoint='single_prompt')
# restServerInstance.add_resource(PostByUserID, "/api/v1.0/prompts/id/<string:postId>",endpoint='single_prompt')
