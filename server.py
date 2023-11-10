from waitress import serve

from cbt.wsgi import application

if __name__=='__main__':
	print('running server')
	serve(application, host='0.0.0.0', port='8000')