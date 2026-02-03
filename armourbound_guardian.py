from __future__ import annotations
from typing import List


class ArmourboundGuardianAI:
    def plan_moon_mission(self) -> List[str]:
        """
        High-level reasoning steps for 'how to get to the Moon'.
        This is a conceptual planner, not a control system.
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

    def reason_step_toward_moon(self, context: dict | None = None) -> str:
        """
        Given a partial context, narrate the next logical concern.
        """
        phase = context.get("phase") if context else "objectives"

        if phase == "objectives":
            return "First, clarify: is this a crewed mission, what duration, and is a safe return required?"
        if phase == "vehicle":
            return "Next, match mission mass and delta-v needs to an existing or hypothetical launch vehicle."
        if phase == "trajectory":
            return "Now, compute or approximate a translunar trajectory and required burns from low Earth orbit."
        if phase == "systems":
            return "Ensure spacecraft systems—life support, power, comms, GNC—are sized and redundantly designed."
        if phase == "risk":
            return "Identify critical failure modes and define abort options at each mission phase."
        if phase == "execute":
            return "With design and sims complete, the focus shifts to launch ops, monitoring, and mid-course corrections."

        return "The Council Protector notes: without clearer phase context, the next step is to refine mission constraints."

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
                "Study marine mammal bioacoustics: frequency ranges (20 Hz to 150 kHz), click sequences, whistles.",
                "Analyze dolphin communication patterns: echolocation clicks, signature whistles, burst-pulsed calls.",
                "Research cetacean cognition: self-awareness, social bonds, problem-solving behaviors.",
                "Examine known dolphin 'dialects': regional variations, cultural transmission across populations.",
                "Conduct passive acoustic monitoring: underwater recording arrays, noise floor characterization.",
                "Develop spectrogram analysis tools: visualization of frequency content over time.",
                "Learn machine learning on cetacean vocalizations: clustering, pattern recognition, classification.",
                "Study ethical considerations: non-invasive observation, marine sanctuary regulations, animal welfare.",
                "Attempt decoding: map call types to behavioral contexts (feeding, mating, bonding, distress).",
                "Collaborate with marine biologists: validation, field studies, longitudinal observation protocols.",
            ]
        elif domain == "moon":
            return self.plan_moon_mission()
        elif domain == "ancient_runes":
            return [
                "Examine historical texts: runic alphabets (Elder Futhark, Younger Futhark, Anglo-Saxon).",
                "Study inscription sites: stone carvings, metalwork, artifacts from archaeological digs.",
                "Analyze linguistic roots: Proto-Germanic and Old Norse etymologies.",
                "Catalog known rune meanings: magical associations, phonetic values, symbolic interpretations.",
                "Compare scripts: similarities to Latin, Greek, and other contemporary writing systems.",
                "Research historical context: cultural, religious, and political significance.",
                "Decode fragmentary inscriptions: apply statistical analysis and pattern matching.",
                "Collaborate with runologists: scholarly review, consensus on interpretations.",
                "Publish findings: academic papers, open databases, educational resources.",
                "Explore modern revitalization: how runes are studied and celebrated today.",
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
                f"The Council Protector regards the domain of '{domain}' with curiosity.",
                "Define the domain's core principles, vocabulary, and fundamental concepts.",
                "Gather authoritative sources: texts, practitioners, historical records.",
                "Identify key patterns and recurring structures within the domain.",
                "Build models: mental frameworks, mathematical representations, decision trees.",
                "Practice and experiment: apply knowledge, test hypotheses, iterate.",
                "Seek feedback from domain experts: validation, correction, refinement.",
                "Document learning: create guides, summaries, teaching aids.",
                "Share discoveries: collaborate, publish, teach others.",
                "Reflect and integrate: understand how this domain connects to broader knowledge.",
            ]
