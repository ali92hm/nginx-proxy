#Node Nginx Proxy

Makes Nginx proxy configuration files. This script automatically generates Nginx configuration files that can act as proxy for node applications.

##Usage

###Install

You only need to clone this repository on your remote machine.
``` bash
git clone https://github.com/SirenLLC/node-nginx-proxy.git
```

###Execution
This application needs sudo permissions because the default Nginx configuration is under `/etc/nginx/` which requires sudo permissions to be changed.
```bash
sudo python nginx-config.py [node-app-name]
```
You will be prompted with several questions for your configuration scripts such as servers ip addresses, ports, and weight.
You can also redirect non-www requests to www.

You can change the default location of the Nginx configuration by passing the following optional parameter.
```bash
sudo python nginx-config.py [node-app-name] -nginx-config-path [path-to-nginx-config]
```



##Dependencies
* [Python2.7](https://www.python.org/download/releases/2.7/)
* [Nginx](http://nginx.org/en/download.html)

##Structure
	node-nginx-proxy
	├── LICENSE-MIT
	├── README.md
	└── lib
		└── nginx-proxy.py		- Generator script

##[Potential Bugs](https://github.com/SirenLLC/node-nginx-proxy/issues)
* This script will not work under the Windows operating system.
* SSL configuration is not tested.

##To do
* Add SSL redirection
* Make an npm module and put on npm

##License
[MIT license](http://opensource.org/licenses/MIT)
