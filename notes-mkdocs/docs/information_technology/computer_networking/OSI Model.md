---
tags:
  - Computer Networking
---

![screenshot](../../../images/2B868F66-0305-4372-8AA2-FD1757D55D30.jpeg)

![screenshot](../../../images/Screenshot_2022-09-10_140332.png)

- Layer 1 ~ Physical

    - Layer 1 networks use a shared medium. Hardware can transmit and listen.

    - The layer 1 standard defines how to transmit and receive on the medium: the voltages, the RF details, and so on.

- Layer 2 ~ Data link

    - Adds MAC addresses, so two devices on a local network can talk to each other directly.

    - Also adds control over the media to avoid cross-talk (devices talking over each other), with back-off times and retransmissions.

    - It uses frames.

- Layer 3 ~ Network

    - It allows for unique device-to-device communication over interconnected networks.

    - L3 devices can pass packets over tens or even hundreds of L2 networks. The packets stay mostly unchanged during the trip, they just get wrapped in different L2 frames as they pass over each network.

    - It uses IP addresses to communicate over the internet.

    - Responsible for moving data across various LANs and WANs.

- Layer 4 ~ Transport

    - L4 adds TCP and UDP.

    - TCP is built for reliable transport. It uses segments to make sure data arrives in the right order, adds error checking, and uses ports so a host can have different streams of communication going at once.

    - UDP is all about speed. No handshake and no guaranteed delivery.

    - This layer is how you have multiple conversations to the same IP.

    - Packs up the message and sends it.

- Layer 5 ~ Session

    - Adds the concept of sessions, so that request and reply communication streams are viewed as a single session of communication between client and server.

    - Starts and stops communication between parties.

- Layer 6 ~ Presentation

    - Adds data conversion, encryption, compression, and standards that L7 can use.

    - Formats the application data for delivery and translates it into a common format the network understands.

- Layer 7 ~ Application

    - Where protocols like HTTP, SSH, DNS, and FTP live.

- You can read how it relates to cybersecurity [here](https://douglasbellonrocha.medium.com/defend-from-hackers-using-computer-networking-fundamentals-d80275f37af3).
