import socketpool
import wifi
import re
import json
import pwmio
import board
import busio
import time
from digitalio import DigitalInOut
import adafruit_ssd1306
import math

pwm_base = pwmio.PWMOut(board.GP16, frequency=50)
pwm_brazo = pwmio.PWMOut(board.GP17, frequency=50)

i2c = busio.I2C(board.GP1, board.GP0)

reset_pin = DigitalInOut(board.GP5)

oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, reset=reset_pin)

oled.fill(0)
oled.show()

base_width = 10
base_height = 10
segment1_length = 30  
segment2_length = 20  


def draw_base():

    oled.fill_rect(64 - base_width // 2, 64 - base_height, base_width, base_height, 1)

def draw_arm(angle1, angle2):

    oled.fill(0)

    draw_base()

    x1 = 64  
    y1 = 64 - base_height  
    x2 = x1 + segment1_length * math.cos(math.radians(angle1))
    y2 = y1 - segment1_length * math.sin(math.radians(angle1))

    x2 = int(x2)
    y2 = int(y2)

    for offset in range(-1, 2):  
        oled.line(x1 + offset, y1, x2 + offset, y2, 1)

    x3 = x2
    y3 = y2
    x4 = x3 + segment2_length * math.cos(math.radians(angle1 + angle2))
    y4 = y3 - segment2_length * math.sin(math.radians(angle1 + angle2))

    x4 = int(x4)
    y4 = int(y4)

    for offset in range(-1, 2):  
        oled.line(x3 + offset, y3, x4 + offset, y4, 1)

    
    oled.show()


def angulo_a_pwm(angulo):
    return int((36.111 * angulo) + 1650)

ssid = 'FORERO MARENTES'
password = 'Alfor123'
wifi.radio.connect(ssid, password)

print('Conectado a Wi-Fi')
print('Dirección IP:', wifi.radio.ipv4_address)

html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Joystick y Brazo Virtual</title>
    <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
        }
        #joystickContainer {
            width: 200px;
            height: 200px;
            background-color: #ddd;
            border-radius: 50%;
            position: relative;
            touch-action: none;
            margin: 20px;
        }
        #joystick {
            width: 50px;
            height: 50px;
            background-color: #333;
            border-radius: 50%;
            position: absolute;
            left: 75px;
            top: 75px;
        }
        #sceneContainer {
            width: 100%;
            height: 80vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
    </style>
</head>
<body>
    <!-- Contenedor del Joystick -->
    <div id="joystickContainer">
        <div id="joystick"></div>
    </div>

    <!-- Contenedor del Brazo Virtual -->
    <div id="sceneContainer"></div>

<script src="https://cdn.jsdelivr.net/npm/three@0.126.1/build/three.min.js"></script>
    <script>
        const joystick = document.getElementById('joystick');
        const joystickContainer = document.getElementById('joystickContainer');
        let currentPos = { x: 75, y: 75 };

        function getJoystickPosition(event) {
            const rect = joystickContainer.getBoundingClientRect();
            const offsetX = (event.touches ? event.touches[0].clientX : event.clientX) - rect.left;
            const offsetY = (event.touches ? event.touches[0].clientY : event.clientY) - rect.top;
            const x = Math.min(Math.max(offsetX - 25, 0), rect.width - 50);
            const y = Math.min(Math.max(offsetY - 25, 0), rect.height - 50);
            return { x, y };
        }

        function updateJoystickPosition(event) {
            const { x, y } = getJoystickPosition(event);
            joystick.style.left = `${x}px`;
            joystick.style.top = `${y}px`;
            return { x, y };
        }

        function handleMove(event) {
            event.preventDefault();
            currentPos = updateJoystickPosition(event);
            sendJoystickData(currentPos.x, currentPos.y); // Enviar datos del joystick
        }

        function handleEnd() {
            joystick.style.left = '75px';
            joystick.style.top = '75px';
            currentPos = { x: 75, y: 75 };
            sendJoystickData(75, 75); // Restablecer el joystick al centro
        }

        joystickContainer.addEventListener('mousedown', handleMove);
        joystickContainer.addEventListener('mousemove', handleMove);
        joystickContainer.addEventListener('mouseup', handleEnd);
        joystickContainer.addEventListener('mouseleave', handleEnd);
        joystickContainer.addEventListener('touchstart', handleMove);
        joystickContainer.addEventListener('touchmove', handleMove);
        joystickContainer.addEventListener('touchend', handleEnd);

        let lastSendTime = 0;
        const throttleTime = 50;  // Enviar datos cada 50ms

        function sendJoystickData(x, y) {
            const now = Date.now();
            if (now - lastSendTime > throttleTime) {
                fetch(`/api?x=${x}&y=${y}`)
                    .then(response => response.json())
                    .then(data => console.log('Joystick data sent:', data))
                    .catch(error => console.error('Error:', error));
                lastSendTime = now;
            }
        }

        const sceneContainer = document.getElementById('sceneContainer');
        const width = window.innerWidth;
        const height = window.innerHeight * 0.8;
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer();
        renderer.setSize(width, height);
        sceneContainer.appendChild(renderer.domElement);

        const geometry = new THREE.BoxGeometry(1, 1, 1);
        const material = new THREE.MeshNormalMaterial();
        const base = new THREE.Mesh(geometry, material);
        base.translateY(0.5);
        scene.add(base);

        const shoulder = new THREE.Object3D();
        shoulder.translateY(0.5);
        base.add(shoulder);

        const geometry2 = new THREE.BoxGeometry(0.5, 2, 0.5);
        const PriBra = new THREE.Mesh(geometry2, material);
        PriBra.translateY(1);
        shoulder.add(PriBra);

        const Codo = new THREE.Object3D();
        Codo.translateY(1);
        Codo.rotation.x = Math.PI / 2;
        PriBra.add(Codo);

        const geometry3 = new THREE.BoxGeometry(0.25, 2, 0.25);
        const SegBra = new THREE.Mesh(geometry3, material);
        SegBra.translateY(1);
        Codo.add(SegBra);

        camera.position.set(5, 3, -1);
        camera.rotation.y = Math.PI / 2;

  function updateArmAngles(x, y) {
    const maxRotation = Math.PI; // Cambiado a 180 grados
    const maxRotation2 = Math.PI;
    const shoulderRotation = (x / 150) * maxRotation - maxRotation / 2;
    const elbowRotation = (y / 150) * maxRotation2 - maxRotation2 / 2;
    shoulder.rotation.x = shoulderRotation;
    Codo.rotation.x = elbowRotation;
}

        function animate() {
            requestAnimationFrame(animate);
            updateArmAngles(currentPos.x, currentPos.y);
            renderer.render(scene, camera);
        }

        animate();
    </script>
</body>
</html>
"""

def handle_request(client, chunk_size=1000):
    buffer = bytearray(1024)
    bytes_received, address = client.recvfrom_into(buffer)
    request_str = str(buffer[:bytes_received])
    
    if bytes_received == 0:
        print('No hay datos')
    elif 'GET / ' in request_str or 'GET /index.html' in request_str:
        client.send("HTTP/1.1 200 OK\r\n")
        client.send("Content-Type: text/html\r\n")
        client.send("Connection: close\r\n\r\n")
        for i in range(0, len(html), chunk_size):
            chunk = html[i:i + chunk_size]
            client.send(chunk)
    elif 'GET /api' in request_str:
        match = re.search(r'GET /api\?([^\s]+) HTTP', request_str)
        if match:
            query_string = match.group(1)
            params = query_string.split('&')
            json_data = {}
            for param in params:
                key, value = param.split('=')
                json_data[key] = value

            x_val = float(json_data.get('x', 75))
            y_val = float(json_data.get('y', 75))  

            angulo_base = (x_val / 150) * 180   
            angulo_brazo = (y_val / 150) * 90 - 45  
            
            draw_arm(angulo_base, angulo_brazo)
            
            pwm_base_val = angulo_a_pwm(- angulo_base + 180)
            pwm_brazo_val = angulo_a_pwm(angulo_brazo)

            pwm_base.duty_cycle = pwm_base_val
            pwm_brazo.duty_cycle = pwm_brazo_val

            print(f"Ángulo base: {angulo_base}, PWM base: {pwm_base_val}")
            print(f"Ángulo brazo: {angulo_brazo + 45}, PWM brazo: {pwm_brazo_val}")

        client.send("HTTP/1.1 200 OK\r\n")
        client.send("Content-Type: application/json\r\n")
        client.send("Connection: close\r\n\r\n")
        client.send(json.dumps({"status": "success", "received_data": json_data}).encode('utf-8'))
    else:
        client.send("HTTP/1.1 404 Not Found\r\n")
        client.send("Content-Type: text/plain\r\n")
        client.send("Connection: close\r\n\r\n")
        client.send("404 Not Found\r\n")

    client.close()

def start_server():
    pool = socketpool.SocketPool(wifi.radio)
    server_socket = pool.socket(pool.AF_INET, pool.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 80))
    server_socket.listen(1)

    print('Servidor escuchando en 0.0.0.0:80')

    while True:
        client, addr = server_socket.accept()
        handle_request(client)

start_server()
