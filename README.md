#Node NginX Proxy

Makes NginX proxy configuration files. This script automatically generates NginX configuration files that can act as proxy for node applications.

##Usage
This application needs sudo permissions because the default NginX configuration is under `/etc/nginx/` which requires sudo permissions to be changed.
```bash
sudo python nginx-config.py [node-app-name]
```
You will be prompted with several questions for your configuration scripts such as servers ip addresses, ports, and weight.
You can also redirect non-www requests to www.

You can change the default location of the NginX configuration by passing the following optional parameter.
```bash
sudo python nginx-config.py [node-app-name] -nginx-config-path [path-to-nginx config]
```



##Dependencies
* Python2.7

##Structure
    thing
    ├── nginx-config.py         - Configuration script

##Potential Bugs:
* This script will not work under the Windows operating system.
* SSL configuration is not tested.

##To do
* Add SSL redirection
* Make an npm module and put on npm

##License
[MIT license](http://opensource.org/licenses/MIT)