---
tags:
  - Cybersecurity
  - Offensive Security
---

## What is Intruder?

- Burp Suite's built-in fuzzing tool.
- Automates request modification and repetitive testing with varied inputs.
- Uses captured requests (often from the Proxy module).
- Sends multiple requests with slightly altered values based on user-defined configurations.
- Use Cases:
    - Brute-forcing login forms (username/password wordlists).
    - Fuzzing attacks (subdirectories, endpoints, virtual hosts).
- Similar Tools: Wfuzz, ffuf (command-line).
- Burp Community Edition limitation: Intruder is throttled, so it's way slower than Burp Professional. That's why a lot of people switch to other fuzzing tools.

## Intruder Sub-tabs:

- Positions:
    - Selects the attack type.
    - Configures where payloads are inserted in the request template.
- Payloads:
    - Selects values to insert into defined positions.
    - Various payload options (e.g., wordlists).
    - Modifies Intruder's payload behavior (pre-processing rules, prefixes, suffixes, match/replace, regex skipping).
- Resource Pool (Burp Professional Only):
    - Resource allocation among automated tasks.
    - Limited use in Community Edition.
- Settings:
    - Configures attack behavior.
    - Handles results and the attack itself.
    - Flags requests with specific text.
    - Defines response to redirects (3xx).

## Key Concepts:

- Fuzzing: Testing functionality/existence by applying various data to a parameter. _Example:_ Fuzzing endpoints by appending words from a wordlist to a URL. (e.g., http://10.10.71.26/WORD_GOES_HERE)
- Add §: Manually define positions by highlighting them in the request editor.
- Clear §: Remove all defined positions.
- Auto §: Automatically identify likely positions (helpful to restore default positions).

## Attack Types:

- Sniper:
    - Default and most common.
    - Cycles through payloads, inserting one at a time into each position.
    - Precise and focused testing.
    - `requests = numberOfWords * numberOfPositions`
- Battering Ram:
    - Uses one payload set and puts the *same* payload into *every* position at once.
    - Useful when the same value has to show up in more than one place in the request (like a username that appears in two fields).
    - `requests = numberOfWords`

    ![screenshot](../../../images/Pasted image 20250103135951.png)

- Pitchfork:
    - Tests multiple positions with _different_ payloads _simultaneously_.
    - Multiple payload sets (one per position).
    - Iterates through all sets simultaneously.
    - Stops when the _shortest_ payload list is exhausted. Payload lists ideally should be the same length.

    ![screenshot](../../../images/Pasted image 20250103140300.png)

- Cluster Bomb:
    - Uses a separate payload set for each position, like Pitchfork.
    - But instead of pairing them up line by line, it tries _every possible combination_ of payloads across all the sets.
    - `requests = product of the number of lines in each payload set`
    - Generates a large amount of traffic.
    - Useful for credential brute-forcing (unknown username/password mapping).
    - Can be very slow in Burp Community Edition.

    ![screenshot](../../../images/Pasted image 20250103140658.png)
