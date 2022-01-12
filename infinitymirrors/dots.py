from LaplaceMirror import *


class Dots(Mirror):
    def run(self, speed = 3, num = 2, size=10):
        n = random.randint(0,self.n)
        i = -1
        while True:
            i = (i+1)%2
            if i == 0:
                while abs( (new_n:= random.randint(0,self.n)) -n ) < size +4: pass
                n = new_n
                h,s,l = random.random(), 0.5 + random.random()/2.0, 0.4 + random.random()/5.0
                r,g,b = [int(256*i) for i in colorsys.hls_to_rgb(h,l,s)]
                for enum,n_ in enumerate(range(n-size, n+size+1)):
                    self.add(n_, (r,g,b))
                    self.fade(1+abs(enum-size)*0.5, n_)

            self.fade(1.1)
            self.print()
            time.sleep(0.1)

if __name__ == "__main__":
    Dots().run()
