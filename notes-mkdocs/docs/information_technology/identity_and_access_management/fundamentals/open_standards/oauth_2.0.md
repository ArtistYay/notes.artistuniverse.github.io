---
tags:
  - Cybersecurity
  - Identity & Access Management
---

Remember how I explained federation is a trust relationship between IdPs and SPs? That's the what. A big part of the how is OAuth 2.0. (OAuth itself is about authorization, what an app is allowed to do for you. The login part is OpenID Connect, which sits on top of it.)

Before OAuth existed, if an app wanted to read your Gmail contacts, it literally asked for your Google username and password and stored them on its server. That's a nightmare. OAuth 1.0 fixed that so the user approves or denies what the app can access without ever handing over their password, but it was complicated to implement because every request had to be cryptographically signed. OAuth 2.0 made it simpler.

Now, the user doesn't share their credentials with the app. The app sends you to Google (a redirect), you sign into your account on Google's side, and once you successfully sign in you get redirected back to the app.

In technical terms:

1. The App (Relying Party) realizes it doesn't know who you are. It constructs a special URL and redirects your browser to Google (The Authorization Server).
2. Google presents its own login screen.
3. Google asks for your consent: "The App 'SuperToDoList' wants to view your email address. Do you agree?"
4. Google does not send the token to your browser immediately (because browsers are somewhat unsafe). Instead, Google generates a temporary, one-time code called an Authorization Code and redirects you back to the App with this code attached to the URL.
5. The App's server sees the code, contacts Google's server directly, and trades the authorization code for an access token (and an ID token, if it's using OpenID Connect). Modern apps also use PKCE here, which proves the app trading in the code is the same one that started the login, so a stolen code is useless.
6. You are now logged into the application via your Google account.

[Article | Curity](https://curity.io/resources/learn/oauth-overview/#what-is-oauth-20)

[Article | Aaron Parecki](https://www.oauth.com/oauth2-servers/background/) - This explains how OAuth 2.0 came to be

[Blog Article | Aaron Parecki](https://aaronparecki.com/oauth-2-simplified/) - Explains how to implement the open standard

[Article | Okta](https://www.okta.com/identity-101/saml-vs-oauth/)

!!! youtube "Explain OAuth 2.0 Like A 5 Year Old"
    <iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/hHRFjbGTEOk?si=bCUvGmm3EdEEnhDM" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
