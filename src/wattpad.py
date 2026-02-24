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
		response = self.session.post(
			f"{self.api}/v4/sessions", data=data).json()
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
		return self.session.post(
			f"{self.api}/v4/users", data=data).json()


	def validate_email(self, email: str) -> dict:
		return self.session.get(
			f"{self.public_api}/api/v3/users/validate?email={email}").json()

	def validate_username(self, username: str) -> dict:
		return self.session.get(
			f"{self.public_api}/api/v3/users/validate?username={username}").json()

	def get_password_strength_policies(self) -> dict:
		return self.session.get(
			f"{self.public_api}/5/password-strength/policies").json()

	def check_password_strength(self, username: str, password: str) -> dict:
		data = {
			"password": password,
			"requester": {
				"username": username
			}
		}
		return self.session.post(
			f"{self.public_api}/v5/password-strength/check", data=data).json()

	def get_language_ids(self) -> dict:
		return self.session.get(f"{self.public_api}/apiv2/getlang").json()

	def get_categories(self) -> dict:
		return self.session.get(
			f"{self.public_api}/api/v3/categories?language={self.language_id}").json()

	def get_user_archive(
			self,
			username: str,
			fields: str = "nextUrl,total,stories(id,title,name,cover,deleted,user,readingPosition,modifyDate)",
			limit: int = 40) -> dict:
		return self.session.get(
			f"{self.public_api}/api/v3/users/{username}/archive?fields={fields}&limit={limit}&wp_token={self.wp_token}").json()

	def get_user_lists(
			self,
			username: str,
			fields: str = "lists(user,id,action,name,numStories,featured,promoted,description,cover),nextUrl",
			limit: int = 10) -> dict:
		return self.session.get(
			f"{self.public_api}/api/v3/users/{username}/lists?fields={fields}&limit={limit}&wp_token={self.wp_token}").json()

	def get_user_wallet(self, username: str) -> dict:
		return self.session.get(
			f"{self.api}/v5/users/{username}/wallet?wp_token={self.token}").json()

	def get_user_library(
			self,
			username: str,
			fields: str = "last_sync_timestamp,nextUrl,total,stories(id,title,length,createDate,modifyDate,promoted,user,description,cover,completed,isPaywalled,paidModel,categories,tags,numParts,readingPosition,deleted,dateAdded,lastPublishedPart(createDate),story_text_url(text),parts(id,title,modifyDate,length,deleted,text_url(text)))",
			limit: int = 40) -> dict:
		return self.session.get(
			f"{self.public_api}/api/v3/users/{username}/library?fields={fields}&limit={limit}&wp_token={self.wp_token}").json()

	def get_user_stories(
			self,
			username: str,
			fields: str = "stories(id,title,length,createDate,modifyDate,voteCount,readCount,commentCount,language,user,description,cover,url,completed,isPaywalled,categories,tags,numParts,readingPosition,deleted,story_text_url(text),copyright,rating,mature,ratingLocked,tagRankings,hasBannedCover,parts(id,title,voteCount,commentCount,videoId,readCount,photoUrl,modifyDate,length,voted,deleted,text_url(text),dedication,url,wordCount,draft,hash,hasBannedImages),isAdExempt),nextUrl",
			drafts: int = 1) -> dict:
		return self.session.get(
			f"{self.public_api}/api/v3/users/{username}/stories?fields={fields}&drafts={drafts}&wp_token={self.wp_token}").json()

	def get_user_subscription_prompts(self, username: str) -> dict:
		return self.session.get(
			f"{self.api}/v5/users/{username}/subscriptions/prompts?wp_token={self.wp_token}").json()

	def get_user_published_stories(
			self,
			username: str,
			fields: str = "stories(id),nextUrl") -> dict:
		return self.session.get(
			f"{self.api}/v4/users{username}/stories/published?fields={fields}&wp_token={self.wp_token}").json()

	def get_browse_topics(self, type: str = "onboarding") -> dict:
		return self.session.get(
			f"{self.api}/v5/browse/topics?language={self.language_id}&type={type}&wp_token={self.wp_token}").json()

	def get_products_list(self) -> dict:
		return self.session.get(
			f"{self.api}/v5/subscriptions/products?wp_token={self.wp_token}").json()

	def get_home_page(self) -> dict:
		return self.session.get(
			f"{self.api}/v5/home?wp_token={self.wp_token}").json()

	def get_story_info(
			self,
			story_id: int,
			drafts: int = 0,
			include_deleted: int = 1,
			fields: str = "id,title,length,createDate,modifyDate,voteCount,readCount,commentCount,url,promoted,sponsor,language,user,description,cover,highlight_colour,completed,isPaywalled,paidModel,categories,numParts,readingPosition,deleted,dateAdded,lastPublishedPart(createDate),tags,copyright,rating,story_text_url(text),,parts(id,title,voteCount,commentCount,videoId,readCount,photoUrl,modifyDate,length,voted,deleted,text_url(text),dedication,url,wordCount),isAdExempt,tagRankings") -> dict:
		return self.session.get(
			f"{self.public_api}/api/v3/stories/{story_id}?drafts={drafts}&include_deleted={include_deleted}&fields={fields}&wp_token={self.wp_token}").json()

	def get_similar_stories(
			self,
			story_id: int,
			fields: str = "id,title,readCount,cover,isPaywalled",
			limit: int = 10) -> dict:
		return self.session.get(
			f"{self.public_api}/api/v3/stories/{story_id}?fields={fields}&limit={limit}&wp_token={self.wp_token}").json()

	def get_user_info(
			self,
			username: str,
			fields: str = "username,description,avatar,name,email,genderCode,language,birthdate,verified,isPrivate,ambassador,is_staff,follower,following,backgroundUrl,votesReceived,numFollowing,numFollowers,createDate,followerRequest,website,facebook,twitter,followingRequest,numStoriesPublished,numLists,location,externalId,programs,showSocialNetwork,verified_email,has_accepted_latest_tos,email_reverification_status,highlight_colour,safety(isMuted,isBlocked)") -> dict:
		return self.session.get(
			f"{self.public_api}/api/v3/users/{username}?fields={fields}&wp_token={self.wp_token}").json()

	def get_user_followers(
			self,
			username: str,
			fields: str = "users(username,avatar,location,numFollowers,following,follower,followingRequest,followerRequest),nextUrl") -> dict:
		return self.session.get(
			f"{self.public_api}/api/v3/users/{username}/followers?fields={fields}&wp_token={self.wp_token}").json()

	def get_user_followings(
			self,
			username: str,
			fields: str = "users(username,avatar,location,numFollowers,following,follower,followingRequest,followerRequest),nextUrl",
			limit: int = 10,
			offset: int = 10) -> dict:
		return self.session.get(
			f"{self.public_api}/api/v3/users/{username}/following?fields={fields}&wp_token={self.wp_token}&limit={limit}&offset={offset}").json()

	def ignore_user(self, username: str) -> dict:
		data = {
			"id": username,
			"action": "ignore_user"
		}
		return self.session.post(
			f"{self.public_api}/apiv2/ignoreuser?wp_token={self.wp_token}", data=data).json()

	def unignore_user(self, username: str) -> dict:
		data = {
			"id": username,
			"action": "unignore_user"
		}
		return self.session.post(
			f"{self.public_api}/apiv2/ignoreuser?wp_token={self.wp_token}", data=data).json()

	def resend_email_verification(self) -> dict:
		data = {
			"activation_email": True
		}
		return self.session.post(
			f"{self.public_api}/api/v3/users/validate?wp_token={self.wp_token}", data=data).json()

	def get_wall_comments(
			self,
			username: str,
			fields: str = "messages(id,body,createDate,from,numReplies,isOffensive,isReply,latestReplies),total,nextUrl",
			limit: int = 30) -> dict:
		return self.session.get(
			f"{self.api}/v4/users/{username}/messages?fields={fields}&return=data&limit={limit}&wp_token={self.wp_token}").json()

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
		return self.session.post(
			f"{self.public_api}/apiv2/updateuseremail?wp_token={self.wp_token}", data=data).json()

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
		return self.session.post(
			f"{self.api}/v4/users/{username}/messages?wp_token={self.wp_token}", data=data).json()

	def delete_comment(self, username: str, message_id: int) -> dict:
		return self.session.delete(
			f"{self.api}/v4/users/{username}/messages/{message_id}?wp_token={self.wp_token}").json()

	def get_comment_replies(
			self,
			message_id: int,
			fields: str = "replies(id,body,createDate,from),nextUrl") -> dict:
		return self.session.get(
			f"{self.api}/v4/messages/{message_id}?fields={fields}&wp_token={self.wp_token}").json()

	def follow_user(self, username: str) -> dict:
		return self.session.post(
			f"{self.public_api}/api/v3/users/{self.username}/following?users={username}&wp_token={self.wp_token}").json()

	def unfollow_user(self, username: str) -> dict:
		return self.session.delete(
			f"{self.public_api}/api/v3/users/{self.username}/following?users={username}&wp_token={self.wp_token}").json()

	def search_users(
			self,
			query: str,
			fields: str = "username,avatar,following,name,verified,ambassador,is_staff,programs",
			limit: int = 20,
			offset: int = 20) -> dict:
		return self.session.get(
			f"{self.public_api}/api/v3/users?fields={fields}&limit={limit}&offset={offset}&query={query}&wp_token={self.wp_token}").json()

	def search_stories(
			self,
			query: str,
			mature: int = 1,
			free: int = 1,
			paid: int = 1,
			limit: int = 30,
			fields: str = "stories(id,title,voteCount,readCount,numParts,tags,description,user,mature,completed,rating,cover,promoted,isPaywalled,lastPublishedPart,sponsor(name,avatar),tracking(clickUrl,impressionUrl,thirdParty(impressionUrls,clickUrls)),contest(endDate,ctaLabel)),tags,nextUrl,total") -> dict:
		return self.session.get(
			f"{self.api}/v4/search/stories?query={query}&mature={mature}&free={free}&paid={paid}&limit={limit}&fields={fields}&language={self.language_id}&wp_token={self.wp_token}").json()

	def search_lists(
			self,
			query: str,
			limit: int = 10,
			offset: int = 10) -> dict:
		return self.session.get(
			f"{self.public_api}/v4/lists?query={query}&wp_token={self.wp_token}&limit={limit}&offset={offset}").json()

	def send_message(self, username: str, message: str) -> dict:
		data = {
			"sender": self.username,
			"recipient": username,
			"body": message
		}
		return self.session.post(
			f"{self.public_api}/api/v3/users/{self.username}/inbox/{username}?wp_token={self.wp_token}", data=data).json()

	def delete_chat(self, username: str) -> dict:
		return self.session.delete(
			f"{self.public_api}/api/v3/users/{self.username}/inbox/{username}?wp_token={self.wp_token}").json()

	def get_started_chats(self, limit: int = 20) -> dict:
		return self.session.get(
			f"{self.public_api}/api/v3/users/{self.username}/inbox?limit={limit}&wp_token={self.wp_token}").json()

	def get_notifications(
			self,
			fields: str = "feed,nextUrl",
			limit: int = 10,
			direction: int = 0) -> dict:
		return self.session.get(
			f"{self.public_api}/api/v3/users/{self.username}/notifications?return=data&fields={fields}&limit={limit}&direction={direction}&wp_token={self.wp_token}").json()

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
		return self.session.post(
			f"{self.public_api}/apiv2/updateusername?wp_token={self.wp_token}", data=data).json()

	def update_fullname(self, fullname: str) -> dict:
		data = {
			"name": fullname
		}
		return self.session.put(
			f"{self.public_api}/api/v3/users/{self.username}?wp_token={self.wp_token}", data=data).json()

	def update_website(self, url: str) -> dict:
		data = {
			"website": url
		}
		return self.session.put(
			f"{self.public_api}/api/v3/users/{self.username}?wp_token={self.wp_token}", data=data).json()
	
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
		return self.session.post(
			f"{self.public_api}/apiv2/updateuserpassword?wp_token={self.wp_token}", data=data).json()
