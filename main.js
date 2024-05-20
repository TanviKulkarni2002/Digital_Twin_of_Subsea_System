//Import the THREE.js library
import * as THREE from "https://cdn.skypack.dev/three@0.129.0/build/three.module.js";
// To allow for the camera to move around the scene
import { OrbitControls } from "https://cdn.skypack.dev/three@0.129.0/examples/jsm/controls/OrbitControls.js";
// To allow for importing the .gltf file
import { GLTFLoader } from "https://cdn.skypack.dev/three@0.129.0/examples/jsm/loaders/GLTFLoader.js";

//Create a Three.JS Scene
const scene = new THREE.Scene();
//create a new camera with positions and angles
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);

//Keep the 3D object on a global variable so we can access it later
let object;

//Instantiate a loader for the .gltf file
const loader = new GLTFLoader();
// const airFlow = document.getElementById('airFlow').value;
var air_pred=0,temp_pred=0,pres_pred=0;

document.getElementById('myform').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from submitting traditionally
    const formData = new FormData();
        formData.append('inputFile',document.getElementById('inputFile').files[0]);        
        // Make a POST request to your Flask API
        fetch('/predict', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                // Handle successful response
                return response.json(); // Parse response JSON
            } else {
                // Handle error response
                console.error('Failed to submit data');
                throw new Error('Failed to submit data');
            }
        })
        .then(data => {
            // Handle predictions
            air_pred = data.air;
            pres_pred = data.pressure;
            temp_pred = data.temp;
            console.log('Air Predictions:', air_pred);
            console.log('Pressure Predictions:', pres_pred);
            console.log('Temperature Predictions:', temp_pred);
            // Do something with the predictions (e.g., display them on the UI)
        })
        .catch(error => {
            // Handle network error
            console.error('Error:', error);
        });
    // Call the changecolor function with the obtained input values
    changeModelColor(air_pred, pres_pred,temp_pred);
});

function changeModelColor(airFlow, outletTemp, outletPressure) {

    // Define threshold values for each parameter
    const airflowThreshold = 100; // Example threshold for airflow
    const tempThreshold = 50; // Example threshold for outlet temperature
    const pressureThreshold = 25; // Example threshold for outlet pressure

    // Check if any of the input values are above their respective thresholds
    if (airFlow > airflowThreshold || outletTemp > tempThreshold || outletPressure > pressureThreshold) {
        // If any value is above its threshold, change the color of the model to red
        object.traverse((child) => {
            if (child.isMesh) {
                child.material.color.set(0xff0000); // Set color to red
            }
        });
    }
}


//Load the file
loader.load(
    '../model/3d Model/integratedparts_v4.gltf',
    function (gltf) {
        // If the file is loaded, add it to the scene
        object = gltf.scene;
        scene.add(object);
        console.log("Model loaded successfully:", object);
		// object.scale.set(1.5, 1.5, 1.5); // Adjust the scale as needed

        // changeModelColor(120, 60, 40); // Example input values

        // Start the animation after the model has been loaded
        animate();
    },
    function (xhr) {
        // While it is loading, log the progress
        console.log((xhr.loaded / xhr.total * 100) + '% loaded');
    },
    function (error) {
        // If there is an error, log it
        console.error("Error loading model:", error);
    }
);

//Instantiate a new renderer and set its size
const renderer = new THREE.WebGLRenderer({ alpha: true }); //Alpha: true allows for the transparent background
renderer.setSize(window.innerWidth, window.innerHeight);

//Add the renderer to the DOM
document.getElementById("container3D").appendChild(renderer.domElement);

camera.position.z = 4.5;
// camera.position.x = 9.5;

//Add lights to the scene, so we can actually see the 3D model
const topLight = new THREE.DirectionalLight(0xffffff, 1); // (color, intensity)
topLight.position.set(500, 500, 500) //top-left-ish
topLight.castShadow = true;
scene.add(topLight);

const ambientLight = new THREE.AmbientLight(0x333333, 1);
scene.add(ambientLight);

function animate() {
    requestAnimationFrame(animate);

    // Check if the object is defined
    if (object) {
        renderer.render(scene, camera);
    }
}

// //Add a listener to the window, so we can resize the window and the camera
// window.addEventListener("resize", function () {
// 	camera.aspect = window.innerWidth / window.innerHeight;
// 	camera.updateProjectionMatrix();
// 	renderer.setSize(window.innerWidth, window.innerHeight);
// });

let isDragging = false;
let previousMousePosition = {
    x: 0,
    y: 0
};

//Add mouse down event listener to start rotating the object
document.addEventListener('mousedown', (event) => {
    isDragging = true;
    previousMousePosition = {
        x: event.clientX,
        y: event.clientY
    };
});

//Add mouse move event listener to rotate the object
document.addEventListener('mousemove', (event) => {
    if (isDragging) {
        const deltaX = event.clientX - previousMousePosition.x;
        const deltaY = event.clientY - previousMousePosition.y;

        object.rotation.y += deltaX * 0.01;
        object.rotation.x += deltaY * 0.01;

        previousMousePosition = {
            x: event.clientX,
            y: event.clientY
        };
    }
});

//Add mouse up event listener to stop rotating the object
document.addEventListener('mouseup', () => {
    isDragging = false;
});

animate();

