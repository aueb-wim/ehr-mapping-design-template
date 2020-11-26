# ehr-mapping-design-template

[![AUEB](https://img.shields.io/badge/AUEB-RC-red.svg)](http://rc.aueb.gr/el/static/home) [![HBP-SP8](https://img.shields.io/badge/HBP-SP8-magenta.svg)](https://www.humanbrainproject.eu/en/follow-hbp/news/category/sp8-medical-informatics-platform/)

This is the successor of the EHR mapping design template for the EHR DataFactory pipeline. Its goal is to simplify the procedures for data curation and harmonization so as to be easily handled by any user without requiring any background on databases and data integration.

## Requirements

- docker (v18)
- docker-compose (v1.22 - v1.8)

Datafactory User must be in the user group “docker”, so the scripts will run without the “sudo” command.
To do that, follow the below instructions:
Add the docker group if it doesn't already exist:

```shell
 sudo groupadd docker
 ```

Add the connected user "$USER" to the docker group. Change the user name to match your preferred user if you do not want to use your current user:

```shell
sudo gpasswd -a $USER docker
```

Either do a newgrp docker or log out/in to activate the changes to groups.
You can use `$ docker run hello-world`  to check if you can run docker without sudo.

