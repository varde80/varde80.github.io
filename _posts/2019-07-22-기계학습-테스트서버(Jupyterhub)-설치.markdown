---
layout: post
title:  "기계학습 테스트서버(Jupyterhub) 설치 "
date:   2019-07-22 16:25:00 +0900
categories: AI Jupyterhub
---

## Step 1: The Littlest JupyterHub (TLJH) 설치

1. Terminal을 사용하여 설치하고자 하는 서버에 SSH를 통하여 접속한 후, 아래와 같이 python3, curl, git을 설치한다.

	```	
 	$ sudo apt install python3 git curl
	```

2. 아래의 텍스트를 복사하여 Terminal에 붙인 후 실행한다. 이때 `admin-user-name` 을 JupyterHub에 최초로 사용할 관리자 이름으로 바꾸어 실행한다.

	```
 	curl https://raw.githubusercontent.com/jupyterhub/the-littlest-jupyterhub/master/bootstrap/bootstrap.py | sudo -E python3 - --admin *admin-user-name*
	```

3. Enter 키를 눌러 설치를 시작한다. 설치는 5-10분 정도 소요되며 설치가 완료되면 ‘Done!’이라는 메시지를 보여준다. 

4. 해당서버의 IP 주소를 카피한 후 인터넷 브라우저에 `http://IP주소 (cf. http://123.123.123.123)`와 같이 입력한다. 설치가 성공적으로 끝났다면 다음과 같은 admin page에 접속이 가능해 진다. 

	![JupyterHub log-in page](/assets/admin2.png)

5. 위에서 사용한 관리자 ID를 이용하여 로그인 한다. 이때 비밀 번호의 경우 최초로 입력하는 비밀번호가 향후 사용되어진다. 전체 서버를 관리하기 위한 암호 이므로 강력한 암호를 설정하는 것이 좋다. 

## Step 2: 사용자 추가 

JupyterHub에서 대부분의 administration 과 configuration은 웹 UI를 통해 직접적으로 수행가능하다.

1. JupyterHub 페이지의 우측상단의 `control panel` 버튼을 클릭하여 Control Panel을 실행한다. 

	![Control panel button in notebook](/assets/cpanel.png)

2. `control panel` 페이지에서 좌측상단의 `Admin` 링크를 실행 한다.

	![Admin button in control panel, top left](/assets/adminpage.png)

	JupyterHub admin 페이지에서는 새로운 사용자를 추가하거나 제거 할수 있으며, 각각의 사용자의 서버를 시작하거나 종료할수 있다. .

3. Click the Add Users button.

	![Add Users button in the admin page](/assets/adduser.png)
A Add Users dialog box opens up.

4. Type the names of users you want to add to this JupyterHub in the dialog box, one per line.

	![JupyterHub adduser pages](/assets/users.png)

	Adding users with add users dialog
	You can tick the Admin checkbox if you want to give admin rights to all these users too.

5. Click the Add Users button in the dialog box. Your users are now added to the JupyterHub! When they log in for the first time, they can set their password - and use it to log in again in the future.

	Congratulations, you now have a multi user JupyterHub that you can add arbitrary users to!

## Step 3: 전체 사용자를 위한 conda / pip 패키지 설치 
* JupyterHub에서 전체 사용자에게 공유되는 사용자 환경은 conda 환경이다. 
이 환경 상에서 설치된 라이브러리들은 전체 사용자에게 즉시 사용 가능하게 되며, 이를 위해 관리자는 
`sudo -E` 명령어를 통하여 관련 라이브러리들을 설치 할 수 있다.

	1. 이를 위한 관리자 (admin user)로 JupyterHub에 접속한 뒤 Jupyter Notebook 상에서 Terminal을 실행한다. 

	2. 	Terminal 상에서 `conda-forge`에서 `gdal` 을 설치한다. 
	`sudo -E conda install -c conda-forge gdal`
	
	*The sudo -E is very important!*

	3. 	`pip`를 이용하여 `there`를 설치한다. p
			
	`sudo -E pip install there`
	
	이로써 gdal 과 there 패키지를 JupyterHub 전체사용자가 사용가능하도록 설치하였다. 그러나 현재 python notebook을 사용하고 있는 사용자의 경우 사용중인 notebook의 kernel을 재시작 해야 새로 설치죈 라이브러리가 사용가능해지게 된다. 

## Step 4: HTTPS 설정
* 도메인 등을 설정하여 실질적으로 서버 운영을 하고자 할때는 보안등을 위하여 HTTPS를 설정하는 것이 필요하다. 자세한 사항은 Jupyterhub의 [Enable HTTPS][Enable-HTTPS] 도움말을 참고하자.

## 참고: [Jupyterhub 설치 페이지][Jupyterhub-docs]

 [Jupyterhub-docs]: https://the-littlest-jupyterhub.readthedocs.io/en/latest/install/custom-server.html
 [Enable HTTPS]: https://the-littlest-jupyterhub.readthedocs.io/en/latest/howto/admin/https.html#howto-admin-https

