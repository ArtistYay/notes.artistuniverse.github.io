### What is Repeater?

- Allows modifying and resending intercepted requests to a target.
- Manipulates captured requests (from Proxy) or creates new ones from scratch (like cURL).
### Inspector

- Used in both Proxy and Repeater modules.
- Provides a more intuitive way to analyze and modify requests compared to the raw editor.
- **Modifiable Sections:**
    - **Request Attributes:** Location, method, protocol. _Examples:_ Change resource, switch HTTP method (GET to POST), change protocol (HTTP/1 to HTTP/2).
    - **Request Query Parameters:** Data sent in the URL (GET requests). _Example:_ `https://example.com/?param1=value1`.
    - **Request Body Parameters:** Data sent in POST requests.
    - **Request Cookies:** List of cookies sent with the request.
    - **Request Headers:** View, access, modify (add/remove) headers. Useful for testing server response to unexpected headers.
- **Non-Modifiable Section:**
    - **Response Headers:** Headers returned by the server. Only visible after sending a request.