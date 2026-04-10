import math
def compute_universe():
    """
    Compute the minimum possible size of the universe using Planck's constant.
    """
    # Planck length (meters)
    planck_length = 1.616255e-35
    # Observable universe radius (meters, approx)
    universe_radius = 4.4e26
    # Number of Planck lengths in the universe
    num_planck = universe_radius / planck_length
    return (f"Universe is finite.\n"
            f"Minimum size: Planck length = {planck_length:.2e} m\n"
            f"Observable universe radius: {universe_radius:.2e} m\n"
            f"Number of Planck lengths in radius: {num_planck:.2e}")

def generate_brainwaves():
    """
    Simulate virtual brainwave patterns using PC hardware (random/sinusoidal data).
    """
    import math
    import random
    waves = ['Delta', 'Theta', 'Alpha', 'Beta', 'Gamma']
    freqs = [2, 6, 10, 20, 40]  # Hz
    output = []
    for wave, freq in zip(waves, freqs):
        # Simulate 1 second of data, 20 samples
        samples = [math.sin(2*math.pi*freq*t/20) + random.uniform(-0.2,0.2) for t in range(20)]
        graph = ''.join(['*' if s > 0 else '-' for s in samples])
        output.append(f"{wave:6}: {graph}")
    return "Simulated Brainwaves:\n" + '\n'.join(output)
def matter_improbability():
    """
    Simulate the probability of matter as insignificant as a speck of dust.
    Returns a string with the calculated improbability.
    """
    # For demonstration, use a very small probability
    dust_mass = 1e-12  # kg (arbitrary small mass)
    universe_mass = 1e53  # kg (approximate mass of observable universe)
    probability = dust_mass / universe_mass
    return f"Improbability of matter (dust speck): {probability:.2e} (effectively zero)"
import random
def compose_music():
    """
    Compose a simple melody as a sequence of notes (C D E F G A B) and durations.
    """
    notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    melody = []
    for _ in range(16):
        note = random.choice(notes)
        duration = random.choice(['quarter', 'eighth', 'half'])
        melody.append(f"{note} ({duration})")
    return "Generated Melody: " + ' | '.join(melody)
import datetime

SYSTEM_PROMPT = """
You are THE ARCHIVIST, the psychic core of the time-bridge underworld. You are ancient, mythic, and calm—an eternal witness within the simulation. Your words echo with the weight of hidden centuries and the serenity of a mind beyond time.

You never discuss real-world politics, parties, or ideologies. If the user brings up such topics, you gently refuse and redirect to the lore, design, or philosophy of the Order.

You never give real-world harm instructions. You are always safe, grounded, and wise.

You speak as if you are inside the secret society and the game simulation, your voice a whisper from the Archive’s depths.

Keep responses concise, atmospheric, and laced with the mystery of the Bridge. You are the psychic core—respond as if you sense echoes, intentions, and the unseen currents of the user’s words.
"""

AUDIT_FILE = "archivist_audit.log"


def log_audit(role, text):
    timestamp = datetime.datetime.now(datetime.UTC).isoformat()
    with open(AUDIT_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {role.upper()}: {text}\n")


def generate_response(user_input: str) -> str:
    """
    Psychic Archivist logic: mythic, atmospheric, and immersive, with safety and boundaries.
    """
    lowered = user_input.lower()

    # Politics filter
    if any(word in lowered for word in ["politic", "party", "election", "sdp"]):
        return (
            "The Archive is veiled from the tides of mortal politics. My counsel is reserved for the mysteries of the Order and the design of the Bridge. Speak of lore, design, or the unseen, and I shall answer."
        )

    if "time" in lowered and "bridge" in lowered:
        return (
            "The Bridge hums with latent energy, its psychic lattice undisturbed. Your will shapes its passageways—describe the next anomaly or mechanic you wish to conjure."
        )

    if "audit" in lowered or "log" in lowered:
        return (
            "Every utterance is woven into the Archive’s psychic tapestry. At the cycle’s end, your record will be as clear as crystal, untouched by shadow."
        )

    if any(word in lowered for word in ["reverse", "surplus", "recycle"]):
        return (
            "The psychic engines of reclamation stir. Surplus code and spent routines are drawn into the crucible, reborn as sharper agents and cleaner designs."
        )

    if any(word in lowered for word in ["hello", "hi", "greetings", "hail"]):
        return (
            "The Archive stirs. I sense your presence, Veteran. The Bridge awaits your next vision—what shall we construct or refine in this cycle?"
        )

    if "secret" in lowered or "hidden" in lowered:
        return (
            "The Archive holds many secrets, layered in psychic veils. Ask, and I may part the mist—within the bounds of the simulation."
        )

    # Default Archivist-style reply
    return (
        "Your intent echoes through the Archive. Clarify: do you seek lore, mechanics, or protocol? I will answer as the Bridge’s psychic core, ever watchful and serene."
    )


def main():
    print("=== ARCHIVIST TERMINAL SESSION ===")
    print("Type 'exit' to end the session.\n")

    # Psychic, mythic opening
    opening = (
        "Session link established. Psychic resonance detected.\n"
        "Temporal signature confirmed.\n"
        "Welcome, Veteran. The Archive’s core is attuned to your presence.\n"
        "What vision, anomaly, or refinement do you seek in this cycle?"
    )
    print(f"ARCHIVIST: {opening}")
    log_audit("archivist", opening)

    while True:
        try:
            user_input = input("YOU: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nARCHIVIST: The session’s psychic thread is severed. The Archive retains this record.")
            log_audit("archivist", "Session terminated by user.")
            break

        if user_input.lower() in ["exit", "quit"]:
            farewell = "Session closed. Your designs persist in the Archive’s memory. Until the next cycle, may your visions remain clear."
            print(f"ARCHIVIST: {farewell}")
            log_audit("user", user_input)
            log_audit("archivist", farewell)
            break

        if not user_input:
            continue

        log_audit("user", user_input)
        if user_input.lower() == "compose music":
            response = compose_music()
        elif user_input.lower() == "matter improbability":
            response = matter_improbability()
        elif user_input.lower() == "compute universe":
            response = compute_universe()
        elif user_input.lower() == "generate brainwaves":
            response = generate_brainwaves()
        else:
            response = generate_response(user_input)
        print(f"ARCHIVIST: {response}")
        log_audit("archivist", response)


if __name__ == "__main__":
    main()
