1. What is the highest port number being open less than 10,000?
		8080; I used `nmap -sS -Pn <IP Address>`
		![screenshot](../../../images/Pasted image 20250116105500.png)

2. There is an open port outside the common 1000 ports; it is above 10,000. What is it?
		10021; `nmap -sS -Pn -p- <IP Address>`
		![screenshot](../../../images/Pasted image 20250116105854.png)

3. How many TCP ports are open?
		6
4. What is the flag hidden in the HTTP server header?
		Go to the IP in the browser and use developer tools, in the networking section, you should see it in the filtered headers under server.
		![screenshot](../../../images/Pasted image 20250116110141.png)

5. What is the flag hidden in the SSH server header?
		`ssh -v <username@<ip address>`; `-v` verbose output to get the banner/header information.
6. We have an FTP server listening on a nonstandard port. What is the version of the FTP server?
		vsftpd 3.0.5; used the `-sV` flag, which tells you all the services running on the ports.
7. We learned two usernames using social engineering: `eddie` and `quinn`. What is the flag hidden in one of these two account files and accessible via FTP?
		Shit is so fucking slow but used `hydra -l eddie -P /usr/share/wordlists/rockyou.txt -t 5 10.10.53.3 ftp`
8. Browsing to `http://10.10.53.3:8080` displays a small challenge that will give you a flag once you solve it. What is the flag?
	Used `-sN` flag; `nmap -sN <ip address` to evade the IDS. https://security.stackexchange.com/questions/121900/how-can-the-nmap-tool-be-used-to-evade-a-firewall-ids