### SAML

Ever wondered whenever you log into your work laptop and launch Slack or even Zoom you are automatically signed? Well that's SAML, it's mostly used for enterprise environments for single sign on (SSL). It uses XML as it's format.

###### The process:

1. Request: You try to access Salesforce. Salesforce sees you aren't logged in.
2. Redirect: Salesforce generates a SAML Request (an XML file) and redirects your browser to your Company's Login Page (the IdP, eg. Active Directory).
3. Authentication: You enter your username/password on your Company Page.
4. The Assertion: The Company Server verifies you and creates a SAML Assertion (a XML document sent from an Identity Provider (IdP) to a Service Provider (SP) that contains user authentication, attribute, or authorization information.
5. The Hand-off: Your browser POSTs (uploads) this XML document back to Salesforce.
6. Login: Salesforce reads the XML, checks the digital signature, and logs you in.

![screenshot](saml.png)

[Article | Thales Group](https://cpl.thalesgroup.com/access-management/saml-authentication)

[Article | Onelogin](https://www.onelogin.com/learn/saml)

[Article | Okta](https://www.okta.com/identity-101/saml-vs-oauth/)