---
layout: post
title:  "linux server setting for Linode "
date:   2019-11-16 20:25:00 +0900
categories: Linode Linux
---

참고자료 [Corey Schafer's Youtube][corey]

# Step 1: ssh setting

## Terminal을 사용하여 설치하고자 하는 서버에 SSH를 통하여 접속

 	$ ssh root@139.162.68.100
	$ apt-get update && apt-get upgrade
	$ hostnamectl set-hostname mdcs-server
	$ hostname

## server에 host 파일 설정
	$ nano /etc/hosts 

* 139.162.68.100 mdcs-server 추가

## server에 user 이름 추가
	$ adduser varde

## server에 user sudo 권한 추가
	```
	$ adduser varde sudo 
	```

## server에 user 이름으로 재접속
	```
 	$ ssh varde@139.162.68.100
	```

## server에 ssh 키저장을 위한 폴더 만들기
	```
	$ mkdir -p ~/.ssh
	```

## local에서 key 만들기
	```
	$ ssh-keygen -b 4096
	$ scp ~/.ssh/id_rsa.pub varde@139.162.68.100:~/.ssh/authorized_keys
	```
## server에 key 파일권한 수정
	```
	$ sudo chmod 700 ~/.ssh
	$ sudo chmod 600 ~/.ssh*
	```

## server root 로그인 제한을 위한 수정

	$ sudo nano /etc/ssh/sshd_config

  * PermitRootLogin no로 수정
  * PasswordAuthentucation No 수정
	
# ssh 재시작	

	$ sudo systemctl restart sshd

# Step 2: UFW 기반 방화벽 설정


	$ sudo apt-get install ufw
	$ sudo ufw default allow outgoing
	$ sudo ufw default deny incoming
	$ sudo ufw allow ssh
	$ sudo ufw allow 8000
	$ sudo ufw enable
	$ sudo ufw status

# Step 2: pyenv 설치

## Pyenv용 기본 패키지 설치

	$ sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl git

	$ curl https://pyenv.run | bash
	$ exec $SHELL
	$ pyenv update

[corey]: https://www.youtube.com/watch?v=Sa_kQheCnds
