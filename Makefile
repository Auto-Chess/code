.PHONY: sync ssh \
		run run-h run-server test \
		setup-file setup scan status restart-ip \
		psql-create psql-destroy psql-start psql-stop

# Sync
sync:
	scp {*.py,requirements.txt,Makefile} pi@10.0.0.102:/home/pi/app

# SSH
ssh:
	ssh pi@10.0.0.102

# Run
# -- -- Run
run-h:
	OP_MODE=hardware python3 ./main.py

run:
	python ./main.py

run-server:
	python ./webserver.py

# -- -- Test
test:
	ENVIRONMENT=test python -m unittest discover

# RPI Network Setup
# -- -- Configure dhcpd via config file
setup-file:
	sudo bash -c "echo \"subnet 10.0.0.0 netmask 255.255.255.0 {\n    range 10.0.0.100 10.0.0.120;\n    option routers 10.0.0.1;\n    option domain-name-server 144.118.24.20;\n}\" > /etc/dhcpd.conf"

# -- -- Start internal network
setup:
	sudo bash -c "echo 1 > /proc/sys/net/ipv4/ip_forward"
	sudo iptables -t nat -A POSTROUTING -o wlp58s0 -j MASQUERADE
	sudo iptables -A FORWARD -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
	sudo iptables -A FORWARD -i enp57s0u1 -o wlp58s0 -j ACCEPT
	sudo iptables -I INPUT -p udp --dport 67 -i enp57s0u1 -j ACCEPT
	sudo iptables -I INPUT -p udp --dport 53 -s 10.0.0.0/24 -j ACCEPT
	sudo iptables -I INPUT -p tcp --dport 53 -s 10.0.0.0/24 -j ACCEPT
	sudo ifconfig enp57s0u1 10.0.0.1 netmask 255.255.255.0 up
	sudo systemctl start dhcpd4.service

# -- -- Scan for RPI on internal network
scan:
	nmap -sn 10.0.0.0/24

# -- -- See status of dhcpd service
status:
	sudo systemctl status dhcpd4.service

# -- -- Restart dhcpd service
restart-ip:
	sudo systemctl restart dhcpd4.service

# PostgreSQL dev server
psql-create:
	docker run \
		--name auto-chess-postgres \
		-e POSTGRES_USER=username \
		-e POSTGRES_PASSWORD=password \
		-e POSTGRES_DB=auto-chess \
		-p 5432:5432 \
		--network=host \
		-d \
		postgres
psql-destroy:
	docker rm auto-chess-postgres
psql-start:
	docker start auto-chess-postgres
psql-stop:
	docker stop auto-chess-postgres
