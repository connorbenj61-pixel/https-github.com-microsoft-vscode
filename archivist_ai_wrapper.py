import archivist_terminal

class ArchivistAIWrapper:
    """
    Wrapper to run the Archivist DNA AI logic from other AI modules.
    """
    def __init__(self):
        pass

    def run_interactive(self):
        archivist_terminal.main()

    def evolve_phrase(self, phrase):
        return archivist_terminal.archivist_dna_run(phrase)
