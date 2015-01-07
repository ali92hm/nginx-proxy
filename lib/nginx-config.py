"""
Author: Ali Hajimirza (ali@alihm.net)
With help of: http://stackoverflow.com/questions/5009324/node-js-nginx-and-now
"""

#!/usr/bin/env python
import sys
import os
import argparse

upstream_template = """#Node server instances
upstream {app_name} {{
{servers}
	keepalive 8;
}}\n
"""

redirect_template = """# {comment}
server {{
	listen       {port};
	server_name  {redirect_from};
	return       301 {protocol}://{redirect_to}$request_uri;
}}\n
"""

nginx_node_server_template = """#The NginX server instance
server {{
	listen {port};
	server_name {domain};
	access_log /var/log/nginx/{app_name}.log;

	location / {{
		#Socket proxy upgrade
		proxy_http_version 1.1;
		proxy_set_header Upgrade $http_upgrade;
		proxy_set_header Connection "upgrade";

		proxy_set_header X-Real-IP $remote_addr;
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
		proxy_set_header Host $http_host;
		proxy_set_header X-NginX-Proxy true;

		proxy_pass {protocol}://{app_name}/;
		proxy_redirect off;
	}}
}}\n"""

nginx_static_server_template = """#The NginX server instance
server {{
	listen {port};
	server_name {domain};
	access_log /var/log/nginx/{app_name}.log;

	location / {{
		root {path};
		error_page 404 /404.html;
		location = /404.html {{
			internal;
		}}
	}}
}}\n"""

 

parser = argparse.ArgumentParser(description='Makes nginx configuration file for node applications.')
parser.add_argument('app_name', type=None, help='Name of your Application')
parser.add_argument('-config-path', type=None, default='/etc/nginx/', help='Path to the nginx')
args = parser.parse_args()

config_file_path = os.path.join(args.config_path, 'sites-available', args.app_name) 

with open(config_file_path,'wb') as config_file:
	try:
		# Creating the server section
		domain_name = raw_input('Enter name of your domain without www (Example example.com) ')
		use_www_proxy = raw_input('Do you want to redirect {domain_name} to www.{domain_name}? [y/n] '.format(domain_name = domain_name)).lower() == 'y'
		# use_https = raw_input('Do you want to redirect HTTP requests to HTTPS? (y/n) '.format(domain_name)).strip().lower() == 'y'
		use_https = False #Implement in the future

		# Handling redirects
		if use_www_proxy:
			base_name = domain_name            
			domain_name = 'www.'+domain_name
			if use_https:
				# Redirect HTTP www to HTTPS www
				config_file.write(redirect_template.format(
					comment='Redirect HTTP www to HTTPS www',
					port='80',
					redirect_from=domain_name,
					redirect_to=domain_name,
					protocol='https'))

				# Redirect HTTP non-www to HTTPS www
				config_file.write(redirect_template.format(
					comment='Redirect HTTP non-www to HTTPS www',
					port='80',
					redirect_from=base_name,
					redirect_to=domain_name,
					protocol='https'))

				# Redirect HTTPS non-www to HTTPS www
				config_file.write(redirect_template.format(
					comment='Redirect HTTPS non-www to HTTPS www',
					port='443 ssl',
					redirect_from=base_name,
					redirect_to=domain_name,
					protocol='https'))
				
			else:
				# Redirect non www to www
				config_file.write(redirect_template.format(
					comment='Redirect non www to www',
					port='80',
					redirect_from=base_name,
					redirect_to=domain_name,
					protocol='http'))

		protocol = 'http'
		port = '80'
		if use_https:
			protocol = 'https'
			port = '443 ssl'
			# Still need to redirect HTTP to HTTPS
			if not use_www_proxy:
				config_file.write(redirect_template.format(
					comment='Redirect HTTP to HTTPS', 
					port='80',
					redirect_from=domain_name,
					redirect_to=domain_name,
					protocol='https'))

		# Static web hosting
		if raw_input('Is this a static application? [y/n] ').lower() == 'y':
			serve_path = raw_input('Enter the path for your static files: ')
			config_file.write(nginx_static_server_template.format(port=port, domain=domain_name, app_name=args.app_name, path=os.path.abspath(serve_path)))
		# Proxy configuration
		else:
			# Creating the upstream section
			sys.stdout.write('Enter sever address one by one.\n')
			server_list = list()
			while (True):
				address = raw_input('Enter the address of the machine running the server (Default 127.0.0.1) ').strip()
				if address == '':
					address = '127.0.0.1'
				app_port = raw_input('Enter the port that this server is running on (Example 3000) ').strip()
				weight = raw_input('Enter weight of this server (Default 1) ').strip()
				if weight == '':
					server_list.append('\tserver {}:{};'.format(address, app_port))
				else:
					server_list.append('\tserver {}:{} weight={};'.format(address, app_port, weight))
				if 'n' == raw_input('Would you like to add more servers? [y/n] ').strip().lower():
					break
			config_file.write(upstream_template.format(app_name=args.app_name, servers='\n'.join(server_list)))
			config_file.write(nginx_node_server_template.format(port=port, domain=domain_name, app_name=args.app_name, protocol=protocol))

	except KeyboardInterrupt:
		sys.stdout.write('\nTerminating...\n')
		sys.exit(-1)

# Creating a symbolic link from configuration in sites-available to sites-enabled
alias_path = os.path.join(args.config_path, 'sites-enabled', args.app_name)
if not os.path.isfile(alias_path):
	os.system('sudo ln -s {} {}'.format(config_file_path, alias_path))
# Restarting NginX server
os.system('sudo /etc/init.d/nginx restart')
sys.stdout.write('Successfully configured nginx for {}\n'.format(args.app_name))
