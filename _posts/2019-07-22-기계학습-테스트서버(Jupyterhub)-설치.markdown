

# Step 1: Installing The Littlest JupyterHub

* Terminal을 사용하여 설치하고자 하는 서버에 SSH를 통하여 접속한 후, 아래와 같이 opython3, curl, git을 설치한다.

	$ sudo apt install python3 git curl
Copy to clipboard
Copy the text below, and paste it into the terminal. Replace <admin-user-name> with the name of the first admin user for this JupyterHub. Choose any name you like (don’t forget to remove the brackets!). This admin user can log in after the JupyterHub is set up, and can configure it to their needs. Remember to add your username!
```
curl https://raw.githubusercontent.com/jupyterhub/the-littlest-jupyterhub/master/bootstrap/bootstrap.py | sudo -E python3 - --admin <admin-user-name>
```
Copy to clipboard
Note
See What does the installer do? if you want to understand exactly what the installer is doing. Customizing the Installer documents other options that can be passed to the installer.

Press Enter to start the installation process. This will take 5-10 minutes, and will say ‘Done!’ when the installation process is complete.

Copy the Public IP of your server, and try accessing http://<public-ip> from your browser. If everything went well, this should give you a JupyterHub login page.

JupyterHub log-in page
Login using the admin user name you used in step 2. You can choose any password that you wish. Use a strong password & note it down somewhere, since this will be the password for the admin user account from now on.

Congratulations, you have a running working JupyterHub!

#Step 2: Adding more users
Most administration & configuration of the JupyterHub can be done from the web UI directly. Let’s add a few users who can log in!

Open the Control Panel by clicking the control panel button on the top right of your JupyterHub.

Control panel button in notebook, top right
In the control panel, open the Admin link in the top left.

Admin button in control panel, top left
This opens up the JupyterHub admin page, where you can add / delete users, start / stop peoples’ servers and see who is online.

Click the Add Users button.

Add Users button in the admin page
A Add Users dialog box opens up.

Type the names of users you want to add to this JupyterHub in the dialog box, one per line.

Adding users with add users dialog
You can tick the Admin checkbox if you want to give admin rights to all these users too.

Click the Add Users button in the dialog box. Your users are now added to the JupyterHub! When they log in for the first time, they can set their password - and use it to log in again in the future.

Congratulations, you now have a multi user JupyterHub that you can add arbitrary users to!

#Step 3: Install conda / pip packages for all users
The User Environment is a conda environment that is shared by all users in the JupyterHub. Libraries installed in this environment are immediately available to all users. Admin users can install packages in this environment with sudo -E.

Log in as an admin user and open a Terminal in your Jupyter Notebook.

New Terminal button under New menu
Install gdal from conda-forge.

sudo -E conda install -c conda-forge gdal
Copy to clipboard
The sudo -E is very important!

Install there with pip
			
sudo -E pip install there
Copy to clipboard
The packages gdal and there are now available to all users in JupyterHub. If a user already had a python notebook running, they have to restart their notebook’s kernel to make the new libraries available.

See Install conda, pip or apt packages for more information.

# Step 4: Setup HTTPS
Once you are ready to run your server for real, and have a domain, it’s a good idea to proceed directly to Enable HTTPS.

 

