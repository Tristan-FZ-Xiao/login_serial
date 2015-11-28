# We want to login our router first.

import urllib, urllib2, cookielib, re, time
import json
import time

# Time out == 5s

class login:
	def __init(self):
		urllib2.socket.setdefaulttimeout(5)

	# Description:	Get html context from URL with POST method
	def post(self, url, data, referer):
		req = urllib2.Request(url)
		data = urllib.urlencode(data)
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())

		if referer is not None:
			req.add_header('Referer', referer)
		try:
			response = opener.open(req, data)
		except:
			print "post open URL Error " + url
			return None
		return response.headers['Set-Cookie']

	def login_server(self, url, user_name, password, referer, count):
		data = {
			'username' : user_name,
			'password' : password,
		}
		for i in range(count):
			ret = self.post(url, data, referer)
			if None == ret:
				continue
			else:
				return ret
		return None

	# Description:	Get html context from URL
	# Input:	count: retry times
	#		cookie: use to login
	# Output:	return buf of html context
	def get_html4(self, url, referer, cookie, count):
		g = urllib2.Request(url)
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
		if cookie is not None:
			g.add_header('Cookie', cookie)
		g.add_header('Connection', 'keep-alive')
		if referer is not None:
			g.add_header('Referer', referer)
		g.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 5.1; rv:12.0) Gecko/20100101 Firefox/12.0')
		g.add_header('Content-Type', 'application/x-www-form-urlencoded')
		for i in range(count):
			try:
				resp = opener.open(g)
			except:
				print "open url error " + url
				resp = None
			if resp == None:
				continue
			else:
				return resp.read()
		return None

	def get_html2(self, url, count):
		for i in range(count):
			try:
				f = urllib2.urlopen(url)
			except:
				print "open url error " + url
				f = None
			if f == None:
			 	continue
			else:
				buf = f.read()
				f.close()
				return buf
		return None

def login_geewan_router():
	login_url = "http://192.168.199.1/"
	password = 'admin'

	a = login()
	first_buf = a.get_html2(login_url, 3)
	if first_buf == None:
		return
	redir = re.findall("href=\"(.*?)\"", first_buf)
	if redir == None:
		return
	login_buf = a.get_html2(login_url + redir[0], 3)
	re_name = re.findall("name=\"username\" value=\"(.*?)\"", login_buf);
	if re_name == None:
		return
	user_name = re_name[0]
	cookie_buf = a.login_server(login_url + redir[0], user_name, password, login_url + redir[0], 3)
	re_cookie = re.findall("(.*?); .*", cookie_buf)
	ret_list = []
	if re_cookie is not None:
		ret_list.append(re_cookie[0])
	re_stok = re.findall("(stok=.*?); .*", cookie_buf)
	if re_stok is not None:
		ret_list.append(re_stok[0])
	re_path = re.findall("path=(.*?); .*", cookie_buf)
	if re_path is not None:
		ret_list.append(re_path[0])
	return ret_list

def reboot_geenwan_router():
	url = "http://192.168.199.1/"
	ret_list = login_geewan_router()

	a = login()
	reboot = a.get_html4(url + ret_list[2] + ";" + ret_list[1] + "/api/sys/reboot",
				url + ret_list[2] + ";" + ret_list[1] + "/web/sys/sysinfo",
				ret_list[0], 3)
	print reboot

if __name__ == '__main__':
	print "hello world"
	reboot_geenwan_router()




