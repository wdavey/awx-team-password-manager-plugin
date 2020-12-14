# AWX Team Password Manager Plugin
---

This is a fork from the example plugin: https://github.com/ansible/awx-custom-credential-plugin-example.git

This plugin provides access to the Team Password Manager API (currently v4) as a credential provider for AWX/Tower.


## Installation
In version 15.0.1 of AWX, installation steps are:
1. On *all* AWX nodes, install the plugin into the awx virtualenv, this is done from the machine AWX is installed:

```shell
docker exec awx_web /var/lib/awx/venv/awx/bin/pip3 install git+https://github.com/wdavey/awx-team-password-manager-plugin.git
docker exec awx_task /var/lib/awx/venv/awx/bin/pip3 install git+https://github.com/wdavey/awx-team-password-manager-plugin.git
```

2. From *any* of the AWX nodes run the *setup managed credential types* command, this is done from the machine AWX is installed:

```shell
docker exec awx_web awx-manage setup_managed_credential_types
```

3. Restart AWX containers, this is done from where the AWX ansible play is run:

```shell
ansible -i inventory -m docker_compose -a "project_src=<docker_compose_dir in inventory> restarted='yes'" <awx hostname>
```
Example:
```shell
ansible -i inventory -m docker_compose -a "project_src=/data/awx/awxcompose restarted='yes'" awx-server
```

## Usage

* See [Credentials](https://docs.ansible.com/ansible-tower/latest/html/userguide/credentials.html) for a general overview of credentials in AWX/Tower

* See [Show a password](https://teampasswordmanager.com/docs/api-passwords/#show_password) for details on what information this plugin provides

This plugin requires 5 inputs, 3 of which are global to the credential type.

### Global Properties

* Server URL: URL to the index.php of your Team Password Manager instance. Must include a trailing backslash

* Private Key: The private API key for the user that has access to the information stored in Team Password Manager

* Public Key: The public API key for the user that has access to the information stored in Team Password Manager

### User Properties

* Password ID: The ID of the password record in Team Password Manager

* Field Name: The name of the field (lowercase and underscore for spaces) as it's recorded in Team Password Manager on the password record

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/wdavey/awx-team-password-manager-plugin). 

## Authors

* **William Davey** - *Forked Work* - [wdavey](https://github.com/wdavey)