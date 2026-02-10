
![screenshot](../../../images/2B868F66-0305-4372-8AA2-FD1757D55D30.jpeg)

![screenshot](../../../images/Screenshot_2022-09-10_140332.png)

- Layer 1 ~ Physical
    
    - Layer 1 networks use a shared medium. Hardware can transmit and listen.
    
    - Layer 1 standard agrees how to transmit and receive the medium, the voltages, and the RF details
    
- Layer 2 ~ Data link
    
    - Add MAC Addresses which can be used for named communication between two devices on a local network.
    
    - Also adds controls over the media, avoiding cross-talk, this allows a back-off time and retransmissions
    
    - It uses frames
    
- Layer 3 ~ Network
    
    - It allows for unique device-to-device communication over interconnected networks.
    
    - L3 devices can pass packets over tens or even hundreds of L2 networks. The packets remain largely unchanged during this journey - traveling within different L2 frames as they pass over various networks.
    
    - It uses IP addresses to communicate over the internet.
    
    - Responsible for moving data across various LANs and WANs.
    
- Layer 4 ~ Transport
    
    - L4 adds TCP and UDP.
    
    - TCP is designed for reliable transport, it uses segments to ensure data is received in the correct order and adds error checking and ports allowing different streams of communications to the same host.
    
    - UDP is aimed at speed.
    
    - This layer is how you have multiple conversations to the same IP.
    
    - Packs up the message and sends it.
    
- Layer 5 ~ Session
    
    - Adds the concept of sessions, so that request and reply communication streams are viewed as a single session of communication between client and server.
    
    - Starts and stops communication between parties.
    
- Layer 6 ~ Presentation
    
    - Adds data conversion, encryption, compression, and standards that L7 can use.
    
    - Application data is formatted for delivery. Translated into a common network language.
    
- Layer 7 ~ Application
    
    - Is where protocols such as HTTP, SSH, and FTP are added.
    
- You can read how It relates to cybersecurity [here](https://douglasbellonrocha.medium.com/defend-from-hackers-using-computer-networking-fundamentals-d80275f37af3).