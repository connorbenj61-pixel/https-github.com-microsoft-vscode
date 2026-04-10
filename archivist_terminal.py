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
    timestamp = datetime.datetime.utcnow().isoformat()
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
        response = generate_response(user_input)
        print(f"ARCHIVIST: {response}")
        log_audit("archivist", response)


if __name__ == "__main__":
    main()
