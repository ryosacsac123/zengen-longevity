
// Module aliases
const Engine = Matter.Engine,
    Render = Matter.Render,
    Runner = Matter.Runner,
    Bodies = Matter.Bodies,
    Composite = Matter.Composite,
    Events = Matter.Events,
    MouseConstraint = Matter.MouseConstraint,
    Mouse = Matter.Mouse,
    Body = Matter.Body,
    Vector = Matter.Vector;

// Global physics variables
let engine, render, runner;
let orbs = [];
const width = window.innerWidth;
const height = window.innerHeight;

function initPhysics() {
    // Create engine
    engine = Engine.create();
    engine.world.gravity.y = 0; // Zero gravity initially for floating effect

    // Create renderer
    render = Render.create({
        element: document.getElementById('canvas-container'),
        engine: engine,
        options: {
            width: width,
            height: height,
            wireframes: false,
            background: 'transparent'
        }
    });

    // Create boundaries
    const ground = Bodies.rectangle(width / 2, height + 50, width, 100, { isStatic: true });
    const ceiling = Bodies.rectangle(width / 2, -50, width, 100, { isStatic: true });
    const leftWall = Bodies.rectangle(-50, height / 2, 100, height, { isStatic: true });
    const rightWall = Bodies.rectangle(width + 50, height / 2, 100, height, { isStatic: true });

    Composite.add(engine.world, [ground, ceiling, leftWall, rightWall]);

    // Add random Matcha and Seaweed orbs
    for (let i = 0; i < 30; i++) {
        addOrb();
    }

    // Add Mouse Interaction
    const mouse = Mouse.create(render.canvas);
    const mouseConstraint = MouseConstraint.create(engine, {
        mouse: mouse,
        constraint: {
            stiffness: 0.2,
            render: { visible: false }
        }
    });
    Composite.add(engine.world, mouseConstraint);

    // Keep mouse in sync with scrolling (though we have overflow hidden)
    render.mouse = mouse;

    // Run the engine
    Render.run(render);
    runner = Runner.create();
    Runner.run(runner, engine);

    // Add gentle floating motion
    Events.on(engine, 'beforeUpdate', function () {
        orbs.forEach(orb => {
            // Apply tiny random forces to simulate floating/Brownian motion if gravity is off
            if (engine.world.gravity.scale === 0) {
                Body.applyForce(orb, orb.position, {
                    x: (Math.random() - 0.5) * 0.0005,
                    y: (Math.random() - 0.5) * 0.0005
                });
            }
        });
    });
}

function addOrb() {
    const radius = 10 + Math.random() * 30;
    const x = Math.random() * width;
    const y = Math.random() * height;

    // 50% Matcha (Bright Green), 50% Seaweed (Darker Green)
    const isMatcha = Math.random() > 0.5;
    const color = isMatcha ? '#C5E1A5' : '#558B2F';

    const orb = Bodies.circle(x, y, radius, {
        restitution: 0.9, // Bouncy
        frictionAir: 0.01,
        render: {
            fillStyle: color,
            strokeStyle: '#ffffff',
            lineWidth: 1
        }
    });

    orbs.push(orb);
    Composite.add(engine.world, orb);
}

// Function to trigger the "Grid/Blackhole" effect
function triggerGravitySuck() {
    // Increase gravity scale or create a point attractor
    // For MVP, let's just use a point attractor logic in the update loop
    // But simplest visual is just high gravity to center? 
    // Actually, let's pull them to the center of the screen.

    Events.on(engine, 'beforeUpdate', function (event) {
        const center = { x: width / 2, y: height / 2 };
        orbs.forEach(orb => {
            const vector = Vector.sub(center, orb.position);
            // Apply force towards center
            Body.applyForce(orb, orb.position, Vector.mult(Vector.normalise(vector), 0.002 * orb.mass));
        });
    });
}

// Initialize on load
window.addEventListener('load', initPhysics);
window.addEventListener('resize', () => {
    // Basic resize handling
    render.canvas.width = window.innerWidth;
    render.canvas.height = window.innerHeight;
});
