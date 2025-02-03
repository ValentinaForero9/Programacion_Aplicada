// Variables para el joystick de la cámara (usando nipplejs)
var cameraJoystick = nipplejs.create({
    zone: document.getElementById('joystickCamera'),
    mode: 'static',
    position: { left: '50px', bottom: '50px' },
    color: 'blue',
    size: 100
});

var cameraRotation = { x: 0, y: 0 };
// Actualizar rotación de la cámara
function updateCameraRotation() {
    camera.position.x = 5 * Math.sin(cameraRotation.y);
    camera.position.z = 5 * Math.cos(cameraRotation.y);
    camera.lookAt(0, 0.5, 0);
}

cameraJoystick.on('move', function (evt, data) {
    if (data.direction) {
        if (data.direction.angle === 'left') {
            cameraRotation.y -= 0.05;
        }
        if (data.direction.angle === 'right') {
            cameraRotation.y += 0.05;
        }
        updateCameraRotation();
    }
});
// Variables para el joystick del brazo
const joystickArm = document.getElementById('joystickArm');
const joystickArmContainer = document.getElementById('joystickArmContainer');
let armPos = { x: 50, y: 50 };
// Obtener posición del joystick del brazo
function getJoystickPosition(event) {
    const rect = joystickArmContainer.getBoundingClientRect();
    const offsetX = (event.touches ? event.touches[0].clientX : event.clientX) - rect.left;
    const offsetY = (event.touches ? event.touches[0].clientY : event.clientY) - rect.top;
    const x = Math.min(Math.max(offsetX - 25, 0), rect.width - 50);
    const y = Math.min(Math.max(offsetY - 25, 0), rect.height - 50);
    return { x, y };
}

function updateArmJoystickPosition(event) {
    const { x, y } = getJoystickPosition(event);
    joystickArm.style.left = `${x}px`;
    joystickArm.style.top = `${y}px`;
    return { x, y };
}

function handleArmMove(event) {
    event.preventDefault();
    armPos = updateArmJoystickPosition(event);
    sendMessage(JSON.stringify({dx: armPos.x, dy: armPos.y}));
}

function handleArmEnd() {
    joystickArm.style.left = '50px';
    joystickArm.style.top = '50px';
    armPos = { x: 50, y: 50 };
    sendMessage(JSON.stringify({dx: 50, dy: 50}));

}
// Eventos para el joystick del brazo
joystickArmContainer.addEventListener('mousedown', handleArmMove);
joystickArmContainer.addEventListener('mousemove', handleArmMove);
joystickArmContainer.addEventListener('mouseup', handleArmEnd);
joystickArmContainer.addEventListener('mouseleave', handleArmEnd);
joystickArmContainer.addEventListener('touchstart', handleArmMove);
joystickArmContainer.addEventListener('touchmove', handleArmMove);
joystickArmContainer.addEventListener('touchend', handleArmEnd);
// WebSocket support
var targetUrl = `ws://${location.host}/ws`;
var websocket;
window.addEventListener("load", onLoad);

function onLoad() {
  initializeSocket();
}

function initializeSocket() {
  console.log("Opening WebSocket connection MicroPython Server...");
  websocket = new WebSocket(targetUrl);
  websocket.onopen = onOpen;
  websocket.onclose = onClose;
  websocket.onmessage = onMessage;
}
function onOpen(event) {
  console.log("Starting connection to WebSocket server..");
}
function onClose(event) {
  console.log("Closing connection to server..");
  setTimeout(initializeSocket, 2000);
}
function onMessage(event) {
  console.log("WebSocket message received:", event);
}

function sendMessage(message) {
  websocket.send(message);
}

const sceneContainer = document.getElementById('sceneContainer');
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ alpha: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
sceneContainer.appendChild(renderer.domElement);
// Cube (Base del robot)
var geometry = new THREE.BoxGeometry(1.5, 0.1, 1.8);
var material = new THREE.MeshStandardMaterial({ color: 0xa98307 });
var cube = new THREE.Mesh(geometry, material);
cube.castShadow = true;
cube.position.set(0, 1, 0);
scene.add(cube);
// Front Plate
var placa_geo1 = new THREE.BoxGeometry(0.1, 0.25, 0.9);
var placa1 = new THREE.Mesh(placa_geo1, material);
placa1.castShadow = true;
placa1.position.set(-0.1, 1.25, 0.25);
scene.add(placa1);
// Right side Plate
var placa_geo2 = new THREE.BoxGeometry(1, 2, 0.1);
var placa2 = new THREE.Mesh(placa_geo2, material);
placa2.castShadow = true;
placa2.position.set(0.25, 1, -0.25);
scene.add(placa2);
// Left side Plate
var placa_geo3 = new THREE.BoxGeometry(1, 2, 0.1);
var placa3 = new THREE.Mesh(placa_geo3, material);
placa3.castShadow = true;
placa3.position.set(0.25, 1, 0.75);
scene.add(placa3);
// Back Plate
var placa_geo4 = new THREE.BoxGeometry(0.1, 0.25, 0.9);
var placa4 = new THREE.Mesh(placa_geo4, material);
placa4.castShadow = true;
placa4.position.set(0.65, 1.25, 0.25);
scene.add(placa4);
// Rotor 1 
var rotor1 = new THREE.Object3D();
rotor1.position.set(0, 0.5, 0);
cube.add(rotor1);
// Articulacion 1
var size_position1 = 0.5;
var arti1_geo = new THREE.BoxGeometry(size_position1, 0.1, 0.05);
var arti1 = new THREE.Mesh(arti1_geo, material);
arti1.castShadow = true;
arti1.position.set(size_position1 / 2, 0, 0);
rotor1.add(arti1);
// Rotor 2
var rotor2 = new THREE.Object3D();
rotor2.position.set(0.25, 0, 0);
arti1.add(rotor2);
// Articulacion 2
var size_position2 = 1.5;
var arti2_geo = new THREE.BoxGeometry(0.1, size_position2, 0.05);
var arti2 = new THREE.Mesh(arti2_geo, material);
arti2.castShadow = true;
arti2.position.set(0, size_position2 / 2, 0);
rotor2.add(arti2);
// Rotor 3
var rotor3 = new THREE.Object3D();
rotor3.position.set(0, 0.75, 0);
arti2.add(rotor3);
// Articulacion 3
var size_position3 = 1.5;
var arti3_geo = new THREE.BoxGeometry(size_position3, 0.1, 0.05);
var arti3 = new THREE.Mesh(arti3_geo, material);
arti3.castShadow = true;
arti3.position.set(-size_position3 / 2, 0, 0);
rotor3.add(arti3);
// Rotor 4
var rotor4 = new THREE.Object3D();
rotor4.position.set(0, 0.5, 0);
cube.add(rotor4);
// Articulacion 4
var size_position4 = 1.5;
var arti4_geo = new THREE.BoxGeometry(0.1, size_position4, 0.05);
var arti4 = new THREE.Mesh(arti4_geo, material);
arti4.castShadow = true;
arti4.position.set(0, size_position4 / 2, 0);
rotor4.add(arti4);
// Rotor 5
var rotor5 = new THREE.Object3D();
rotor5.position.set(0, 0.5, 0.5);
cube.add(rotor5);
// Articulacion 5
var size_position5 = 1.5;
var arti5_geo = new THREE.BoxGeometry(0.1, size_position5, 0.05);
var arti5 = new THREE.Mesh(arti5_geo, material);
arti5.castShadow = true;
arti5.position.set(0, size_position5 / 2, 0);
rotor5.add(arti5);
// Rotor 6
var rotor6 = new THREE.Object3D();
rotor6.position.set(0.5, 0.75, 0.5);
cube.add(rotor6);
// Articulacion 6
var size_position6 = 1.4;
var arti6_geo = new THREE.BoxGeometry(0.1, size_position6, 0.05);
var arti6 = new THREE.Mesh(arti6_geo, material);
arti6.castShadow = true;
arti6.position.set(0, (size_position6 / 2), 0);
rotor6.add(arti6);
// Rotor 7
var rotor7 = new THREE.Object3D();
rotor7.position.set(0, 0.75, 0);
arti5.add(rotor7);
// Articulacion 7
var size_position7 = 1;
var arti7_geo = new THREE.BoxGeometry(size_position7, 0.1, 0.05);
var arti7 = new THREE.Mesh(arti7_geo, material);
arti7.castShadow = true;
arti7.position.set(-size_position7 / 2, 0, 0);
rotor7.add(arti7);
// Rotor 8
var rotor8 = new THREE.Object3D();
rotor8.position.set(0, 0.75, 0);
arti6.add(rotor8);
// Articulacion 8
var size_position8 = 0.6;
var arti8_geo = new THREE.BoxGeometry(size_position8, 0.1, 0.05);
var arti8 = new THREE.Mesh(arti8_geo, material);
arti8.castShadow = true;
arti8.position.set(-size_position8 / 2, 0, 0);
rotor8.add(arti8);
// mano 
var mano_geo = new THREE.BoxGeometry(0.1, 0.1, 0.5);
var mano = new THREE.Mesh(mano_geo, material);
mano.castShadow = true;
mano.position.set(-0.5, 0, -0.25);
arti7.add(mano);

function Cinematica_Directa(x1, y1){

    var x = (0.02936 * x1) - 2.43;
    var y = (-0.0315 * y1) + 2.3;
    var q1 = Cinematica_Inversa(x, y, 1.5, 1)[0];
    var q2 = Cinematica_Inversa(x, y, 1.5, 1)[1];
    
    const q1r = ((q1 - 90) * Math.PI) / 180;
    const q2r = (((q2 - 90) * Math.PI) / 180) + q1r;
    rotor1.rotation.z = q2r;
    rotor2.rotation.z = q1r - q2r;
    rotor3.rotation.z = - q1r + q2r;
    rotor4.rotation.z = q1r;
    rotor5.rotation.z = q1r;
    rotor6.rotation.z = q1r;
    rotor7.rotation.z = - q1r + q2r;
    rotor8.rotation.z = (Math.PI / 7.5) - q1r;

}

function Cinematica_Inversa(x, y, l1, l2) {

    const cos_q2 = (x * x + y * y - l1 * l1 - l2 * l2) / (2 * l1 * l2);
    const cos_q2_clamped = Math.max(-1, Math.min(1, cos_q2));
    const sin_q2 = Math.sqrt(1 - cos_q2_clamped ** 2);
    const q2 = Math.atan2(sin_q2, cos_q2_clamped);
    const q1 = Math.atan2(y, x) - Math.atan2(l2 * Math.sin(q2), l1 + l2 * Math.cos(q2));
    const q1_degrees = Math.round((q1 * 180) / Math.PI * 100) / 100;
    const q2_degrees = Math.round((q2 * 180) / Math.PI * 100) / 100;

    return [q1_degrees, q2_degrees];
}
// Light
var light = new THREE.DirectionalLight(0xffffff, 1);
light.position.set(5, 10, 5);
light.castShadow = true;
scene.add(light);
// Plane
var planeGeometry = new THREE.PlaneGeometry(20, 20);
var planeMaterial = new THREE.MeshStandardMaterial({ color: 0xfff0f0 });
var plane = new THREE.Mesh(planeGeometry, planeMaterial);
plane.rotation.x = -Math.PI / 2;
plane.receiveShadow = true;
plane.position.y = 0;
scene.add(plane);
// Ajustar la cámara
camera.position.set(3, 3, 4);
var cameraRotation = { x: 0, y: 0 };
camera.lookAt(0, 0.5, 0);

function animate() {
    requestAnimationFrame(animate);
    Cinematica_Directa(armPos.x, armPos.y);
    renderer.render(scene, camera);
}

animate();