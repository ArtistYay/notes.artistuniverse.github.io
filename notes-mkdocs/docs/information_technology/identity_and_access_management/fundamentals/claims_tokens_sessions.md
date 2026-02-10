### Claims

Users attributes or data about the user like email address, full name etc. The asserting party (IdP) tells the API (eg. Microsoft Graph, Intune) about your (subject) claims (attributes) and what your authorized to do.

They are embedded in tokens and only accepted if the asserting party is trusted.

[Documentation | Curity](https://curity.io/resources/learn/what-are-claims-and-how-they-are-used/)
### Tokens

They are basically a pass to enter club so you don't hate outside of it (a little joke) you can use that same token for different types of clubs as well. In technical terms it is a secure device that allows access to protected resources.

They are different types of authentication tokens:

#### Session

This token is a authenticate one and done. The server sends you a unique ID that is stored in your browser cookies and stores it in it's memory to remember that it is your token, every time you do something that same token is used to prove (non-repudiation) is you.

![screenshot](../../../images/session_token.png)

[Documentation | Wikipedia](https://en.wikipedia.org/wiki/Session_ID)
#### JWT

This is a common token used in IT but it's basically a session token but the only difference is that instead of the server giving it a unique identifier and storing the unique identifier, the token is digitally signed (integrity) so if show this JWT token to any resource or server in your environment it's automatically trusted and that server doesn't need to hit up another server to see if you are legit.

It also holds you claims (attributes).

![screenshot](../../../images/jwt_token.png)

[Documentation | Wikipedia](https://en.wikipedia.org/wiki/JSON_Web_Token)
##### These tokens can be used together:
###### Access

It's a temporary key that gives you access for certain applications, so for example in that token you may have an hour of access to that service. It also proves what you can do, so the token carries the permissions you have in that application. It answers the question '_what is the user allowed to do?_'

![screenshot](../../../images/access_token.png)

[Documentation | Wikipedia](https://en.wikipedia.org/wiki/Access_token)

[Documentation | Auth0](https://auth0.com/docs/secure/tokens/access-tokens)
###### ID

A badge you walk around with that answers the question '_who is this person?_'. An application can read this token and greets you by your name.

![screenshot](../../../images/id_token.png)

[Documentation | Auth0](https://auth0.com/docs/secure/tokens/id-tokens)
###### Refresh

Lastly we have refresh tokens which is pretty straight forward. When an access token expires the refresh token is your renewal voucher that says 'hey, this guy is trusted please send them another access token' it's there to make sure you don't have to go through the whole authentication process again.

[Documentation | Auth0](https://auth0.com/docs/secure/tokens/refresh-tokens)

[Blog Article | Medium](https://medium.com/@sweetondonie/5-types-of-authentication-tokens-every-beginner-should-know-5073ca9b2319) - To learn about the five types of authentication tokens.

[Documentation | Geeks for Geeks](https://www.geeksforgeeks.org/computer-networks/session-vs-token-based-authentication/) - To learn the difference between a session and a token based authentication