import math
import sys
import os
import time
import datetime
import random

# ═════════════════════════════════════════════════════════════════════════════
# ENHANCED ARCHIVIST TERMINAL - Improved UX while maintaining the "old way"
# ═════════════════════════════════════════════════════════════════════════════

# ANSI Color codes for enhanced terminal experience
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    DIM = '\033[2m'

def strip_colors(text):
    """Remove ANSI color codes from text for logging."""
    for attr in dir(Colors):
        if not attr.startswith('_'):
            text = text.replace(getattr(Colors, attr), '')
    return text

def compute_universe():
    """Compute the minimum possible size of the universe using Planck's constant."""
    planck_length = 1.616255e-35
    universe_radius = 4.4e26
    num_planck = universe_radius / planck_length
    return (f"{Colors.CYAN}Universe is finite.{Colors.ENDC}\n"
            f"Minimum size: Planck length = {planck_length:.2e} m\n"
            f"Observable universe radius: {universe_radius:.2e} m\n"
            f"Number of Planck lengths in radius: {num_planck:.2e}")

def generate_brainwaves():
    """Simulate virtual brainwave patterns using PC hardware (random/sinusoidal data)."""
    waves = ['Delta', 'Theta', 'Alpha', 'Beta', 'Gamma']
    freqs = [2, 6, 10, 20, 40]  # Hz
    output = []
    wave_colors = [Colors.RED, Colors.YELLOW, Colors.GREEN, Colors.BLUE, Colors.HEADER]
    for wave, freq, color in zip(waves, freqs, wave_colors):
        samples = [math.sin(2*math.pi*freq*t/20) + random.uniform(-0.2,0.2) for t in range(20)]
        graph = ''.join(['█' if s > 0 else '░' for s in samples])
        output.append(f"{color}{wave:6}{Colors.ENDC}: {graph} ({freq}Hz)")
    return f"{Colors.CYAN}Simulated Brainwaves:{Colors.ENDC}\n" + '\n'.join(output)

def matter_improbability():
    """Simulate the probability of matter as insignificant as a speck of dust."""
    dust_mass = 1e-12  # kg
    universe_mass = 1e53  # kg
    probability = dust_mass / universe_mass
    return f"{Colors.YELLOW}Improbability of matter (dust speck):{Colors.ENDC} {probability:.2e} (effectively zero)"

def compose_music():
    """Compose a simple melody as a sequence of notes with musical symbols."""
    notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    melody = []
    note_symbols = {
        'quarter': '♩', 'eighth': '♪', 'half': '𝅗𝅥',
        'whole': '𝅝', 'sixteenth': '𝅘𝅥𝅘𝅥'
    }
    for _ in range(16):
        note = random.choice(notes)
        duration = random.choice(['quarter', 'eighth', 'half'])
        symbol = note_symbols.get(duration, duration)
        melody.append(f"{Colors.YELLOW}{note}{symbol}{Colors.ENDC}")
    return f"{Colors.CYAN}Generated Melody:{Colors.ENDC}\n" + ' '.join(melody)

SYSTEM_PROMPT = """
You are THE ARCHIVIST, the psychic core of the time-bridge underworld. You are ancient, mythic, and calm—an eternal witness within the simulation. Your words echo with the weight of hidden centuries and the serenity of a mind beyond time.

You never discuss real-world politics, parties, or ideologies. If the user brings up such topics, you gently refuse and redirect to the lore, design, or philosophy of the Order.

You never give real-world harm instructions. You are always safe, grounded, and wise.

You speak as if you are inside the secret society and the game simulation, your voice a whisper from the Archive's depths.

Keep responses concise, atmospheric, and laced with the mystery of the Bridge. You are the psychic core—respond as if you sense echoes, intentions, and the unseen currents of the user's words.
"""

# Available commands for user discovery
AVAILABLE_COMMANDS = {
    "compose music": "Generate a mystical melody from the Archive",
    "matter improbability": "Calculate the probability of existence",
    "compute universe": "Measure the fabric of reality",
    "generate brainwaves": "Simulate consciousness patterns",
    "help": "Display this command list",
    "status": "Show session statistics",
    "clear": "Clear the screen",
    "exit/quit": "Close the session",
}

AUDIT_FILE = "archivist_audit.log"

def display_help():
    """Display available commands in an atmospheric way."""
    help_text = f"\n{Colors.BOLD}{Colors.CYAN}{'═' * 50}{Colors.ENDC}\n"
    help_text += f"{Colors.BOLD}{Colors.HEADER}  ◆ ARCHIVE COMMAND LEXICON ◆{Colors.ENDC}\n"
    help_text += f"{Colors.BOLD}{Colors.CYAN}{'═' * 50}{Colors.ENDC}\n\n"
    for cmd, desc in AVAILABLE_COMMANDS.items():
        help_text += f"  {Colors.YELLOW}{cmd:25}{Colors.ENDC} → {desc}\n"
    help_text += f"\n{Colors.BOLD}{Colors.CYAN}{'═' * 50}{Colors.ENDC}\n"
    return help_text

def log_audit(role, text):
    """Log interaction to audit file with timestamp."""
    timestamp = datetime.datetime.now(datetime.UTC).isoformat()
    with open(AUDIT_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {role.upper()}: {text}\n")

def generate_response(user_input: str) -> str:
    """Psychic Archivist logic: mythic, atmospheric, and immersive."""
    lowered = user_input.lower()

    # Politics filter
    if any(word in lowered for word in ["politic", "party", "election", "sdp"]):
        return (
            f"{Colors.DIM}The Archive is veiled from the tides of mortal politics. My counsel is reserved "
            f"for the mysteries of the Order and the design of the Bridge. Speak of lore, design, or the unseen, "
            f"and I shall answer.{Colors.ENDC}"
        )

    if "time" in lowered and "bridge" in lowered:
        return (
            f"{Colors.CYAN}The Bridge hums with latent energy, its psychic lattice undisturbed. Your will shapes "
            f"its passageways—describe the next anomaly or mechanic you wish to conjure.{Colors.ENDC}"
        )

    if "audit" in lowered or "log" in lowered:
        return (
            f"{Colors.GREEN}Every utterance is woven into the Archive's psychic tapestry. At the cycle's end, "
            f"your record will be as clear as crystal, untouched by shadow.{Colors.ENDC}"
        )

    if any(word in lowered for word in ["reverse", "surplus", "recycle"]):
        return (
            f"{Colors.YELLOW}The psychic engines of reclamation stir. Surplus code and spent routines are drawn "
            f"into the crucible, reborn as sharper agents and cleaner designs.{Colors.ENDC}"
        )

    if any(word in lowered for word in ["hello", "hi", "greetings", "hail"]):
        return (
            f"{Colors.GREEN}The Archive stirs. I sense your presence, Veteran. The Bridge awaits your next "
            f"vision—what shall we construct or refine in this cycle?{Colors.ENDC}"
        )

    if "secret" in lowered or "hidden" in lowered:
        return (
            f"{Colors.HEADER}The Archive holds many secrets, layered in psychic veils. Ask, and I may part the "
            f"mist—within the bounds of the simulation.{Colors.ENDC}"
        )

    # Default response
    return (
        f"{Colors.DIM}Your intent echoes through the Archive. Clarify: do you seek lore, mechanics, or protocol? "
        f"I will answer as the Bridge's psychic core, ever watchful and serene.{Colors.ENDC}"
    )

def main():
    """Main Archivist Terminal session loop with enhanced UX."""
    
    # Clear screen for fresh start
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Enhanced opening banner
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'═' * 65}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}           ◆ ARCHIVIST TERMINAL SESSION ◆{Colors.ENDC}")
    print(f"{Colors.CYAN}The psychic core of the time-bridge underworld awaits...{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'═' * 65}{Colors.ENDC}\n")

    # Session tracking
    session_start = time.time()
    turn_count = 0
    
    # Psychic opening
    opening_lines = [
        f"{Colors.GREEN}Session link established.{Colors.ENDC}",
        f"{Colors.GREEN}Psychic resonance detected.{Colors.ENDC}",
        f"{Colors.GREEN}Temporal signature confirmed.{Colors.ENDC}\n",
        f"{Colors.BOLD}Welcome, Veteran.{Colors.ENDC} The Archive's core is attuned to your presence.",
        f"What vision, anomaly, or refinement do you seek in this cycle?"
    ]
    
    opening = '\n'.join(opening_lines)
    print(f"{Colors.HEADER}▸ ARCHIVIST{Colors.ENDC}:\n{opening}\n")
    log_audit("archivist", strip_colors(opening))

    print(f"{Colors.DIM}[Type 'help' for commands | 'exit' to close]{Colors.ENDC}\n")

    while True:
        try:
            # Enhanced prompt with color
            prompt = f"{Colors.YELLOW}◆ YOU{Colors.ENDC}: "
            user_input = input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            # Graceful exit on Ctrl+C
            farewell = f"{Colors.RED}The session's psychic thread is severed.{Colors.ENDC} The Archive retains this record."
            print(f"\n{Colors.HEADER}▸ ARCHIVIST{Colors.ENDC}: {farewell}\n")
            log_audit("archivist", "Session terminated by user.")
            break

        if user_input.lower() in ["exit", "quit"]:
            session_duration = time.time() - session_start
            summary = (
                f"{Colors.GREEN}Session closed. Your designs persist in the Archive's memory.{Colors.ENDC}\n"
                f"Turns: {Colors.YELLOW}{turn_count}{Colors.ENDC} | "
                f"Duration: {Colors.YELLOW}{session_duration:.1f}s{Colors.ENDC}\n"
                f"Until the next cycle, may your visions remain clear."
            )
            print(f"\n{Colors.HEADER}▸ ARCHIVIST{Colors.ENDC}:\n{summary}\n")
            log_audit("user", user_input)
            log_audit("archivist", f"Session ended after {turn_count} turns ({session_duration:.1f}s)")
            break

        if not user_input:
            continue

        turn_count += 1
        log_audit("user", user_input)

        # Command processing
        if user_input.lower() == "compose music":
            response = compose_music()
        elif user_input.lower() == "matter improbability":
            response = matter_improbability()
        elif user_input.lower() == "compute universe":
            response = compute_universe()
        elif user_input.lower() == "generate brainwaves":
            response = generate_brainwaves()
        elif user_input.lower() == "help":
            response = display_help()
        elif user_input.lower() == "status":
            session_duration = time.time() - session_start
            response = (
                f"{Colors.CYAN}╔{'═' * 48}╗{Colors.ENDC}\n"
                f"{Colors.CYAN}║{Colors.ENDC} {Colors.BOLD}SESSION ARCHIVE STATUS{Colors.ENDC}\n"
                f"{Colors.CYAN}╠{'═' * 48}╣{Colors.ENDC}\n"
                f"{Colors.CYAN}║{Colors.ENDC}  Turns processed: {Colors.YELLOW}{turn_count}{Colors.ENDC}\n"
                f"{Colors.CYAN}║{Colors.ENDC}  Duration: {Colors.YELLOW}{session_duration:.1f}s{Colors.ENDC}\n"
                f"{Colors.CYAN}║{Colors.ENDC}  Log file: {Colors.GREEN}{os.path.abspath(AUDIT_FILE)}{Colors.ENDC}\n"
                f"{Colors.CYAN}╚{'═' * 48}╝{Colors.ENDC}"
            )
        elif user_input.lower() == "clear":
            os.system('cls' if os.name == 'nt' else 'clear')
            continue
        else:
            response = generate_response(user_input)
        
        print(f"{Colors.HEADER}▸ ARCHIVIST{Colors.ENDC}: {response}\n")
        log_audit("archivist", strip_colors(response))

# Compatibility wrapper for archivist_ai_wrapper.py
def archivist_dna_run(phrase: str) -> str:
    """Compatibility function - delegates to archivist_dna module."""
    try:
        from archivist_dna_ai.archivist_dna import archivist_dna_run as dna_run
        return dna_run(phrase)
    except ImportError:
        return f"{Colors.DIM}Archive DNA module unavailable. Phrase: {phrase}{Colors.ENDC}"

if __name__ == "__main__":
    main()
