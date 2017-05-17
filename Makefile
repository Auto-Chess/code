.PHONY: setup-file setup scan status
setup-file:
	sudo bash -c "echo \"subnet 10.0.0.0 netmask 255.255.255.0 {\n    range 10.0.0.100 10.0.0.120;\n    option routers 10.0.0.1;\n    option domain-name-server 144.118.24.20;\n}\" > /etc/dhcpd.conf"

setup:
	sudo bash -c "echo 1 > /proc/sys/net/ipv4/ip_forward"
	sudo iptables -t nat -A POSTROUTING -o wlp58s0 -j MASQUERADE
	sudo ifconfig enp57s0u1 10.0.0.1 netmask 255.255.255.0 up
	sudo systemctl start dhcpd4.service

scan:
	nmap -sn 10.0.0.0/24

status:
	sudo systemctl status dhcpd4.service

restart-ip:
	sudo systemctl restart dhcpd4.service
