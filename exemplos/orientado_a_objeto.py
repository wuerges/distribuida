import bottle        

class Srv(object):
    def __init__(self,param):
        self.param   = param

    def index1(self):
        return("I'm 1 | self.param = %s" % self.param)

    def index2(self, p1):
        return("I'm 2 | self.param = %s, p1 = %s" % (self.param, p1))



class Manager:
    def __init__(self):
        mysrv = Srv(param='some param')

        self.b = bottle.Bottle()
        self.b.get("/1")(mysrv.index1)
        self.b.get("/2/<p1>")(mysrv.index2)

    def run(self):
        self.b.run(host='localhost', port=8080)

m = Manager()
m.run()
