servo_values = open("servo_defaults.txt","r")
servo_values = servo_values.read()
print(servo_values)

class Servo:
    __channel = 0
    __minn = 200
    __maxx = 500
    __slope = 2.25

    def __init__(self, channel, hat, minn, maxx, slope):
        self.__channel = channel
        self.__hat = hat
        self.__minn = minn
        self.__maxx = maxx
        self.__slope = slope
    
    def set_channel(self, channel):
        self.__channel = channel

    def get_channel(self):
        return self.__channel

    def set_hat(self, hat):
        self.__hat = hat

    def get_hat(self):
        return self.__hat

    def set_minn(self, minn):
        self.__minn = minn

    def get_minn(self):
        return self.__minn

    def set_maxx(self, maxx):
        self.__maxx = maxx

    def get_maxx(self):
        return self.__maxx

    def set_slope(self, slope):
        self.__slope = slope

    def get_slope(self):
        return self.__slope

    def toString(self):
        return "Servo({})\n  Hat({})\n  min({})\n  max({})\n  slope({})".format(self.__channel,
                                                                                self.__hat,
                                                                                self.__minn,
                                                                                self.__maxx,
                                                                                slef.__slope)
