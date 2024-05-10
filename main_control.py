from machine import Pin, PWM
import utime
import network
import socket

pwmPIN_A = 12
cwPin_A = 11
acwPin_A = 10

pwmPIN_B = 15
cwPin_B = 14
acwPin_B = 13

pwmPIN_C = 18  
cwPin_C = 17   
acwPin_C = 16  

pwmPIN_D = 21   
cwPin_D = 20   
acwPin_D = 19 

def motorMove(speed, direction, speedGP, cwGP, acwGP):
    if speed > 100:
        speed = 100
    if speed < 0:
        speed = 0
    Speed = PWM(Pin(speedGP))
    Speed.freq(50)
    cw = Pin(cwGP, Pin.OUT)
    acw = Pin(acwGP, Pin.OUT)
    Speed.duty_u16(int(speed / 100 * 65536))
    if direction < 0:
        cw.value(0)
        acw.value(1)
    if direction == 0:
        cw.value(0)
        acw.value(0)
    if direction > 0:
        cw.value(1)
        acw.value(0)

def controlMotors(speed, direction):
    motorMove(speed, direction, pwmPIN_A, cwPin_A, acwPin_A)  # Control motor A
    motorMove(speed, direction, pwmPIN_B, cwPin_B, acwPin_B)  # Control motor B
    motorMove(speed, direction, pwmPIN_C, cwPin_C, acwPin_C)  # Control motor C
    motorMove(speed, direction, pwmPIN_D, cwPin_D, acwPin_D)  # Control motor D

ssid ='*********'
password = '********'
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    utime.sleep(1)

if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('WiFi connected')
    status = wlan.ifconfig()
    pico_ip = status[0]
    print('IP:', pico_ip)

addr = (pico_ip, 80)
s = socket.socket()
s.bind(addr)
s.listen(1)
print('Listening on', addr)

led_state = 0
# Main program
while True:
    client, client_addr = s.accept()
    raw_request = client.recv(1024)
    raw_request = raw_request.decode("utf-8")
    print(raw_request)

    request_parts = raw_request.split()
    http_method = request_parts[0]
    request_url = request_parts[1]

    if request_url == '/motoron':
        motorMove(100, 1, pwmPIN_A, cwPin_A, acwPin_A)
        motorMove(100, 1, pwmPIN_B, cwPin_B, acwPin_B)
        motorMove(100, 1, pwmPIN_C, cwPin_C, acwPin_C)
        motorMove(100, 1, pwmPIN_D, cwPin_D, acwPin_D)
        led_state = 1
    elif request_url == '/motoroff':
        motorMove(0, 0, pwmPIN_A, cwPin_A, acwPin_A)
        motorMove(0, 0, pwmPIN_B, cwPin_B, acwPin_B)
        motorMove(0, 0, pwmPIN_C, cwPin_C, acwPin_C)
        motorMove(0, 0, pwmPIN_D, cwPin_D, acwPin_D)
        led_state = 0
    elif request_url == '/left':
        motorMove(100, 1, pwmPIN_A, cwPin_A, acwPin_A)
        motorMove(100, 1, pwmPIN_B, cwPin_B, acwPin_B)
        motorMove(100, -1, pwmPIN_C, cwPin_C, acwPin_C)
        motorMove(100, -1, pwmPIN_D, cwPin_D, acwPin_D)
        led_state = 1
    elif request_url == '/right':
        motorMove(100, -1, pwmPIN_A, cwPin_A, acwPin_A)
        motorMove(100, -1, pwmPIN_B, cwPin_B, acwPin_B)
        motorMove(100, 1, pwmPIN_C, cwPin_C, acwPin_C)
        motorMove(100, 1, pwmPIN_D, cwPin_D, acwPin_D)
        led_state = 1
    elif request_url == '/forward':
        motorMove(100, -1, pwmPIN_A, cwPin_A, acwPin_A)
        motorMove(100, -1, pwmPIN_B, cwPin_B, acwPin_B)
        motorMove(100, -1, pwmPIN_C, cwPin_C, acwPin_C)
        motorMove(100, -1, pwmPIN_D, cwPin_D, acwPin_D)
        led_state = 1
    elif request_url == '/backward':
        motorMove(100, 1, pwmPIN_A, cwPin_A, acwPin_A)
        motorMove(100, 1, pwmPIN_B, cwPin_B, acwPin_B)
        motorMove(100, 1, pwmPIN_C, cwPin_C, acwPin_C)
        motorMove(100, 1, pwmPIN_D, cwPin_D, acwPin_D)
        led_state = 1
    
    led_state_text = "OFF"
    if led_state:
        led_state_text = "ON"
        
    file = open("Full_move.html")
    html = file.read()
    file.close()
    
    html = html.replace('*ledState*', led_state_text)
    client.send(html)
    client.close()
