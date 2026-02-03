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
