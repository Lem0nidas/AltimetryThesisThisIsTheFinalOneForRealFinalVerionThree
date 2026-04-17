<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { goto } from '$app/navigation';
	import * as THREE from 'three';
	import gsap from 'gsap';
	import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
	import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

	let canvas: HTMLDivElement;
	const loader = new GLTFLoader();

	onMount(() => {
		// Dimensions
		const width: number = window.innerWidth;
		const height: number = window.innerHeight;
		const aspectRatio: number = width / height;

		// Initialize the scene, camera and renderer
		const scene = new THREE.Scene();
		const camera = new THREE.PerspectiveCamera(25, aspectRatio, 0.1, 1000);
		const renderer = new THREE.WebGLRenderer({
			antialias: false // true for smoother edges, but it costs performance
		});

		const timeline = gsap.timeline();

		// const axesHelper = new THREE.AxesHelper(15);
		// scene.add(axesHelper);

		// camera.position.set(0.5, 2, 8);
		camera.position.set(0.2, 2.5, 1.5);
		camera.lookAt(0, 0, 0);

		timeline.to(
			camera.position,
			{
				x: 0,
				y: 0.4,
				z: 8.7,
				duration: 3,
				ease: 'power2.inOut',
				onUpdate: () => {
					camera.lookAt(0, 0, 0);
				}
			},
			0
		);

		timeline.to(camera.position, {
			y: 0,
			duration: 1,
			ease: 'power2.out',
			onUpdate: () => camera.lookAt(0, 0, 0)
		});

		timeline.fromTo(
			camera,
			{ fov: 10 },
			{
				fov: 25,
				duration: 2.5,
				onUpdate: () => camera.updateProjectionMatrix()
			},
			0
		);

		timeline.delay(0.5);

		renderer.setSize(width, height);
		canvas.appendChild(renderer.domElement);

		// Texture;
		// const textLoader = new THREE.TextureLoader();
		// textLoader
		// 	.loadAsync('/Yale Bright Star Map.jpg')
		// 	.then((texture) => {
		// 		scene.background = texture;
		// 	})
		// 	.catch((error) => {
		// 		console.log(error);
		// 	});

		const starFieldMaterial = new THREE.PointsMaterial({
			color: 0xffffff,
			size: 0.5, // Make stars smaller
			opacity: 0.3, // Lower opacity for softer look
			transparent: true
		});

		const starsGeometry = new THREE.BufferGeometry();
		const starsVertices = [];
		for (let i = 0; i < 10000; i++) {
			starsVertices.push(
				(Math.random() - 0.5) * 500,
				(Math.random() - 0.5) * 500,
				(Math.random() - 0.5) * 500
			);
		}
		starsGeometry.setAttribute('position', new THREE.Float32BufferAttribute(starsVertices, 3));

		const starField = new THREE.Points(starsGeometry, starFieldMaterial);
		scene.add(starField);

		// Load the 3D object (Earth model)
		let earthModel: THREE.Group<THREE.Object3DEventMap>;
		function loadEarth() {
			return new Promise((resolve, reject) => {
				loader.load(
					'/Earth_1_12756_edit.glb',
					function (gltf) {
						earthModel = gltf.scene;
						earthModel.name = 'Earth';
						earthModel.position.set(0, -1, 0);
						earthModel.scale.set(0.002, 0.002, 0.002);
						earthModel.rotation.y = THREE.MathUtils.degToRad(150);
						gsap.to(earthModel.position, {
							y: 0,
							duration: 2,
							ease: 'power3.out'
						});
						gsap.to(earthModel.rotation, {
							y: '+=0.5',
							duration: 3,
							ease: 'none'
						});
						scene.add(earthModel);

						// Set earthModel and camera position
						const box = new THREE.Box3().setFromObject(gltf.scene);
						const size = box.getSize(new THREE.Vector3()).length();
						// camera.position.set(0, 0, size * 2);

						// Add lighting
						const light = new THREE.AmbientLight(0xffffff, 0.2);
						scene.add(light);
						// const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
						// scene.add(directionalLight);
						// const helperLight = new THREE.DirectionalLightHelper(directionalLight, 1);
						// scene.add(helperLight);
						const sun = new THREE.DirectionalLight(0xffffff, 1.8);
						sun.position.set(5, 2, 5);
						scene.add(sun);

						sun.target = earthModel;
						scene.add(sun.target);

						const rimLight = new THREE.DirectionalLight(0x4aa3ff, 0.35);
						rimLight.position.set(-5, 1, -3);
						rimLight.color.set(0x6fb6ff);
						rimLight.intensity = 0.25;

						scene.add(rimLight);

						rimLight.target = earthModel;
						scene.add(rimLight.target);

						// const rimLight = new THREE.DirectionalLight(0x4aa3ff, 0.3);
						// rimLight.position.set(-5, 0, -5);
						// scene.add(rimLight);

						// Group camera and light
						// camera.add(directionalLight);
						// directionalLight.position.set(0, 2, -size);
						// directionalLight.rotation.set(0.5, 0, 0);
						scene.add(camera);
						resolve(earthModel);
					},
					undefined,
					(error) => reject(error)
				);
			});
		}

		const satellites: {
			path: string;
			scale: number;
		}[] = [
			{ path: 'j1.glb', scale: 0.8 },
			{ path: 'j2.glb', scale: 0.8 },
			{ path: 'j3.glb', scale: 0.8 },
			{ path: '6a.glb', scale: 0.5 },
			{ path: 'tx.glb', scale: 0.5 }
		];

		let allModels: {
			mesh: THREE.Group<THREE.Object3DEventMap>;
			offset: number;
			radius: number;
			angle: number;
			hoverSpeed: number;
			ready: boolean;
		}[] = [];
		let tempModels: THREE.Group<THREE.Object3DEventMap>[] = [];
		let hoveredModel: THREE.Object3D<THREE.Object3DEventMap> | null = null;

		function loadModel(path: string, scale: number): Promise<THREE.Group> {
			return new Promise((resolve, reject) => {
				loader.load(
					path,
					(gltf) => {
						const model = gltf.scene;
						const targetScale = normalizeScale(model, scale);
						model.name = path.substring(0, 2);
						model.scale.setScalar(targetScale);
						scene.add(model);
						resolve(model);
					},
					undefined,
					(error) => reject(error)
				);
			});
		}

		async function loadAllSatModels() {
			const promises = satellites.map((sat) => loadModel(sat.path, sat.scale));

			const models = await Promise.all(promises);
			return models;
		}

		function normalizeScale(model: THREE.Group<THREE.Object3DEventMap>, scale: number): number {
			const box = new THREE.Box3().setFromObject(model);
			const size = box.getSize(new THREE.Vector3());
			const max = Math.max(size.x, size.y, size.z);
			const target = scale;
			const scaleFactor = target / max;
			return scaleFactor;
		}

		// Add orbit controls
		// const controls = new OrbitControls(camera, canvas);
		// controls.autoRotate = true;
		// controls.enableDamping = true;

		function onResize() {
			const width = window.innerWidth;
			const height = window.innerHeight;

			renderer.setSize(width, height);
			camera.aspect = width / height;
			camera.updateProjectionMatrix();
		}

		window.addEventListener('resize', onResize);

		// Debug camera
		// scene.add(new THREE.CameraHelper(camera));
		const debugCamera = new THREE.PerspectiveCamera(60, width / height, 0.1, 1000);
		debugCamera.position.set(10, 10, 10);
		debugCamera.lookAt(0, 0, 0);

		//Raycasting
		const raycaster = new THREE.Raycaster();
		const mouse = new THREE.Vector2();
		let mouseDownPos = { x: 0, y: 0 };
		let selectedModel: THREE.Object3D | null = null;
		let isDragging = false;
		const clickThreshold = 5;

		function onMouseDown(event: MouseEvent) {
			isDragging = true;
			const rect = canvas.getBoundingClientRect();

			mouseDownPos.x = event.clientX;
			mouseDownPos.y = event.clientY;
			mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
			mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

			raycaster.setFromCamera(mouse, camera);

			const intersects = raycaster.intersectObjects([earthModel, ...tempModels], true);

			if (intersects.length > 0) {
				selectedModel = findRootModel(intersects[0].object, [earthModel, ...tempModels]);
			}
		}

		function findRootModel(object: THREE.Object3D, models: THREE.Object3D[]): THREE.Object3D {
			while (object.parent && !models.includes(object)) {
				object = object.parent;
			}
			return object;
		}

		let targetRotationX = 0;
		const damping = 0.1; // Lower = smoother/slower
		const springStrength = 0.5; // How fast it snaps back
		const maxRotationX = Math.PI / 100;
		function onMouseMove(event: MouseEvent) {
			if (!isDragging || !selectedModel) return;

			const movementX = event.movementX || 0;
			const movementY = event.movementY || 0;

			if (selectedModel.name == 'Earth') {
				targetRotationX += movementY * 0.005;
				selectedModel.rotation.y += movementX * 0.005;
			} else {
				selectedModel.rotation.y += movementX * 0.01;
				selectedModel.rotation.x += movementY * 0.01;
			}
		}

		function onMouseUp(event: MouseEvent) {
			if (!selectedModel) {
				isDragging = false;
				return;
			}

			const dx = event.clientX - mouseDownPos.x;
			const dy = event.clientY - mouseDownPos.y;
			const distance = Math.sqrt(dx * dx + dy * dy);

			// Only treat as click if mouse barely moved
			if (distance < clickThreshold) {
				goto('/download');
			}

			isDragging = false;
			selectedModel = null;
		}

		const plane = new THREE.Plane(new THREE.Vector3(0, 0, 1), 0);
		const point = new THREE.Vector3();
		let distanceFromEarth: number = 100;

		function checkHover(event: MouseEvent) {
			const mouse = new THREE.Vector2();
			const rect = canvas.getBoundingClientRect();

			mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
			mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

			raycaster.setFromCamera(mouse, camera);

			const intersects = raycaster.intersectObjects([earthModel, ...tempModels], true);

			if (intersects.length > 0) {
				const hovered = findRootModel(intersects[0].object, [earthModel, ...tempModels]);
				return hovered;
			}

			raycaster.ray.intersectPlane(plane, point);
			distanceFromEarth = point.distanceTo(new THREE.Vector3(0, 0, 0));

			return null;
		}

		canvas.addEventListener('mousedown', onMouseDown);
		canvas.addEventListener('mousemove', onMouseMove);
		canvas.addEventListener('mouseup', onMouseUp);
		canvas.addEventListener('mousemove', (event) => {
			hoveredModel = checkHover(event);
		});

		// Animate the scene
		let previousTime = 0;
		const speed = 1;

		function animate(time: number) {
			if (previousTime == 0) {
				previousTime = time;
				return;
			}
			const delta = (time - previousTime) / 1000;
			previousTime = time;
			// let distance = 0 - earthModel.position.y;
			// if (earthModel.position.y < 0) {
			// 	earthModel.position.y += (0 - earthModel.position.y) * speed * delta;
			// 	if (Math.abs(distance) < 0.005) {
			// 		earthModel.position.y = 0;
			// 	}
			// }

			if (selectedModel && selectedModel.name === 'Earth') {
				if (targetRotationX > maxRotationX) {
					targetRotationX += (maxRotationX - targetRotationX) * springStrength;
				} else if (targetRotationX < -maxRotationX) {
					targetRotationX += (-maxRotationX - targetRotationX) * springStrength;
				}

				selectedModel.rotation.x += (targetRotationX - selectedModel.rotation.x) * damping;
			}

			earthModel.rotation.y += THREE.MathUtils.degToRad(6) * delta;

			allModels.forEach((model) => {
				const targetHoverSpeed = distanceFromEarth > 1.8 ? 0.5 : 0;
				model.hoverSpeed += (targetHoverSpeed - model.hoverSpeed) * (1 - Math.exp(-2 * delta));
				if (!model.ready) {
					model.angle += 0.5 * delta;
					if (Math.abs(camera.position.y) < 0.5) {
						if (model.radius - 1.5 > 0.002) {
							model.radius += (1.5 - model.radius) * (1 - Math.exp(-2 * delta));
						} else {
							model.radius = 1.5;
							model.ready = true;
						}
					}
				} else {
					model.angle += model.hoverSpeed * delta;
				}

				// Set an initial rotation and only change the posistion. Updating rotation on every axis for every satellite and every frame is heavy
				model.mesh.rotation.x += THREE.MathUtils.degToRad(10) * delta;
				model.mesh.rotation.y += THREE.MathUtils.degToRad(10) * delta;
				model.mesh.rotation.z += THREE.MathUtils.degToRad(10) * delta;
				model.mesh.position.x = -(Math.sin(model.angle) * model.radius);
				model.mesh.position.y = Math.cos(model.angle) * model.radius;
			});
			// controls.update();
			renderer.setPixelRatio(1);
			renderer.render(scene, camera);
			// renderer.render(scene, debugCamera);
		}

		async function init() {
			await loadEarth();
			tempModels = await loadAllSatModels();
			allModels = tempModels.map((model, i) => {
				const offset = (i / tempModels.length) * Math.PI * 2;

				return {
					mesh: model,
					offset,
					radius: 5,
					angle: offset,
					hoverSpeed: 0.5,
					ready: false
				};
			});
		}

		init().then(() => {
			renderer.setAnimationLoop(animate);
		});

		// Stop animation when changing tabs
		document.addEventListener('visibilitychange', () => {
			if (document.hidden) {
				renderer.setAnimationLoop(null);
			} else {
				renderer.setAnimationLoop(animate);
			}
		});
	});

	onDestroy(() => {
		// canvas.removeEventListener("mousedown", onMouseDown);
		// canvas.removeEventListener("mousemove", onMouseMove);
		// canvas.removeEventListener("mouseup", onMouseUp);
		// scene.clear();
		// renderer.dispose();
	});
</script>

<div class="canvas-container" bind:this={canvas}></div>
