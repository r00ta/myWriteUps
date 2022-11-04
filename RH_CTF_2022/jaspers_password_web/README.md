# Jasper's password

Looking at the page source I saw there was an api endpoint `https://edisonmsg.ctf.nofizz.buzz/api`. 

INSERT IMAGE HERE

which returns the following json 

```json
{
	"_links": {
		"accesstokens": {
			"title": "Authentication",
			"href": "http://edisonmsg.ctf.nofizz.buzz/api/accesstokens"
		},
		"me": {
			"title": "Current user",
			"href": "http://edisonmsg.ctf.nofizz.buzz/api/me"
		},
		"messages": {
			"title": "Messaging",
			"href": "http://edisonmsg.ctf.nofizz.buzz/api/messages"
		},
		"self": {
			"href": "http://edisonmsg.ctf.nofizz.buzz/api"
		},
		"users": {
			"title": "User list",
			"href": "http://edisonmsg.ctf.nofizz.buzz/api/users"
		}
	}
}
```

Visiting `http://edisonmsg.ctf.nofizz.buzz/api/users` I've got the first flag 

```json
{
	"_links": {
		"self": {
			"href": "http://edisonmsg.ctf.nofizz.buzz/api/users"
		},
		"up": {
			"href": "http://edisonmsg.ctf.nofizz.buzz/api"
		}
	},
	"users": [
		{
			"id": 0,
			"name": "Chêne Odeur",
			"username": "odeur",
			"password_sha256": null,
			"password_md5": null,
			"password": null,
			"password_hint": null
		},
		{
			"id": 1,
			"name": "Alfred Majordomo",
			"username": "alfred",
			"password_sha256": "00e4611023340a00f0fa0e4f57163d520bfc34e3fd838ee48b208645e38e02d6",
			"password_md5": null,
			"password": null,
			"password_hint": null
		},
		{
			"id": 2,
			"name": "Petit Boulot",
			"username": "boulot",
			"password_sha256": null,
			"password_md5": "54450d24c6cfbf80a25c6c5b0b6be492",
			"password": null,
			"password_hint": "RH_CTF{}"
		},
		{
			"id": 3,
			"name": "Horace Jasper",
			"username": "jasper",
			"password_sha256": null,
			"password_md5": null,
			"password": "RH_CTF{dalmatians}",
			"password_hint": null
		}
	]
}
```


```text
RH_CTF{dalmatians}
```
