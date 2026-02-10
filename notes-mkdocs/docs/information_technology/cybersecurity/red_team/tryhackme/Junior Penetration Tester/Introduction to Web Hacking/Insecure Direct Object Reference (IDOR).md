### **I. What is an IDOR?**

- Vulnerability where an attacker can access objects directly by manipulating a reference.
- _Example:_ Changing `user_id=1000` to `user_id=100` in `http://online-service.thm/profile?user_id=1000`.
### **II. Finding IDORs in Different ID Formats:**

- **Encoded IDs (e.g., Base64):**
    1. Decode the ID (Base64).
    2. Change the value.
    3. Encode the new value.
    4. Use the new encoded ID in the request.
    ![screenshot](../../../images/Pasted image 20241109150946.png)
- **Hashed IDs:**
    - More complex.
    - Check for predictable patterns (e.g., hashed integer values).
    - Use online hash cracking services (e.g., CrackStation).
- **Unpredictable IDs:**
    1. Create two accounts.
    2. Swap IDs between the accounts.
    3. If you can view the other user's content, it's an IDOR.
### **III. IDOR Locations:**

- **Not just in the address bar:** Check AJAX requests, JavaScript files.
- **Unreferenced Parameters (Parameter Mining):** Discover hidden parameters that might be vulnerable. _Example:_ `/user/details` vs. `/user/details?user_id=123`.
- **API Endpoints:** Look for IDs in API calls. _Example:_ `/api/v1/customer?id=`.
### **IV. General IDOR Testing Strategy:**

1. **Identify potential endpoints:** Look for URLs or API calls that take IDs as parameters.
2. **Understand ID format:** Decode, analyze hashes, or test with multiple accounts.
3. **Modify IDs:** Try different values, especially those of other users.
4. **Observe the response:** Check if you can access unauthorized data.
5. **Document findings:** Record the vulnerable endpoint and the ID manipulation method.