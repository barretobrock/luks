# luks
Local key service

## Installation
### Prerequisites
 - [py-package-manager]() installed
 - bash, not dash
   - (`sudo dpkg-reconfigure dash`, `No`)
 - `luks` virtual env in the `~/venvs/` directory
### Package
```bash
# Install package and deps
sh update_script.sh
```
### nginx, etc.
```bash
# Install nginx, gunicorn
sudo apt install nginx gunicorn
# Enable ufw
sudo ufw enable
# Add HTTP
sudo ufw allow 'Nginx HTTP' # Also OpenSSH
# Check status of nginx service
sudo systemctl status nginx
```
Now, check that the URL loads: `http://{ip}`

```bash
# Add app to nginx
sudo nano /etc/nginx/sites-available/luks
# Once done, link to sites-enabled
sudo ln -s /etc/nginx/sites-available/luks /etc/nginx/sites-enabled
# Test changes
sudo nginx -t
# If successful, restart nginx to read new config
sudo systemctl restart nginx
```

## Troubleshooting
These might help with debugging `nginx` stuff
```bash
# Check nginx error logs
sudo less /var/log/nginx/error.log
# Check nginx access logs
sudo less /var/log/nginx/access.log
# Check nginx process logs
sudo journalctl -u nginx
# Check app's uWSGI logs
sudo journalctl -u luks
```

## Resources
 - [Installing nginx for ubuntu 20.04](https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-20-04)
 - [Nginx guide](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04)
