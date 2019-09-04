# Motion Project - Backend

An API that can be used to create a social network platform. I worked on this project during Full-Stack development bootcamp. 
It was a one week individual project and the goal was to achieve as much as we can.

## Technologies

* Python
* Django
* Django REST framework
* Docker

## Description

### Content of a Social Post From a User:

* User who posted

* Datetime when posted

* Title

* Text content

* External link content

* Picture/Gif upload

* Likes relation

* Share relation ot another Post

## Endpoints

### Auth

/api/auth/token/ POST: Get a new JWT by passing username and password

/api/auth/token/refresh/ POST: Get a new JWT by passing an old still valid refresh token.

/api/auth/token/verify/ POST: Verify a token by passing the access token in the body

/api/auth/password-reset/ POST: Reset users password by sending a validation code in an email

/api/auth/password-reset/validate/ POST: Validate password reset token and set new password for the user

### Feed
/api/feed/ GET: lists all the posts of all users in chronological order

/api/feed/?search=<str:search_string> GET: Search posts of all users and list result in chronological order

/api/feed/<int:user_id>/ GET: lists all the posts of a specific user in chronological order

/api/feed/followees/ GET: lists all the posts of followed users in chronological order

/api/feed/friends/ GET: lists all the posts of the logged in user’s friends in chronological order

### Posts

/api/posts/<int:post_id>/ GET: get a specific post by ID and display all the information about that post

/api/posts/<int:post_id>/ PATCH: update a specific post (only allow owner of post or admin)

/api/posts/<int:post_id>/ DELETE: delete a post by ID (only allow owner of post or admin)

/api/posts/like/<int:post_id>/ POST: like a post

/api/posts/like/<int:post_id>/ DELETE: remove like from a post

/api/posts/new-post/ POST: user can make a new post by sending post data

/api/posts/likes/ GET: the list of the posts the user likes

/api/posts/share-post/<int:post_id>/ POST: User can share a post they like from another user (this creates a new post on this user with no content but a share relation)

### Users

/api/users/follow/<int:user_id>/ POST: follow a user

/api/users/follow/<int:user_id>/ DELETE: unfollow a user

/api/users/followers/ GET: List of all the logged in user’s followers

/api/users/following/ GET: List of all the people the user is following

/api/users/ GET: Get all the users

/api/users/?search=<str:search_string> GET: Search users

/api/users/<int:user_id>/ GET: Get specific user profile

/api/users/friendrequests/<int:user_id>/ POST: Send friend request to another user

/api/users/friendrequests/ GET: List all open friend requests from others

/api/users/friendrequests/pending/ GET: List all the logged in user’s pending friend requests

/api/users/friendrequests/accept/<int:request_id>/ POST: Accept an open friend request

/api/users/friendrequests/reject/<int:request_id>/ POST: Reject an open friend request

/api/users/friends/ GET: List all accepted friends

/api/users/friends/unfriend/<int:user_id>/ DELETE: Unfriend a user

### Me

/api/me/ GET: Get logged in user’s profile (as well private information like email, etc.)

/api/me/ POST: Update the logged in user’s profile public info)

### Registration

/api/registration/ POST: Register a new user by asking for an email (send email validation code)

/api/registration/validation/ POST: Validate a new registered user with a validation code sent by email

### Emails

Send an email to the user if they get followed by someone

Send an email to the user if they get a friend request

Send an email if a friend request gets accepted

Send an email to the user if a friend makes a post

