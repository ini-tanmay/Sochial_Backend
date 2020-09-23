# Sochial_Backend




### GET
get followers by userid /api/v1.0/users/id/<string:userID>/followers/<int:last_no>
check if one userid follows otheruserid /api/v1.0/users/id/<string:myUserID>/follows/<string:otherUserID>/check
get following by userid /api/v1.0/users/id/<string:userID>/following
get a post by it's id /api/v1.0/<string:type>/id/<string:postID>
get list of posts with pagination /api/v1.0/<string:type>/id/<string:postID>?limit=11&last_id=5qwfessntunt89wfuyfp
get list of all posts uploaded by a single user /api/v1.0/<string:type>s/user/id/<string:userID>


### POST
upload a post    /api/v1.0/types 
increment views for post /api/v1.0/posts/user/id/<string:userID>?postID=5qiseulwuqnfstunfunp
increment views for blog /api/v1.0/blogs/user/id/<string:userID>?blogID=5qiseulwuqnfstunfunp
add comment for post /api/v1.0/<string:type>/id/comments/<string:postID>
add bookmark for a user /api/v1.0/users/id/<string:userID>/bookmarks
create user /api/v1.0/users/id/<string:userID>
myuser_follows_otheruser /api/v1.0/users/id/<string:otherUserID>/name/<string:name>/username/<string:username>/follow
myuser_unfollows_otheruser /api/v1.0/users/id/<string:myUserID>/unfollow/<string:otherUserID>
increment views  /api/v1.0/<string:type>s/user/id/<string:userID>

### PUT
increment likes /api/v1.0/users/id/<string:userID>/posts/id/<string:postID>/l/inc/<string:type>
decrement likes /api/v1.0/users/id/<string:userID>/posts/id/<string:postID>/l/dec/<string:type>
increment awards /api/v1.0/users/id/<string:userID>/posts/id/<string:postID>/a/inc/<string:type>
increment plays  /api/v1.0/blog/user/id/<string:userID>
update post /api/v1.0/<string:type>/id/<string:postID>
update user /api/v1.0/users/id/<string:userID>

### DELETE
delete post by postid /api/v1.0/<string:type>/id/<string:postID>
delete bookmarb by postid /api/v1.0/users/id/<string:userID>/bookmarks?postID=23lf8plf8pl328pp
