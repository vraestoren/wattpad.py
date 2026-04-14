from uuid import uuid4
from requests import Session

class WattPad:
	def __init__(
			self, locale: str = "en_US", language_id: int = 1) -> None:
		self.api = "https://api.wattpad.com"
		self.public_api = "https://www.wattpad.com"
		self.locale = locale
		self.wp_token = None
		self.language_id = language_id
		self.tracking_id = f"{uuid4()}"
		self.session = Session()
		self.session.headers = {
			"User-Agent": f"Android App v9.76.0; Model: ASUS_Z01QD; Android SDK: 25; Connection: None; Locale: {self.locale};",
			"X-Accept-Language": self.locale,
			"Cookie": f"locale={self.locale}; lang={self.language_id}; wp_id={self.tracking_id};"
		}


	def _get(self, endpoint: str, params: dict = None) -> dict:
		return self.session.get(endpoint, params=params or {}).json()

	def _post(
			self, endpoint: str, data: dict = None, params: dict = None) -> dict:
		return self.session.post(endpoint, data=data, params=params).json()

	def _delete(self, endpoint: str, params: dict = None) -> dict:
		return self.session.delete(endpoint, params=params or {}).json()

	def _put(
			self, endpoint: str, data: dict = None, params: dict = None) -> dict:
		return self.session.put(endpoint, data=data, params=params).json()

	def login(
			self,
			username: str,
			password: str,
			fields: str = "token,ga,user(username,description,avatar,name,email,genderCode,language,birthdate,verified,isPrivate,ambassador,is_staff,follower,following,backgroundUrl,votesReceived,numFollowing,numFollowers,createDate,followerRequest,website,facebook,twitter,followingRequest,numStoriesPublished,numLists,location,externalId,programs,showSocialNetwork,verified_email,has_accepted_latest_tos,email_reverification_status,language,inbox(unread),has_password,connectedServices)") -> dict:
		data = {
			"type": "wattpad",
			"username": username,
			"password": password,
			"fields": fields
		}
		response = self._post(f"{self.api}/v4/sessions", data)
		if "token" in response:
			self.wp_token = response["token"]
			self.user_id = self.wp_token.split(":")[0]
			self.username = response["user"]["username"]
			self.session.headers["cookie"] += f"token={self.wp_token}"
		return response

	def register(
			self,
			username: str,
			password: str,
			email: str,
			has_accepted_latest_tos: bool = True,
			fields: str = "token,ga,user(username,description,avatar,name,email,genderCode,language,birthdate,verified,isPrivate,ambassador,is_staff,follower,following,backgroundUrl,votesReceived,numFollowing,numFollowers,createDate,followerRequest,website,facebook,twitter,followingRequest,numStoriesPublished,numLists,location,externalId,programs,showSocialNetwork,verified_email,has_accepted_latest_tos,email_reverification_status,language,inbox(unread),has_password,connectedServices)") -> dict:
		data = {
			"type": "wattpad",
			"username": username,
			"password": password,
			"email": email,
			"language": self.language_id,
			"has_accepted_latest_tos": has_accepted_latest_tos,
			"fields": fields,
			"trackingId": self.tracking_id
		}
		return self._post(f"{self.api}/v4/users", data)

	def validate_email(self, email: str) -> dict:
		params = {
			"email": email
		}
		return self._get(
			f"{self.public_api}/api/v3/users/validate", params)

	def validate_username(self, username: str) -> dict:
		params = {
			"username": username
		}
		return self._get(
			f"{self.public_api}/api/v3/users/validate", params)

	def get_password_strength_policies(self) -> dict:
		return self._get(
			f"{self.public_api}/5/password-strength/policies")

	def check_password_strength(self, username: str, password: str) -> dict:
		data = {
			"password": password,
			"requester": {
				"username": username
			}
		}
		return self._post(
			f"{self.public_api}/v5/password-strength/check", data)

	def get_language_ids(self) -> dict:
		return self._get(f"{self.public_api}/apiv2/getlang")

	def get_categories(self) -> dict:
		params = {
			"language": self.language_id
		}
		return self._get(
			f"{self.public_api}/api/v3/categories", params)

	def get_user_archive(
			self,
			username: str,
			fields: str = "nextUrl,total,stories(id,title,name,cover,deleted,user,readingPosition,modifyDate)",
			limit: int = 40) -> dict:
		params = {
			"fields": fields,
			"limit": limit,
			"wp_token": self.wp_token
		}
		return self._get(
			f"{self.public_api}/api/v3/users/{username}/archive", params)

	def get_user_lists(
			self,
			username: str,
			fields: str = "lists(user,id,action,name,numStories,featured,promoted,description,cover),nextUrl",
			limit: int = 10) -> dict:
		params = {
			"fields": fields,
			"limit": limit,
			"wp_token": self.wp_token
		}
		return self._get(
			f"{self.public_api}/api/v3/users/{username}/lists", params)

	def get_user_wallet(self, username: str) -> dict:
		params = {
			"wp_token": self.wp_token
		}
		return self._get(
			f"{self.api}/v5/users/{username}/wallet")

	def get_user_library(
			self,
			username: str,
			fields: str = "last_sync_timestamp,nextUrl,total,stories(id,title,length,createDate,modifyDate,promoted,user,description,cover,completed,isPaywalled,paidModel,categories,tags,numParts,readingPosition,deleted,dateAdded,lastPublishedPart(createDate),story_text_url(text),parts(id,title,modifyDate,length,deleted,text_url(text)))",
			limit: int = 40) -> dict:
		params = {
			"fields": fields,
			"limit": limit,
			"wp_token": self.wp_token
		}
		return self._get(
			f"{self.public_api}/api/v3/users/{username}/library", params)

	def get_user_stories(
			self,
			username: str,
			fields: str = "stories(id,title,length,createDate,modifyDate,voteCount,readCount,commentCount,language,user,description,cover,url,completed,isPaywalled,categories,tags,numParts,readingPosition,deleted,story_text_url(text),copyright,rating,mature,ratingLocked,tagRankings,hasBannedCover,parts(id,title,voteCount,commentCount,videoId,readCount,photoUrl,modifyDate,length,voted,deleted,text_url(text),dedication,url,wordCount,draft,hash,hasBannedImages),isAdExempt),nextUrl",
			drafts: int = 1) -> dict:
		params = {
			"fields": fields,
			"drafts": drafts,
			"wp_token": self.wp_token
		}
		return self._get(
			f"{self.public_api}/api/v3/users/{username}/stories", params)

	def get_user_subscription_prompts(self, username: str) -> dict:
		params = {
			"wp_token": self.wp_token
		}
		return self._get(
			f"{self.api}/v5/users/{username}/subscriptions/prompts", params)

	def get_user_published_stories(
			self,
			username: str,
			fields: str = "stories(id),nextUrl") -> dict:
		params = {
			"fields": fields,
			"wp_token": self.wp_token
		}
		return self._get(
			f"{self.api}/v4/users{username}/stories/published", params)

	def get_browse_topics(self, type: str = "onboarding") -> dict:
		params = {
			"language": self.language_id,
			"type": type,
			"wp_token": self.wp_token
		}
		return self._get(
			f"{self.api}/v5/browse/topics", params)

	def get_products_list(self) -> dict:
		params = {
			"wp_token": self.wp_token
		}
		return self._get(
			f"{self.api}/v5/subscriptions/products", params)

	def get_home_page(self) -> dict:
		params = {
			"wp_token": self.wp_token
		}
		return self._get(
			f"{self.api}/v5/home", params)

	def get_story_info(
			self,
			story_id: int,
			drafts: int = 0,
			include_deleted: int = 1,
			fields: str = "id,title,length,createDate,modifyDate,voteCount,readCount,commentCount,url,promoted,sponsor,language,user,description,cover,highlight_colour,completed,isPaywalled,paidModel,categories,numParts,readingPosition,deleted,dateAdded,lastPublishedPart(createDate),tags,copyright,rating,story_text_url(text),,parts(id,title,voteCount,commentCount,videoId,readCount,photoUrl,modifyDate,length,voted,deleted,text_url(text),dedication,url,wordCount),isAdExempt,tagRankings") -> dict:
		params = {
			"drafts": drafats,
			"include_deleted": include_deleted,
			"fields": fields,
			"wp_token": self.wp_token
		}
		return self._get(
			f"{self.public_api}/api/v3/stories/{story_id}", params)

	def get_similar_stories(
			self,
			story_id: int,
			fields: str = "id,title,readCount,cover,isPaywalled",
			limit: int = 10) -> dict:
		params = {
			"fields": fields,
			"limit": limit,
			"wp_token": self.wp_token
		}
		return self._get(
			f"{self.public_api}/api/v3/stories/{story_id}", params)

	def get_user_info(
			self,
			username: str,
			fields: str = "username,description,avatar,name,email,genderCode,language,birthdate,verified,isPrivate,ambassador,is_staff,follower,following,backgroundUrl,votesReceived,numFollowing,numFollowers,createDate,followerRequest,website,facebook,twitter,followingRequest,numStoriesPublished,numLists,location,externalId,programs,showSocialNetwork,verified_email,has_accepted_latest_tos,email_reverification_status,highlight_colour,safety(isMuted,isBlocked)") -> dict:
		params = {
			"fields": fields,
			"wp_token": self.wp_token
		}
		return self._get(
			f"{self.public_api}/api/v3/users/{username}", params)

	def get_user_followers(
			self,
			username: str,
			fields: str = "users(username,avatar,location,numFollowers,following,follower,followingRequest,followerRequest),nextUrl") -> dict:
		params = {
			"fields": fields,
			"wp_token": self.wp_token
		}
		return self._get(
			f"{self.public_api}/api/v3/users/{username}/followers", params)

	def get_user_followings(
			self,
			username: str,
			fields: str = "users(username,avatar,location,numFollowers,following,follower,followingRequest,followerRequest),nextUrl",
			limit: int = 10,
			offset: int = 10) -> dict:
		params = {
			"fields": fields,
			"wp_token": self.wp_token,
			"limit": limit,
			"offset": offset
		}
		return self._get(
			f"{self.public_api}/api/v3/users/{username}/following", params)

	def ignore_user(self, username: str) -> dict:
		data = {
			"id": username,
			"action": "ignore_user"
		}
		params = {
			"wp_token": self.wp_token
		}
		return self._post(
			f"{self.public_api}/apiv2/ignoreuser", data, params).json()

	def unignore_user(self, username: str) -> dict:
		data = {
			"id": username,
			"action": "unignore_user"
		}
		params = {
			"wp_token": self.wp_token
		}
		return self._post(
			f"{self.public_api}/apiv2/ignoreuser", data, params).json()

	def resend_email_verification(self) -> dict:
		data = {
			"activation_email": True
		}
		params = {
			"wp_token": self.wp_token
		}
		return self._post(
			f"{self.public_api}/api/v3/users/validate", data, params).json()

	def get_wall_comments(
			self,
			username: str,
			fields: str = "messages(id,body,createDate,from,numReplies,isOffensive,isReply,latestReplies),total,nextUrl",
			limit: int = 30) -> dict:
		params = {
			"fields": fields,
			"return": "data",
			"limit": limit,
			"wp_token": self.wp_token
		}
		return self._get(
			f"{self.api}/v4/users/{username}/messages", params)

	def change_email(
			self,
			email: str,
			password: str,
			authenticate: int = 1) -> dict:
		data = {
			"id": self.user_id,
			"email": email,
			"confirm_email": email,
			"password": password,
			"authenticate": authenticate
		}
		params = {
			"wp_token": self.wp_token
		}
		return self._post(
			f"{self.public_api}/apiv2/updateuseremail", data, params)

	def send_comment(
			self,
			username: str,
			message: str,
			broadcast: int = 0) -> dict:
		data = {
			"name": username,
			"body": message,
			"broadcast": broadcast
		}
		params = {
			"wp_token": self.wp_token
		}
		return self._post(
			f"{self.api}/v4/users/{username}/messages", data, params)

	def delete_comment(self, username: str, message_id: int) -> dict:
		params = {
			"wp_token": self.wp_token
		}
		return self._delete(
			f"{self.api}/v4/users/{username}/messages/{message_id}", params)

	def get_comment_replies(
			self,
			message_id: int,
			fields: str = "replies(id,body,createDate,from),nextUrl") -> dict:
		params = {
			"fields": fields,
			"wp_token": self.wp_token
		}
		return self._get(
			f"{self.api}/v4/messages/{message_id}", params)

	def follow_user(self, username: str) -> dict:
		params = {
			"users": username,
			"wp_token": self.wp_token
		}
		return self._post(
			f"{self.public_api}/api/v3/users/{self.username}/following", params)

	def unfollow_user(self, username: str) -> dict:
		params = {
			"users": username,
			"wp_token": self.wp_token
		}
		return self._delete(
			f"{self.public_api}/api/v3/users/{self.username}/following", params)

	def search_users(
			self,
			query: str,
			fields: str = "username,avatar,following,name,verified,ambassador,is_staff,programs",
			limit: int = 20,
			offset: int = 20) -> dict:
		params = {
			"fields": fields,
			"limit": limit,
			"offset": offset,
			"query": query,
			"wp_token": self.wp_token
		}
		return self._get(
			f"{self.public_api}/api/v3/users", params)

	def search_stories(
			self,
			query: str,
			mature: int = 1,
			free: int = 1,
			paid: int = 1,
			limit: int = 30,
			fields: str = "stories(id,title,voteCount,readCount,numParts,tags,description,user,mature,completed,rating,cover,promoted,isPaywalled,lastPublishedPart,sponsor(name,avatar),tracking(clickUrl,impressionUrl,thirdParty(impressionUrls,clickUrls)),contest(endDate,ctaLabel)),tags,nextUrl,total") -> dict:
		params = {
			"query": query,
			"mature": mature,
			"free": free,
			"paid": paid,
			"limit": limit,
			"fields": fields,
			"language": self.language_id,
			"wp_token": self.wp_token
		}
		return self._get(
			f"{self.api}/v4/search/stories", params)

	def search_lists(
			self,
			query: str,
			limit: int = 10,
			offset: int = 10) -> dict:
		params = {
			"query": query,
			"wp_token": self.wp_token,
			"limit": limit,
			"offset": offset
		}
		return self._get(
			f"{self.public_api}/v4/lists", params)

	def send_message(self, username: str, message: str) -> dict:
		data = {
			"sender": self.username,
			"recipient": username,
			"body": message
		}
		params = {
			"wp_token": self.wp_token
		}
		return self._post(
			f"{self.public_api}/api/v3/users/{self.username}/inbox/{username}", data, params)

	def delete_chat(self, username: str) -> dict:
		params = {
			"wp_token": self.wp_token
		}
		return self._delete(
			f"{self.public_api}/api/v3/users/{self.username}/inbox/{username}", params)

	def get_started_chats(self, limit: int = 20) -> dict:
		params = {
			"limit": limit,
			"wp_token": self.wp_token
		}
		return self._get(
			f"{self.public_api}/api/v3/users/{self.username}/inbox", params)

	def get_notifications(
			self,
			fields: str = "feed,nextUrl",
			limit: int = 10,
			direction: int = 0) -> dict:
		params = {
			"return": "data",
			"fields": fields,
			"limit": limit,
			"direction": direction,
			"wp_token": self.wp_token
		}
		return self._get(
			f"{self.public_api}/api/v3/users/{self.username}/notifications", params)

	def update_username(
			self,
			username: str,
			password: str,
			authenticate: int = 1) -> dict:
		data = {
			"id": self.user_id,
			"username": username,
			"password": password,
			"authenticate": authenticate
		}
		params = {
			"wp_token": self.wp_token
		}
		return self._post(
			f"{self.public_api}/apiv2/updateusername", data, params)

	def update_name(self, name: str) -> dict:
		data = {
			"name": name
		}
		params = {
			"wp_token": self.wp_token
		}
		return self._put(
			f"{self.public_api}/api/v3/users/{self.username}", data, params)

	def update_website(self, website: str) -> dict:
		data = {
			"website": website
		}
		params = {
			"wp_token": self.wp_token
		}
		return self._put(
			f"{self.public_api}/api/v3/users/{self.username}", data, params)
	
	def change_password(
			self,
			old_password: str,
			new_password: str,
			has_password: int = 1) -> dict:
		data = {
			"id": self.user_id,
			"new_password": new_password,
			"confirm_password": new_password,
			"old_password": old_password,
			"haspassword": has_password
		}
		params = {
			"wp_token": self.wp_token
		}
		return self._post(
			f"{self.public_api}/apiv2/updateuserpassword", data, params)
