Remember how I explained federation is a trust relationship between two IdPs and SPs? That is the what, the how is where OAuth 2.0 comes in.
### OAuth 2.0

Before OAuth 2.0 there was OAuth (OAuth 1), it is an open standard that establishes or implements that trust so users can use eg. a Google account to sign into an application. The user can deny or approve what that application has access to but the user had to sign in with their username and password which would be stored in plaintext in the server side. 

Now, the user does not share their credentials to the server side, the server sends you to Google (redirection) and you sign into your account on the Google side. Once you successfully sign in you are redirected back to the app.

In technical terms:

1. The App (Relying Party) realizes it doesn't know who you are. It constructs a special URL and redirects your browser to Google (The Authorization Server).
2. Google presents its own login screen.
3. Google asks for your consent: "The App 'SuperToDoList' wants to view your email address. Do you agree?"
4. Google does not send the token to your browser immediately (because browsers are somewhat unsafe). Instead, Google generates a temporary, one-time code called an Authorization Code and redirects you back to the App with this code attached to the URL.
5. The App's server sees the code contacts the Google server directly and ask for the ID and access token with the authorization code.
6. You are now logged into the application via your Google account.

[Article | Curity](https://curity.io/resources/learn/oauth-overview/#what-is-oauth-20)

[Article | Aaron Parecki](https://www.oauth.com/oauth2-servers/background/) - This explains how OAuth 2.0 came to be

[Blog Article | Aaron Parecki](https://aaronparecki.com/oauth-2-simplified/) - Explains how to implement the open standard

[Article | Okta](https://www.okta.com/identity-101/saml-vs-oauth/)

!!! youtube "Explain OAuth 2.0 Like A 5 Year Old"
    <iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/hHRFjbGTEOk?si=bCUvGmm3EdEEnhDM" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>