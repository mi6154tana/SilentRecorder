class DamyInput:
    def __init__(self):
        self.counter = 0
        f = open('./damy_input.txt','r')
        self.damy_line = []
        for i in f:
            self.damy_line.append(str(i).split())
        #tmp = f.readline()
        #self.damy_line = tmp.split()
    
    def rcv_input(self):
        #print('input : ', self.damy_line[self.counter])
        if self.counter > len(self.damy_line)-1:
            return '0:00000000'
        data  = ','.join(self.damy_line[self.counter])
        self.counter += 1
        return data 