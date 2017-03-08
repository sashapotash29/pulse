from celery import Celery

app = Celery('tasks', backend='amqp', broker='amqp://localhost:5672/')

@app.task
def add():
	print ('hello')

@app.task(ignore_result=True)
def gen_prime(x):
	mult=[]
	res=[]
	for i in range(2,x+1):
		if i not in mult:
			res.append(i)
			for j in range(i*i,x+1,i):
				mult.append(i)
	print (res)