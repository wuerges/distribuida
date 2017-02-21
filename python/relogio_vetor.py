

class VC:
    def __init__(self, name):
        self.name = name
        self.v = { self.name : 0 }

    def increment(self):
        self.v[self.name] += 1
        return self

    def __repr__(self):
        return "V%s" % repr(self.v)

    # isso esta errado: a ordem nao e' total
    def __lt__(self, o):
        ks = list(set(self.v.keys()).union(set(o.v.keys())))
        ks.sort()
        def nextv(k, vz):
            if k in vz:
                return vz[k]
            else:
                return 0
        for k in ks:
            if nextv(k, self.v) > nextv(k, o.v):
                return False
        return True

    def update(self, o):
        for (k, v) in o.v.items():
            print(k,v)
            if k in self.v:
                if v >= self.v[k]:
                    self.v[k] = v
            else:
                self.v[k] = v





v1 = VC("http://localhost:8080/")
v2 = VC("http://localhost:8081/")
v3 = VC("http://localhost:8082/")

v1.increment()
v1.increment()
v1.increment()
print(v1)
v2.increment()
print(v2)

v2.update(v1)
v3.update(v1)
print(v2)
print(v3)

v1.increment()
v1.increment()

v2.update(v1)
print(v2)
v2.update(v3)
print(v2)

v2.update(v1)
v1.update(v2)
v1.increment()
v2.increment()
print("V1", v1)
print("V2", v2)
print(v1 > v2)
print(v1 < v2)


