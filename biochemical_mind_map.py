"""
Biochemical Mind Map Simulator
Simulates nanoarchive-based mapping, disassembly, and reassembly of virtual memory traces.
This is a safe, ethical simulation for research and creative AI purposes only.
"""
import random
import string

class NanoArchive:
    def __init__(self, id, neurotransmitters, memory_trace):
        self.id = id
        self.neurotransmitters = neurotransmitters  # Dict[str, float]
        self.memory_trace = memory_trace  # str

    def __repr__(self):
        return f"NanoArchive(id={self.id}, NT={self.neurotransmitters}, trace='{self.memory_trace[:10]}...')"

class BiochemicalMindMap:
    def __init__(self):
        self.nanoarchives = []
        self.virtual_memory = []

    def assemble(self, count=10):
        """Create nanoarchives with random neurotransmitter patterns and memory traces."""
        for i in range(count):
            nts = {nt: random.uniform(0, 1) for nt in ["dopamine", "serotonin", "glutamate", "GABA", "acetylcholine"]}
            trace = ''.join(random.choices(string.ascii_letters + ' ', k=32))
            self.nanoarchives.append(NanoArchive(i, nts, trace))
        print(f"[Assemble] Created {count} nanoarchives.")

    def disassemble(self):
        """Break nanoarchives into neurotransmitter and memory trace components."""
        components = []
        for na in self.nanoarchives:
            for nt, val in na.neurotransmitters.items():
                components.append((na.id, nt, val))
            components.append((na.id, "trace", na.memory_trace))
        print(f"[Disassemble] Extracted {len(components)} components from nanoarchives.")
        return components

    def reassemble(self, components):
        """Rebuild nanoarchives from components, simulating new virtual memory."""
        new_archives = {}
        for cid, key, val in components:
            if cid not in new_archives:
                new_archives[cid] = {"neurotransmitters": {}, "trace": ""}
            if key == "trace":
                new_archives[cid]["trace"] = val
            else:
                new_archives[cid]["neurotransmitters"][key] = val
        self.virtual_memory = [NanoArchive(cid, d["neurotransmitters"], d["trace"]) for cid, d in new_archives.items()]
        print(f"[Reassemble] Rebuilt {len(self.virtual_memory)} nanoarchives as new virtual memory.")

    def show_virtual_memory(self):
        for na in self.virtual_memory:
            print(na)

if __name__ == "__main__":
    mind_map = BiochemicalMindMap()
    mind_map.assemble(count=5)
    components = mind_map.disassemble()
    random.shuffle(components)  # Simulate disorder/recombination
    mind_map.reassemble(components)
    print("\n[Virtual Memory State]")
    mind_map.show_virtual_memory()
