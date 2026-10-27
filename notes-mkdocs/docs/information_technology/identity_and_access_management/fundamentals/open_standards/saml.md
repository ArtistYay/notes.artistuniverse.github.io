---
tags:
  - Cybersecurity
  - Identity & Access Management
---

Ever wondered why when you log into your work laptop and launch Slack or Zoom, you're automatically signed in? A lot of the time that's SAML. It's mostly used in enterprise environments for single sign-on (SSO), and it uses XML as its format.

## The process:

1. Request: You try to access Salesforce. Salesforce sees you aren't logged in.
2. Redirect: Salesforce generates a SAML request (an XML file) and redirects your browser to your company's login page (the IdP, like Microsoft Entra ID or AD FS).
3. Authentication: You enter your username/password (and MFA) on your company's page.
4. The Assertion: The company's IdP verifies you and creates a SAML assertion (an XML document sent from the Identity Provider (IdP) to the Service Provider (SP) that has your authentication, attribute, or authorization info), and digitally signs it.
5. The Hand-off: Your browser POSTs (uploads) this XML document back to Salesforce.
6. Login: Salesforce reads the XML, checks the digital signature, and logs you in.

[Article | Thales Group](https://cpl.thalesgroup.com/access-management/saml-authentication)

[Article | Onelogin](https://www.onelogin.com/learn/saml)

[Article | Okta](https://www.okta.com/identity-101/saml-vs-oauth/)
