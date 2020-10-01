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







# Introducing Sochial

A social networking platform for readers and writers. Where you can blog, share, read, write, learn, publish* and earn*.

Things you can discover on Sochial -

 * Poems.
 * Blogs.
 * Musings.
 * Writing Prompts.
 * Other users' thoughts, beliefs, ideas, and stories.
___

### Blogs
 * Publish your experiences, passions, thoughts, beliefs, and get recognised by the right people and develop an audience.
Once a fellow Sochialite follows you they have essentially also subscribed to your blog.  


 * Essentially, blogs are to Sochial as to Channels are to YouTube, as a matter of fact, each blog is also a podcast in a way.

 * Speech is synthesised from the text in your posts and an audio version of the blog post can be played just like an episode of a podcast.

 * Fellow Sochialites can find your content based on their interests, their past reading history, searches, recommendations, daily top 150 blog posts, and what users they follow read.

*(and nope, we won't sell ANY of your data. All data stored by us is solely for improving the overall experience of the app and/or providing analytics to your posts)*

*PS: The number of followers you have has zero effect on rankings when it comes to being featured in the daily top 150 blog posts.*

### Poems
Poetry can do in a few stanzas what it takes many essays pages to do. In many poems, the meaning is something that must be constructed by the reader, while essays are much more explicit about their meaning. When you synthesize your own interpretation of a poem, the message you take away from it ends up being much more personal, and because of this, often stronger.

There are things you can express with music that you can't express as elegantly with words, but there are equally things that you can express with words in ways that you can't express as skillfully with music. If an artist wants to use words as their medium without filling hundreds of pages, poetry is a strong choice.

As Robert Frost said, "Poetry is when an emotion has found its thought and the thought has found words."

Whether you're a novice or a poetry whiz, you're always free to ask for help from your followers or the forum section (Coming soon)
 
Post poems and get feedback from fellow Sochialites as well as find users who can relate with your experiences and feelings or have the same idealogy as yours.

### Writing Prompts
Write story starters that light a fire under other writers (and readers alike), add writing prompts that are revamps of established fictional universes or the next bestseller.

Other Sochialites can add endings to your writing prompts and.. Well..**let the games begin!**

### Musings
Share shower thoughts, theories, aphorisms, and your own quotes with beautiful photos in the background, to add a little charm.

***Note: Poems and Musings are the only posts that can be posted anonymously.***

In case you're worried that since Sochial is a newly emerging writing (and reading) platform, your posts could be deleted if Sochial goes downhill, you always have the option to get every poem, writing prompt, and blog post mailed to you whenever you post.

