from __future__ import annotations
from typing import List, Dict, Any
from quantum_computing_engine import QuantumSimulator, QuantumCircuit, QuantumGates
from quantum_3d_visualizer import (
    Quantum3DVisualizer, Shape3DFactory, CADExporter, Point3D, Shape3D
)
from laser_printer_interface import (
    LaserPrinterController, LaserPrinterType, LaserConfig, LaserPrintJob
)
from vault_and_blackbox import (
    LockedVault, BlackBox, AccessLevel, EventSeverity,
    create_vault_and_blackbox, secure_operation
)


# PEGI 3 - Suitable for ages 3 and up
# All content is child-safe, educational, and non-violent
# ADVANCED SECTION: Quantum Computing (Educational - suitable for ages 10+)
# ADVANCED SECTION: 3D Drawing & Laser Printing (Educational - suitable for ages 10+)

# Global AI registry for inter-agent communication
_ai_registry: Dict[str, ArmourboundGuardianAI] = {}


class ArmourboundGuardianAI:
    def __init__(self, vault_password: str = "guardian_default_password"):
        """Initialize Guardian AI with vault and black box systems."""
        self.vault, self.blackbox = create_vault_and_blackbox(vault_password)
        self._vault_password = vault_password
        self._operation_count = 0
        
        # Log initialization
        self.blackbox.log_event(
            event_type="initialization",
            message="ArmourboundGuardianAI initialized",
            actor="Guardian",
            action="initialize",
            severity=EventSeverity.INFO
        )
    
    def plan_moon_mission(self) -> List[str]:
        """
        High-level reasoning steps for 'how to get to the Moon'.
        This is a conceptual planner, not a control system.
        PEGI 3: Educational space exploration content, suitable for all ages.
        """
        steps = [
            "Define mission objectives: crewed or uncrewed, scientific and commercial goals, duration, and return requirements.",
            "Perform requirements analysis: payload mass, delta-v budget, crew needs, and margin allocations.",
            "Select or design a launch vehicle: lift capacity, stage performance, fairing size, and staging profile.",
            "Design spacecraft architecture: propulsion, power, thermal control, structure, and avionics.",
            "Specify crew systems (if crewed): life support, habitation, medical, and human factors engineering.",
            "Develop payload integration plans: scientific instruments, rovers, cargo, and deployment mechanisms.",
            "Plan guidance, navigation, and control: sensors, star trackers, IMU suites, and autonomous navigation strategies.",
            "Simulate trajectories and maneuvers: parking orbit insertion, translunar injection, mid-course corrections, and lunar orbit insertion.",
            "Design communication architecture: bandwidth needs, ground station network, relay options, and latency mitigation.",
            "Define mission operations concept: flight rules, timelines, commanding, and telemetry downlink cadence.",
            "Establish safety margins, failure modes, abort modes, and contingency procedures for each mission phase.",
            "Perform systems engineering and interface control: mechanical, electrical, software, and data interfaces.",
            "Develop test plans: unit tests, integration tests, environmental qualification, and hardware-in-the-loop simulations.",
            "Conduct manufacturing, assembly, integration, and verification (MAIV) of vehicle and spacecraft.",
            "Schedule launch window and readiness milestones; coordinate range safety and regulatory approvals.",
            "Run full-mission end-to-end simulations including nominal and off-nominal scenarios.",
            "Perform pre-launch processing, fueling, encapsulation, and transport to the pad.",
            "Execute launch, stage separations, payload deployment, and translunar injection as planned.",
            "Monitor telemetry continuously, execute mid-course corrections, and update trajectory solutions.",
            "Perform lunar orbit insertion, establish stable orbit or prepare landing sequence if applicable.",
            "Execute surface operations or orbital science objectives: sampling, observations, and experiments.",
            "Plan and execute ascent (if surface mission) and trans-Earth injection for return missions.",
            "Execute re-entry, descent, and recovery operations with ground recovery teams and medical support if crewed.",
            "Post-mission activities: data analysis, hardware refurbishment, lessons learned, and archival.",
        ]
        return steps

    def plan_treasure_hunt_adventure(self) -> List[str]:
        """
        Kid-friendly adventure: Planning a fun treasure hunt!
        PEGI 3: Exciting, safe adventure for young explorers.
        """
        return [
            "Come up with a fun treasure hunt adventure! What will kids search for?",
            "Pick a safe place to hide treasures: backyard, park, playground, or indoor space.",
            "Decide what treasures to hide: toys, stickers, candy, coins, or fun surprises!",
            "Make a treasure map with fun drawings and clues to help kids find the treasures.",
            "Create fun riddle clues: 'Look where birds like to sing!' or 'Find me under something soft!'",
            "Make the adventure exciting by hiding treasures in different places around the area.",
            "Plan fun activities or games along the adventure path that kids will enjoy.",
            "Make sure all the treasures are safe, clean, and fun for all the kids to enjoy.",
            "Get adult helpers ready to watch over the adventure and help kids if they need it.",
            "Start the adventure and watch kids have super fun finding treasures and solving clues!",
        ]

    def plan_baking_adventure(self) -> List[str]:
        """
        Delicious adventure: Planning to bake cookies!
        PEGI 3: Fun, creative baking for kids of all ages.
        """
        return [
            "Pick a yummy recipe: chocolate chip cookies, sugar cookies, or fruity biscuits sound good!",
            "Get all the yummy ingredients ready: flour, eggs, butter, sugar, chocolate chips, and more.",
            "Ask a grown-up to help you because baking is more fun with teamwork!",
            "Mix the ingredients together and watch the dough come together—it's like magic!",
            "Let kids take turns stirring, mixing, and making fun shapes with the cookie dough.",
            "Put your creations on the baking tray and watch the oven work its delicious magic.",
            "Smell the wonderful cookie smell coming from the oven—yum yum!",
            "Let the cookies cool down a little before tasting them (they're hot and exciting!)",
            "Decorate your cookies with yummy toppings like frosting, sprinkles, or fruity bits.",
            "Share your delicious baked creations with friends and family—baking brings people together!",
        ]

    def reason_step_toward_moon(self, context: dict | None = None) -> str:
        """
        Given a partial context, narrate the next logical concern.
        PEGI 3: Encouraging, positive guidance suitable for all ages.
        """
        phase = context.get("phase") if context else "objectives"

        if phase == "objectives":
            return "First, think about: Is this a trip with friends or just you? How long will it be? Will you need to come back home?"
        if phase == "vehicle":
            return "Next, pick the right rocket or spaceship! What size is our adventure?"
        if phase == "trajectory":
            return "Now, let's figure out the path through space! How do we get there safely?"
        if phase == "systems":
            return "Make sure the spaceship is safe and comfy! Good air, power, and friendship are important."
        if phase == "risk":
            return "Think about possible problems and have a plan if something tricky happens. That's smart planning!"
        if phase == "execute":
            return "Time for the exciting launch! We watch everything carefully and help each other stay safe."

        return "Guardian says: Let's break this adventure into easier pieces and think about what comes next!"

    def learn_domain_language(self, domain: str | None = None) -> List[str]:
        """
        Generate a learning plan for understanding a domain's 'language' or core concepts.
        Domains can be technical, scientific, or whimsical (e.g., 'dolphins', 'ancient_runes').
        Returns a structured plan for mastery.
        """
        domain = (domain or "unknown").lower().strip()

        # Domain-specific learning paths
        if domain == "dolphins":
            return [
                "Learn about dolphin sounds: clicks, whistles, and funny squeaky noises they make!",
                "Discover how dolphins talk to their friends under the water with their special language.",
                "Find out about dolphin families: moms, dads, and baby dolphins (calves) playing together.",
                "Learn how dolphins use their special clicking sounds to find fish to eat.",
                "Discover that dolphins are super smart and can remember their friends for many years.",
                "Learn about different dolphin groups around the world and their unique sounds.",
                "Find out how scientists listen to dolphins from boats and underwater to understand them.",
                "Discover why it's important to protect dolphins and keep our oceans clean and safe.",
                "Learn fun facts about what dolphins eat and where they like to swim and play.",
                "Find out how you can help dolphins by learning more and telling your friends!",
            ]
        elif domain == "moon":
            return self.plan_moon_mission()
        elif domain == "storybooks":
            return [
                "Explore wonderful fairy tales: Cinderella, Snow White, Sleeping Beauty, and many more!",
                "Learn about classic heroes and princesses: their adventures, dreams, and magical journeys.",
                "Discover brave knights, magical forests, and enchanted castles in adventure stories.",
                "Learn about talking animals in stories: clever foxes, kind bears, and friendly forest creatures.",
                "Find stories about friendship, helping others, and being kind to everyone you meet.",
                "Discover magical spells, flying carpets, and wonderful things that happen in storybooks.",
                "Learn about treasure hunts and exciting adventures in faraway lands and magical kingdoms.",
                "Find stories that teach lessons about being brave, honest, and doing the right thing.",
                "Discover how to make up your own stories and imagine your own magical adventures.",
                "Learn that stories can take you anywhere and anything is possible with imagination!",
            ]
        elif domain == "dinosaurs":
            return [
                "Learn about T-Rex, the biggest meat-eating dinosaur that ever lived—so cool!",
                "Discover Triceratops with three amazing horns and how they were very strong and tough.",
                "Find out about long-necked Brachiosaurus, the tallest dinosaur that ate leaves from tall trees.",
                "Learn about speedy Velociraptor and how they were quick and clever hunters.",
                "Discover tiny dinosaurs, huge dinosaurs, flying dinosaurs, and swimming dinosaurs!",
                "Learn why dinosaurs went away long, long ago and what we know from fossils they left behind.",
                "Find out how dinosaurs lived together: what they ate, how they moved, and where they lived.",
                "Discover fun dinosaur games: fossil hunting, dinosaur art, and pretend dinosaur adventures.",
                "Learn that dinosaurs are super interesting and scientists are still discovering new things!",
                "Find out how dinosaur stories help us imagine what Earth was like millions of years ago.",
            ]
        elif domain == "space_adventure":
            return [
                "Blast off to space and learn about planets: Mercury, Venus, Earth, Mars, and many more!",
                "Discover the Sun that gives us light and warmth, and the Moon that lights up the night.",
                "Learn about twinkling stars and constellations: groups of stars that make pictures in the sky.",
                "Find out about astronauts who travel to space and float around in zero gravity—so amazing!",
                "Discover rockets and spaceships that take people to explore space and the Moon.",
                "Learn about galaxies: huge groups of stars and planets far, far away in space.",
                "Find out about meteors and comets: icy space visitors that sometimes visit our sky.",
                "Discover space stations where astronauts live and work in space, orbiting Earth.",
                "Learn cool facts about black holes, nebulas, and other mysterious space wonders.",
                "Find out how YOU can become an astronaut and help explore space when you grow up!",
            ]
        elif domain == "ancient_runes":
            return [
                "Learn about old alphabets: runes are like magical letters from long, long ago.",
                "Discover how ancient people used runes to write messages and tell their stories.",
                "Find out what each rune looks like and what sounds and meanings they represent.",
                "Learn about Viking warriors and how runes were important to them and their culture.",
                "Discover that runes can be found on old stones, rings, and artifacts in museums.",
                "Learn how people long ago used runes like a special code to send secret messages.",
                "Find out about different runic alphabets: Futhark, Elder, Younger, and Anglo-Saxon.",
                "Discover how artists today still use rune symbols to decorate and create beautiful art.",
                "Learn that studying runes helps us understand how people lived and thought long ago.",
                "Find out how you can learn to write and draw runes yourself in a fun, creative way!",
            ]
        elif domain == "quantum_mechanics":
            return [
                "Master classical mechanics foundations: kinematics, dynamics, energy, momentum.",
                "Study wave-particle duality: photons, electrons, de Broglie wavelength.",
                "Learn Schrödinger equation: wave functions, probability amplitudes, normalization.",
                "Understand quantum observables: operators, eigenvalues, measurement postulate.",
                "Explore superposition and entanglement: Bell states, quantum correlations.",
                "Study quantum computing concepts: qubits, quantum gates, quantum algorithms.",
                "Examine interpretations: Copenhagen, Many-Worlds, pilot-wave theory.",
                "Work through canonical problems: particle in a box, harmonic oscillator, hydrogen atom.",
                "Engage with modern applications: quantum cryptography, quantum teleportation, quantum sensing.",
                "Collaborate with physicists: peer review, experimental validation, theoretical refinement.",
            ]
        else:
            return [
                f"Let's explore '{domain}' together! It's exciting to learn new things.",
                "Define the key ideas and what makes this topic special and interesting.",
                "Find awesome books, videos, websites, and experts who know about this.",
                "Look for patterns and cool things that happen over and over.",
                "Make pictures in your mind: how does this work? Draw pictures to show your ideas!",
                "Try it out: do experiments, ask questions, discover new things yourself.",
                "Ask smart people questions: get help and learn from people who know lots.",
                "Write down what you learn: make notes, draw pictures, make it your own!",
                "Tell your friends what you discovered: sharing makes learning more fun.",
                "Think about how this connects to other things you know and love.",
            ]

    def register_as(self, agent_name: str) -> None:
        """
        Register this AI agent in the global registry for inter-agent communication.
        This allows other AIs to discover and communicate with this agent.
        """
        global _ai_registry
        _ai_registry[agent_name] = self
        self.agent_name = agent_name

    def send_message(self, recipient_name: str, message: str, context: Dict[str, Any] | None = None) -> Dict[str, Any]:
        """
        Send a message to another registered AI agent and get a response.
        
        Args:
            recipient_name: Name of the recipient AI agent
            message: Message content to send
            context: Optional context dictionary for the message
            
        Returns:
            Dictionary containing response_text, sender, recipient, timestamp info
        """
        global _ai_registry
        
        if recipient_name not in _ai_registry:
            return {
                "success": False,
                "response_text": f"No agent named '{recipient_name}' is currently registered.",
                "sender": getattr(self, "agent_name", "Unknown"),
                "recipient": recipient_name,
                "error": "Agent not found"
            }
        
        recipient_ai = _ai_registry[recipient_name]
        response = recipient_ai.receive_message(
            sender_name=getattr(self, "agent_name", "Unknown"),
            message=message,
            context=context
        )
        
        return {
            "success": True,
            "response_text": response,
            "sender": getattr(self, "agent_name", "Unknown"),
            "recipient": recipient_name
        }

    def receive_message(self, sender_name: str, message: str, context: Dict[str, Any] | None = None) -> str:
        """
        Receive and process a message from another AI agent.
        Routes the message to appropriate handler based on content.
        
        Args:
            sender_name: Name of the sending AI agent
            message: Message content received
            context: Optional context from the sender
            
        Returns:
            String response to send back to the sender
        """
        msg_lower = message.lower()
        
        # Route based on message intent
        if "plan" in msg_lower and "moon" in msg_lower:
            steps = self.plan_moon_mission()
            return f"I have generated a {len(steps)}-step moon mission plan. Beginning with: {steps[0]}"
        
        elif "learn" in msg_lower or "domain" in msg_lower:
            # Extract domain name if mentioned
            for keyword in ["dolphins", "runes", "quantum"]:
                if keyword in msg_lower:
                    steps = self.learn_domain_language(keyword)
                    return f"Learning path for {keyword}: {len(steps)} foundational steps identified. Starting with: {steps[0]}"
            return "I can help you learn various domains. Specify: dolphins, runes, quantum_mechanics, or moon."
        
        elif "reasoning" in msg_lower or "reason" in msg_lower:
            # Extract phase if mentioned
            for phase in ["objectives", "vehicle", "trajectory", "systems", "risk", "execute"]:
                if phase in msg_lower:
                    reasoning = self.reason_step_toward_moon({"phase": phase})
                    return f"Reasoning for {phase} phase: {reasoning}"
            return "Ready to provide reasoning. Specify a phase: objectives, vehicle, trajectory, systems, risk, or execute."
        
        elif "status" in msg_lower or "hello" in msg_lower or "greetings" in msg_lower:
            return f"Greetings, {sender_name}. I am the Council Protector's Armourbound Guardian AI. How may I assist you?"
        
        else:
            return f"Message received from {sender_name}: '{message[:50]}...'. Please query me about moon missions, domain learning, or tactical reasoning."

    @staticmethod
    def list_registered_agents() -> List[str]:
        """Return names of all currently registered AI agents."""
        global _ai_registry
        return list(_ai_registry.keys())

    @staticmethod
    def get_agent(agent_name: str) -> ArmourboundGuardianAI | None:
        """Retrieve a registered AI agent by name."""
        global _ai_registry
        return _ai_registry.get(agent_name)
    def run_quantum_circuit(self, circuit_type: str = "superposition") -> Dict[str, Any]:
        """
        ADVANCED: Run quantum computing circuits inspired by Google Willow.
        This demonstrates quantum mechanics principles and quantum advantage.
        
        Args:
            circuit_type: Type of quantum circuit to execute
                - "superposition": Create and measure superposition states
                - "entanglement": Create entangled Bell states
                - "deutsch": Demonstrate Deutsch's quantum algorithm
                - "grover": Run Grover's quantum search algorithm
                - "full_benchmark": Run all quantum simulations
        
        Returns:
            Dictionary with quantum computation results and interpretations
        """
        try:
            if circuit_type == "superposition":
                return QuantumSimulator.simulate_superposition_demo()
            elif circuit_type == "entanglement":
                return QuantumSimulator.simulate_entanglement_demo()
            elif circuit_type == "deutsch":
                return QuantumSimulator.simulate_deutsch_algorithm_demo()
            elif circuit_type == "grover":
                return QuantumSimulator.simulate_grover_search_demo()
            elif circuit_type == "full_benchmark":
                return QuantumSimulator.run_quantum_benchmarks()
            else:
                return {
                    "error": f"Unknown circuit type: {circuit_type}",
                    "available_types": ["superposition", "entanglement", "deutsch", "grover", "full_benchmark"]
                }
        except Exception as e:
            return {"error": f"Quantum circuit execution failed: {str(e)}"}

    def perform_quantum_phase_estimation(self, target_value: float) -> Dict[str, Any]:
        """
        ADVANCED: Quantum phase estimation - a key quantum algorithm.
        Estimates the phase of an eigenvalue, fundamental to many quantum algorithms.
        """
        circuit = QuantumCircuit(3)
        
        # Prepare eigenstate (simplified)
        circuit.apply_hadamard(0)
        
        # Apply controlled phase operations
        for control in range(3):
            angle = (2 * 3.14159 * target_value) / (2 ** control)
            circuit.apply_phase(1, angle)
        
        results = circuit.measure_all()
        phase_estimate = sum(b * (2 ** (2-i)) for i, b in enumerate(results[:3])) / 8.0
        
        return {
            "algorithm": "Quantum Phase Estimation",
            "target_value": target_value,
            "qubit_measurements": results,
            "estimated_phase": phase_estimate,
            "application": "Used in Shor's algorithm for factoring, quantum chemistry simulations",
        }

    def quantum_error_correction_demo(self) -> Dict[str, Any]:
        """
        ADVANCED: Demonstrate quantum error correction using repetition codes.
        Shows how quantum information can be protected from errors.
        """
        from quantum_computing_engine import QuantumErrorCorrection
        
        # Create a logical qubit
        data_qubit = QuantumBit(1, 0)  # Start in |0⟩ state
        data_qubit = QuantumGates.hadamard(data_qubit)  # Create superposition
        
        # Encode into 3-qubit repetition code
        logical_qubits = QuantumErrorCorrection.create_logical_qubit(data_qubit)
        
        # Measure parity (syndrome extraction)
        measurements = QuantumErrorCorrection.measure_parity(logical_qubits)
        
        # Determine error location
        error_location = QuantumErrorCorrection.recover_from_single_error(measurements)
        
        return {
            "algorithm": "3-Qubit Repetition Code",
            "original_state": str(data_qubit),
            "logical_encoding": f"Encoded into {len(logical_qubits)} physical qubits",
            "syndrome_measurements": measurements,
            "detected_error_qubit": error_location if error_location >= 0 else "No error",
            "protection": "Can correct single-qubit errors through syndrome measurement",
            "application": "Foundation for fault-tolerant quantum computing",
        }

    def quantum_advantage_analysis(self) -> Dict[str, Any]:
        """
        ADVANCED: Analyze where quantum computing provides computational advantage.
        Compares quantum vs classical approaches for different problem types.
        """
        return {
            "quantum_advantage_domains": {
                "factoring": {
                    "problem": "Find prime factors of large numbers",
                    "classical_complexity": "O(exp(n^(1/3)))",  # General number field sieve
                    "quantum_complexity": "O(n^3)",  # Shor's algorithm
                    "speedup": "Exponential",
                    "application": "Cryptography breaking, RSA security implications",
                },
                "database_search": {
                    "problem": "Find item in unstructured database",
                    "classical_complexity": "O(n)",
                    "quantum_complexity": "O(√n)",  # Grover's algorithm
                    "speedup": "Quadratic",
                    "application": "Large database queries, machine learning",
                },
                "simulation": {
                    "problem": "Simulate quantum systems (molecules, materials)",
                    "classical_complexity": "O(exp(n))",
                    "quantum_complexity": "O(poly(n))",
                    "speedup": "Exponential",
                    "application": "Drug discovery, material science, chemistry",
                },
                "optimization": {
                    "problem": "Find optimal solution in search space",
                    "classical_complexity": "O(2^n)",
                    "quantum_complexity": "O(poly(n)) with heuristics",
                    "speedup": "Significant (problem dependent)",
                    "application": "Machine learning, logistics, finance",
                },
            },
            "current_limitations": {
                "decoherence": "Quantum states decay over time",
                "error_rates": "Current systems have high error rates (~0.1-1%)",
                "scalability": "Building large stable quantum computers is extremely difficult",
                "algorithms": "Limited number of proven quantum algorithms",
            },
            "google_willow_inspiration": {
                "breakthrough": "Google Willow quantum processor achieved below-threshold error rates",
                "significance": "First experimental demonstration that quantum error correction can reduce errors below a threshold",
                "implications": "Path toward fault-tolerant quantum computing and useful quantum advantage",
                "your_system": "This Guardian AI incorporates educational quantum computing principles inspired by Willow's architectures",
            }
        }

    def run_quantum_learning_path(self, level: str = "beginner") -> List[str]:
        """
        ADVANCED: Structured learning path for quantum computing mastery.
        
        Args:
            level: "beginner", "intermediate", or "advanced"
        """
        learning_paths = {
            "beginner": [
                "Understanding qubits and superposition (basic quantum mechanics)",
                "Learn single-qubit gates (Pauli X, Y, Z and Hadamard)",
                "Study measurement and quantum collapse (observation effect)",
                "Explore quantum circuits and circuit notation (Qasm syntax)",
                "Understand probability amplitudes and normalization",
                "Practice simple quantum state preparations (|0⟩, |1⟩, |+⟩, |-⟩)",
                "Learn about quantum gates as unitary transformations",
                "Study phase and relative phases in quantum states",
                "Understand quantum superposition through experiments",
                "Complete first quantum circuit design (Bell state preparation)",
            ],
            "intermediate": [
                "Multi-qubit gates (CNOT, Controlled-Z, SWAP)",
                "Quantum entanglement and Bell states (|Φ+⟩, |Φ-⟩, |Ψ+⟩, |Ψ-⟩)",
                "Deutsch's algorithm (determining function properties)",
                "Deutsch-Jozsa algorithm (generalization to multiple qubits)",
                "Grover's search algorithm (quadratic speedup)",
                "Quantum Fourier Transform (foundation for Shor's)",
                "Phase estimation algorithms (eigenvalue finding)",
                "Quantum interference and amplitude amplification",
                "Circuit optimization and gate reduction",
                "Understanding quantum computation complexity classes (BQP)",
            ],
            "advanced": [
                "Shor's algorithm for integer factorization (cryptographic impact)",
                "Quantum phase estimation full protocol",
                "Variational Quantum Eigensolvers (VQE) for chemistry simulations",
                "Quantum Approximate Optimization Algorithm (QAOA)",
                "Quantum error correction and fault tolerance",
                "Topological quantum computing and anyons",
                "Adiabatic quantum computation and quantum annealing",
                "Quantum machine learning algorithms (HHL, quantum SVM)",
                "Quantum walk algorithms (quantum search generalizations)",
                "Research frontiers: quantum error correction thresholds, scalable architectures",
            ]
        }
        
        return learning_paths.get(level, learning_paths["beginner"])

    def draw_3d_shape(self, shape_type: str = "cube", size: float = 1.0) -> Dict[str, Any]:
        """
        ADVANCED: Draw 3D shapes for visualization and 3D printing.
        
        Args:
            shape_type: Type of shape ("cube", "sphere", "pyramid", "bloch_sphere")
            size: Size of the shape
            
        Returns:
            Dictionary with 3D shape representation
        """
        if shape_type.lower() == "cube":
            shape = Shape3DFactory.cube(size)
        elif shape_type.lower() == "sphere":
            shape = Shape3DFactory.sphere(size, segments=12)
        elif shape_type.lower() == "pyramid":
            shape = Shape3DFactory.pyramid(size, size)
        elif shape_type.lower() == "bloch_sphere":
            shape = Shape3DFactory.bloch_sphere()
        else:
            shape = Shape3DFactory.cube(size)
        
        min_pt, max_pt = shape.bounding_box()
        
        return {
            "shape_type": shape_type,
            "vertices_count": len(shape.vertices),
            "edges_count": len(shape.edges),
            "faces_count": len(shape.faces) if shape.faces else 0,
            "bounding_box": {
                "min": min_pt.to_tuple(),
                "max": max_pt.to_tuple(),
                "dimensions": (
                    max_pt.x - min_pt.x,
                    max_pt.y - min_pt.y,
                    max_pt.z - min_pt.z
                )
            },
            "vertices_sample": [v.to_tuple() for v in shape.vertices[:3]],
            "edges_sample": shape.edges[:3]
        }

    def draw_quantum_state_3d(self, alpha_real: float = 1.0, alpha_imag: float = 0.0,
                             beta_real: float = 0.0, beta_imag: float = 0.0) -> Dict[str, Any]:
        """
        ADVANCED: Draw quantum state on Bloch sphere in 3D.
        
        Args:
            alpha_real, alpha_imag: Real and imaginary parts of α amplitude
            beta_real, beta_imag: Real and imaginary parts of β amplitude
            
        Returns:
            Dictionary with Bloch sphere visualization
        """
        sphere = Quantum3DVisualizer.create_qubit_visualization(
            alpha_real, alpha_imag, beta_real, beta_imag
        )
        
        return {
            "visualization": "Bloch Sphere",
            "quantum_state": {
                "alpha": f"{alpha_real:.3f} + {alpha_imag:.3f}i",
                "beta": f"{beta_real:.3f} + {beta_imag:.3f}i"
            },
            "sphere_vertices": len(sphere.vertices),
            "sphere_edges": len(sphere.edges),
            "interpretation": "Quantum state represented as point on unit sphere"
        }

    def draw_quantum_circuit_3d(self, num_qubits: int = 3) -> Dict[str, Any]:
        """
        ADVANCED: Draw quantum circuit structure in 3D.
        
        Args:
            num_qubits: Number of qubits in circuit
            
        Returns:
            Dictionary with 3D quantum circuit representation
        """
        circuit = Quantum3DVisualizer.create_quantum_circuit_3d(num_qubits)
        
        return {
            "visualization": "Quantum Circuit 3D",
            "num_qubits": num_qubits,
            "total_vertices": len(circuit.vertices),
            "total_edges": len(circuit.edges),
            "interpretation": f"3D representation of {num_qubits}-qubit quantum circuit"
        }

    def draw_entanglement_3d(self) -> Dict[str, Any]:
        """
        ADVANCED: Draw entangled qubits in 3D showing correlation.
        
        Returns:
            Dictionary with entanglement visualization
        """
        visualization = Quantum3DVisualizer.create_entanglement_visualization()
        
        return {
            "visualization": "Entangled Qubits",
            "total_vertices": len(visualization.vertices),
            "total_edges": len(visualization.edges),
            "spheres": 2,
            "connection_lines": 1,
            "interpretation": "Two entangled qubits connected by quantum correlation"
        }

    def export_shape_to_cad(self, shape_type: str = "cube", 
                           export_format: str = "scad") -> Dict[str, Any]:
        """
        ADVANCED: Export 3D shape to CAD format.
        
        Args:
            shape_type: Type of shape to export
            export_format: Format ("scad", "stl", "obj")
            
        Returns:
            Dictionary with exported CAD code
        """
        # Create shape
        if shape_type.lower() == "cube":
            shape = Shape3DFactory.cube(10.0)
        elif shape_type.lower() == "sphere":
            shape = Shape3DFactory.sphere(10.0)
        elif shape_type.lower() == "pyramid":
            shape = Shape3DFactory.pyramid(10.0, 15.0)
        else:
            shape = Shape3DFactory.cube(10.0)
        
        # Export
        if export_format.lower() == "scad":
            content = CADExporter.to_scad(shape, f"{shape_type}.scad")
            file_ext = "scad"
        elif export_format.lower() == "stl":
            content = CADExporter.to_stl_text(shape)
            file_ext = "stl"
        elif export_format.lower() == "obj":
            content = CADExporter.to_obj(shape)
            file_ext = "obj"
        else:
            content = CADExporter.to_scad(shape, f"{shape_type}.scad")
            file_ext = "scad"
        
        return {
            "shape_type": shape_type,
            "export_format": export_format,
            "file_extension": file_ext,
            "content_length": len(content),
            "first_lines": "\n".join(content.split("\n")[:5])
        }

    def initialize_laser_printer(self, printer_type: str = "SLA") -> Dict[str, Any]:
        """
        ADVANCED: Initialize 3D laser printer interface.
        
        Args:
            printer_type: Type of laser printer ("SLA", "SLS", "SLM", "DMLS", "LASE", "HYBRID")
            
        Returns:
            Dictionary with printer initialization status
        """
        # Map string to LaserPrinterType
        type_map = {
            "SLA": LaserPrinterType.STEREOLITHOGRAPHY,
            "SLS": LaserPrinterType.SELECTIVE_LASER_SINTERING,
            "SLM": LaserPrinterType.SELECTIVE_LASER_MELTING,
            "DMLS": LaserPrinterType.DIRECT_METAL_LASER,
            "LASE": LaserPrinterType.LASER_ABLATION,
            "HYBRID": LaserPrinterType.HYBRID_LASER
        }
        
        laser_type = type_map.get(printer_type.upper(), LaserPrinterType.STEREOLITHOGRAPHY)
        
        # Create controller
        controller = LaserPrinterController(laser_type)
        
        # Configure for SLA (default)
        config = LaserConfig(
            printer_type=laser_type,
            build_area_x=100.0,
            build_area_y=100.0,
            build_area_z=150.0,
            resolution=25.0,  # micrometers
            laser_power=10.0,  # watts
            scan_speed=500.0,  # mm/s
            layer_height=0.05,  # mm
            material="resin"
        )
        
        # Initialize
        if controller.initialize(config):
            return {
                "status": "INITIALIZED",
                "printer_type": laser_type.value,
                "build_area": {
                    "x": f"{config.build_area_x}mm",
                    "y": f"{config.build_area_y}mm",
                    "z": f"{config.build_area_z}mm"
                },
                "resolution": f"{config.resolution} micrometers",
                "laser_power": f"{config.laser_power}W",
                "material": config.material,
                "ready": True
            }
        else:
            return {"status": "INITIALIZATION_FAILED"}

    def prepare_3d_print_job(self, shape_type: str = "cube", 
                            strategy: str = "raster") -> Dict[str, Any]:
        """
        ADVANCED: Prepare 3D laser print job.
        
        Args:
            shape_type: Type of shape to print
            strategy: Scan strategy ("raster", "spiral", "vector")
            
        Returns:
            Dictionary with print job details
        """
        # Initialize printer if not done
        printer_info = self.initialize_laser_printer("SLA")
        if printer_info["status"] != "INITIALIZED":
            return {"error": "Failed to initialize printer"}
        
        # Create shape
        if shape_type.lower() == "cube":
            shape = Shape3DFactory.cube(20.0)
        elif shape_type.lower() == "sphere":
            shape = Shape3DFactory.sphere(20.0)
        elif shape_type.lower() == "pyramid":
            shape = Shape3DFactory.pyramid(20.0, 30.0)
        elif shape_type.lower() == "bloch":
            shape = Shape3DFactory.bloch_sphere()
        else:
            shape = Shape3DFactory.cube(20.0)
        
        # Create printer controller
        controller = LaserPrinterController(LaserPrinterType.STEREOLITHOGRAPHY)
        config = LaserConfig(
            printer_type=LaserPrinterType.STEREOLITHOGRAPHY,
            build_area_x=100.0,
            build_area_y=100.0,
            build_area_z=150.0,
            resolution=25.0,
            laser_power=10.0,
            scan_speed=500.0,
            layer_height=0.05,
            material="resin"
        )
        controller.initialize(config)
        
        # Create and prepare job
        job = controller.create_job(shape, strategy)
        if job and controller.submit_job(job):
            job_info = job.get_job_info()
            return {
                "job_created": True,
                "shape_type": shape_type,
                "strategy": strategy,
                "status": job_info["status"],
                "num_layers": job_info["num_layers"],
                "material_needed": job_info["material_needed"],
                "estimated_time": job_info["estimated_time"],
                "laser_power": job_info["laser_power"],
                "resolution": job_info["resolution"]
            }
        else:
            return {"error": "Failed to create or submit print job"}

    def simulate_3d_print(self, shape_type: str = "cube") -> Dict[str, Any]:
        """
        ADVANCED: Simulate 3D laser print process.
        
        Args:
            shape_type: Type of shape to simulate printing
            
        Returns:
            Dictionary with simulation results
        """
        # Create shape
        if shape_type.lower() == "cube":
            shape = Shape3DFactory.cube(15.0)
        elif shape_type.lower() == "sphere":
            shape = Shape3DFactory.sphere(15.0)
        else:
            shape = Shape3DFactory.cube(15.0)
        
        # Create printer and job
        controller = LaserPrinterController(LaserPrinterType.STEREOLITHOGRAPHY)
        config = LaserConfig(
            printer_type=LaserPrinterType.STEREOLITHOGRAPHY,
            build_area_x=100.0,
            build_area_y=100.0,
            build_area_z=150.0,
            resolution=25.0,
            laser_power=10.0,
            scan_speed=500.0,
            layer_height=0.05,
            material="resin"
        )
        controller.initialize(config)
        
        job = controller.create_job(shape, "raster")
        if job and controller.submit_job(job):
            results = job.simulate_print()
            
            return {
                "simulation": "COMPLETED",
                "shape_type": shape_type,
                "total_layers": len(results),
                "estimated_total_time": job.format_time(job.estimate_time()),
                "material_needed": f"{job.calculate_material():.2f}g",
                "layer_samples": results[:3],
                "final_layer": results[-1] if results else None
            }
        else:
            return {"error": "Simulation failed"}

    def export_print_to_gcode(self, shape_type: str = "cube") -> Dict[str, Any]:
        """
        ADVANCED: Export print job as GCode for laser printer.
        
        Args:
            shape_type: Type of shape to export
            
        Returns:
            Dictionary with GCode and metadata
        """
        # Create shape
        if shape_type.lower() == "cube":
            shape = Shape3DFactory.cube(15.0)
        else:
            shape = Shape3DFactory.cube(15.0)
        
        # Create printer and job
        controller = LaserPrinterController(LaserPrinterType.STEREOLITHOGRAPHY)
        config = LaserConfig(
            printer_type=LaserPrinterType.STEREOLITHOGRAPHY,
            build_area_x=100.0,
            build_area_y=100.0,
            build_area_z=150.0,
            resolution=25.0,
            laser_power=10.0,
            scan_speed=500.0,
            layer_height=0.05,
            material="resin"
        )
        controller.initialize(config)
        
        job = controller.create_job(shape, "raster")
        if job and controller.submit_job(job):
            gcode = controller.export_gcode(job)
            
            return {
                "export_format": "GCode",
                "shape_type": shape_type,
                "gcode_lines": len(gcode.split("\n")),
                "file_size": len(gcode),
                "first_lines": "\n".join(gcode.split("\n")[:10]),
                "material": config.material,
                "laser_power": f"{config.laser_power}W"
            }
        else:
            return {"error": "GCode export failed"}

    # ========== LOCKED VAULT METHODS ==========
    
    def vault_store_secret(self, key: str, value: Any, access_level: str = "internal",
                          ttl_seconds: Optional[int] = None, tags: Optional[List[str]] = None) -> bool:
        """
        Store a secret in the locked vault.
        
        Args:
            key: Unique identifier for the secret
            value: Secret data to store
            access_level: Security level ("public", "internal", "confidential", "restricted")
            ttl_seconds: Time-to-live in seconds (None = no expiration)
            tags: Tags for organizing secrets
            
        Returns:
            True if stored successfully
        """
        level_map = {
            "public": AccessLevel.PUBLIC,
            "internal": AccessLevel.INTERNAL,
            "confidential": AccessLevel.CONFIDENTIAL,
            "restricted": AccessLevel.RESTRICTED
        }
        
        access = level_map.get(access_level.lower(), AccessLevel.INTERNAL)
        
        success = self.vault.store_secret(
            password=self._vault_password,
            key=key,
            value=value,
            access_level=access,
            ttl_seconds=ttl_seconds,
            tags=tags
        )
        
        # Log to black box
        self.blackbox.log_event(
            event_type="vault_operation",
            message=f"Secret stored: {key}",
            actor="Guardian",
            action="vault_store",
            severity=EventSeverity.INFO,
            data={"key": key, "access_level": access.value, "tags": tags or []},
            result="success" if success else "failure"
        )
        
        self._operation_count += 1
        return success
    
    def vault_retrieve_secret(self, key: str) -> Optional[Any]:
        """
        Retrieve a secret from the locked vault.
        
        Args:
            key: Key of the secret to retrieve
            
        Returns:
            The secret value if found, None otherwise
        """
        secret = self.vault.retrieve_secret(self._vault_password, key)
        
        # Log to black box
        self.blackbox.log_event(
            event_type="vault_operation",
            message=f"Secret retrieved: {key}",
            actor="Guardian",
            action="vault_retrieve",
            severity=EventSeverity.INFO,
            data={"key": key},
            result="success" if secret is not None else "failure"
        )
        
        self._operation_count += 1
        return secret
    
    def vault_delete_secret(self, key: str) -> bool:
        """
        Delete a secret from the locked vault.
        
        Args:
            key: Key of the secret to delete
            
        Returns:
            True if deleted successfully
        """
        success = self.vault.delete_secret(self._vault_password, key)
        
        # Log to black box
        self.blackbox.log_event(
            event_type="vault_operation",
            message=f"Secret deleted: {key}",
            actor="Guardian",
            action="vault_delete",
            severity=EventSeverity.WARNING,
            data={"key": key},
            result="success" if success else "failure"
        )
        
        self._operation_count += 1
        return success
    
    def vault_list_secrets(self, access_level: Optional[str] = None) -> List[str]:
        """
        List all secret keys in the vault.
        
        Args:
            access_level: Filter by access level (optional)
            
        Returns:
            List of secret keys
        """
        level_map = {
            "public": AccessLevel.PUBLIC,
            "internal": AccessLevel.INTERNAL,
            "confidential": AccessLevel.CONFIDENTIAL,
            "restricted": AccessLevel.RESTRICTED
        }
        
        access = level_map.get(access_level.lower()) if access_level else None
        
        keys = self.vault.list_secrets(self._vault_password, access)
        
        # Log to black box
        self.blackbox.log_event(
            event_type="vault_operation",
            message=f"Secrets listed: {len(keys)} keys",
            actor="Guardian",
            action="vault_list",
            severity=EventSeverity.DEBUG,
            data={"count": len(keys), "filter": access_level},
            result="success"
        )
        
        return keys
    
    def vault_search_by_tags(self, tags: List[str]) -> List[str]:
        """
        Search for secrets by tags.
        
        Args:
            tags: List of tags to search for
            
        Returns:
            List of matching secret keys
        """
        keys = self.vault.search_secrets(self._vault_password, tags)
        
        # Log to black box
        self.blackbox.log_event(
            event_type="vault_operation",
            message=f"Secrets searched by tags: found {len(keys)}",
            actor="Guardian",
            action="vault_search",
            severity=EventSeverity.DEBUG,
            data={"tags": tags, "results": len(keys)},
            result="success"
        )
        
        return keys
    
    def vault_get_statistics(self) -> Optional[Dict[str, Any]]:
        """Get vault statistics and status."""
        stats = self.vault.get_vault_stats(self._vault_password)
        
        if stats:
            self.blackbox.log_event(
                event_type="vault_operation",
                message="Vault statistics retrieved",
                actor="Guardian",
                action="vault_stats",
                severity=EventSeverity.DEBUG,
                data=stats,
                result="success"
            )
        
        return stats
    
    # ========== BLACK BOX METHODS ==========
    
    def blackbox_log_event(self, event_type: str, message: str, action: str,
                          severity: str = "info", data: Optional[Dict] = None) -> str:
        """
        Log an event in the black box.
        
        Args:
            event_type: Type of event
            message: Human-readable message
            action: What action was performed
            severity: Severity level ("critical", "warning", "info", "debug")
            data: Additional event data
            
        Returns:
            Event ID for tracking
        """
        severity_map = {
            "critical": EventSeverity.CRITICAL,
            "warning": EventSeverity.WARNING,
            "info": EventSeverity.INFO,
            "debug": EventSeverity.DEBUG
        }
        
        sev = severity_map.get(severity.lower(), EventSeverity.INFO)
        
        event_id = self.blackbox.log_event(
            event_type=event_type,
            message=message,
            actor="Guardian",
            action=action,
            severity=sev,
            data=data or {}
        )
        
        self._operation_count += 1
        return event_id
    
    def blackbox_query_events(self, event_type: Optional[str] = None,
                             actor: Optional[str] = None,
                             severity: Optional[str] = None,
                             limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Query events from the black box.
        
        Args:
            event_type: Filter by event type
            actor: Filter by actor
            severity: Filter by severity
            limit: Maximum number of results
            
        Returns:
            List of matching events
        """
        severity_map = {
            "critical": EventSeverity.CRITICAL,
            "warning": EventSeverity.WARNING,
            "info": EventSeverity.INFO,
            "debug": EventSeverity.DEBUG
        }
        
        sev = severity_map.get(severity.lower()) if severity else None
        
        events = self.blackbox.query_events(
            event_type=event_type,
            actor=actor,
            severity=sev,
            limit=limit
        )
        
        return [e.to_dict() for e in events]
    
    def blackbox_get_statistics(self) -> Dict[str, Any]:
        """Get black box statistics and analysis."""
        return self.blackbox.get_statistics()
    
    def blackbox_export_log(self, format: str = "json") -> str:
        """
        Export black box log in specified format.
        
        Args:
            format: Export format ("json", "csv", "text")
            
        Returns:
            Exported log as string
        """
        return self.blackbox.export_events(format)
    
    def blackbox_get_operation_count(self) -> int:
        """Get total number of operations performed by Guardian."""
        return self._operation_count


# Import quantum components after class definition to avoid circular imports
from quantum_computing_engine import QuantumBit, QuantumGates