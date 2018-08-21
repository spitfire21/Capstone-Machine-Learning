import bottle, codecs, os, csv, json
from bottle import route, run, template, request,get, post, response

from beaker.middleware import SessionMiddleware

from model import model
from bottle_jwt import (JWTProviderPlugin, jwt_auth_required)
from bottle_jwt.backends import AuthBackend









app = bottle.app()
app.config.load_config('./etc/config.conf')
print(app.config)
server_secret = app.config['server_secret']
ssid = app.config['ssid']
twilio = app.config['twilio']

model = Model()
model.load_model()
"""@api {post} /login Login to the service with email and password.
   @apiVersion 0.0.1
   @apiName Login
   @apiGroup User

   @apiParam {String} email the user's email.
   @apiParam {String} password the user's password.

   @apiSuccess {String} email  email of the User.


 """


"""@api {post} /signup Signup to the service with email and password.
   @apiVersion 0.0.1
   @apiName Signup
   @apiGroup User

   @apiParam {String} email the user's email.
   @apiParam {String} password the user's password.

   @apiSuccess {String} email  email of the User.


 """


provider_plugin = JWTProviderPlugin(
	keyword='jwt',
	auth_endpoint='/login',
	register_endpoint='/signup',
	validate_endpoint='/validate',
	backend=AuthBackend('users'),
	fields=('username', 'password', 'email','phone','code'),
	secret=server_secret,
	ssid=ssid,
	twilio=twilio,

	ttl=30000
)
app.install(provider_plugin)






def enable_cors(fn):
	def _enable_cors(*args, **kwargs):
		# set CORS headers
		response.headers['Access-Control-Allow-Origin'] = '*'
		response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
		response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

		if bottle.request.method != 'OPTIONS':
			# actual request; reply with the actual response
			return fn(*args, **kwargs)

	return _enable_cors


def post_get(name, default=''):
	return bottle.request.POST.get(name, default).strip()


@route('/hello/<name>')
def index(name):
	return template('<b>Hello {{name}}</b>!', name=name)







@route('/model')
def main_model():

	return model.get_model()

@route('/histogram', method=['GET','OPTIONS'])
@jwt_auth_required
@enable_cors
def main_model():

	return model.histogram()


@route('/model/<i>')
def time(i):

	return model.get_time(int(i))


@route('/model/predict', method=['GET','OPTIONS','POST'])
@jwt_auth_required
@enable_cors
def predict():
	response.headers['Content-type'] = 'application/json'
	data = request.json

	x = list()
	length = len(data['values'])
	for i in data['values']:
		x.append(i)
	for i in range(length,32):
		x.append([0,0])

	x, RMSE = model.predict(x,length)
	return model.predict_helper(x,RMSE)

def date_Covert(data):
    print "DATA IS:", data
    dataS = data.strip('\r')
    months=[0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    x = dataS.split("/")
    print "x is equal to", x
    day = int(x[0])
    daysOfMonth = float(x[1])
    date = float(months[day])
    decimal = float(daysOfMonth/date)
    print "DECIMAL:", round(decimal,2)
    converted = float(day+round(decimal,2))
    print "CONVERTED:", converted
    return converted

@route('/upload', method='POST')
@jwt_auth_required
@enable_cors
def do_upload():
	final = list()
	batchList = list()
	athleteList = list()
	print(request.body.read())
	row = request.POST['uploaded_file'].file.getvalue().split('\n');
	for i in range(1, len(row)):
		data = row[i].split(',')
        	print "DATA ", data
		batch = list()
		for i in range(1,len(data),2):
                   if data[i] is not '':
		        batch.append([data[i],date_Covert(data[i+1])])
		for i in range(len(data),64):
			batch.append([0,0])
		batchList.append(batch)
		athleteList.append(data[0])
		print "BATCH IS ", batch
		res, RMSE = model.predict(batch,len(data)/2)

		for i in res:
			final.append(i)

	obj = json.loads(model.predict_helper(final,RMSE))
	obj["times"] = []
	obj["athletes"] =[]

	obj["times"].append(batchList)
	obj["athletes"].append(athleteList)
	return obj



def main():

	# Start the Bottle webapp

	bottle.debug(True)
	bottle.run(app=app, quiet=False, reloader=True)

if __name__ == "__main__":
	main()
