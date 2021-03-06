import Adafruit_MCP3008

# SPI Configuration
CLK  = 18
MISO = 23
MOSI = 24
CS   = 25

mcp = None
alcohol = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
buffer_index = 1


def init():
    global mcp
    mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)


def get():
    # return last alcohol value read from breathalyzer
    global alcohol
    return alcohol[-1]


def update():
    # read real value from breathalyzer
    global alcohol
    global buffer_index

    value = mcp.read_adc(0)
    value = value - 190
    if value < 0:
        value = 0
    value = 1.9 * value / 1024.0
    value = round(value, 2)

    print "alcohol level: "+str(value)

    alcohol[buffer_index] = value
    buffer_index += 1
    if buffer_index == 20:
        buffer_index = 1


def danger():
    global alcohol
    med = sum(alcohol) / 20
    print med
    print 'breathalyzer danger: '+str(med)
    return med > 0.2

def set(value):
    # set value for demonstration
    global alcohol
    alcohol = value
