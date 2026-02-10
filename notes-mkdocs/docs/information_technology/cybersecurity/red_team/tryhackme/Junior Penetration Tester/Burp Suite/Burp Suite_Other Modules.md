### Decoder

- **Purpose:** Data manipulation.
- Encodes and decodes data.
- Creates hashsums.
- **Smart Decode:** Recursively decodes data until plaintext is reached.
- **Encoding/Decoding Options:**
    - **Plain:** Raw text.
    - **URL:** Encodes characters for safe URL transmission (`%` followed by hexadecimal). _Example:_ `/` becomes `%2F`.
    - **HTML:** Replaces special characters with HTML entities (`&` followed by hexadecimal or character reference, ending with `;`). Prevents XSS.
    - **Base64:** Encodes data into ASCII-compatible format.
    - **ASCII Hex:** Converts between ASCII and hexadecimal representations. _Example:_ "ASCII" becomes "4153434949".
    - **Hex, Octal, Binary:** Converts between number systems.
    - **Gzip:** Compresses data. Often not valid ASCII/Unicode.
- **Stacking:** Encoding methods can be combined (e.g., ASCII Hex then Octal).
- **Hex View:** Allows byte-by-byte input editing.
- **Hashing:** Algorithm output is typically converted to a hexadecimal string ("hash").
### Comparer

- **Purpose:** Compares two pieces of data (ASCII or bytes).
- Displays compared data in text or hex format.
- **Comparison Key:** Shows modified, deleted, and added data.
- **Sync Views:** Keeps both data sets in the same format (text or hex).
### Sequencer

- **Purpose:** Evaluates the randomness (entropy) of tokens (e.g., session cookies, CSRF tokens).
- **Methods:**
    1. **Live Capture:** Sends a request that generates a token to Sequencer, then automatically repeats the request thousands of times, storing tokens for analysis.
    2. **Manual Load:** Loads a list of pre-generated tokens.
- **Auto Analyze:** Periodically performs entropy analysis during live capture.
- **Analysis Report:**
    - **Overall Result:** Broad assessment of token security.
    - **Effective Entropy:** Measures token randomness (higher is better).
    - **Reliability:** Confidence level in the results.
    - **Sample:** Details about the analyzed tokens.
### Organizer

- **Purpose:** Stores and annotates HTTP requests for later review.
- Creates read-only copies of requests.
- Useful for organizing penetration testing workflow.