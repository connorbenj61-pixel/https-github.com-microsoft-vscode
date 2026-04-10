from animus_ai import Animus

animus = Animus()

# Camouflage a file (e.g., animus_simian_system.sql)
input_file = 'animus_simian_system.sql'
camouflaged_file = 'animus_simian_system.sql.camouflaged'
revealed_file = 'animus_simian_system.sql.revealed'

animus.camouflage_file(input_file, camouflaged_file)
print(f"File camouflaged: {camouflaged_file}")

animus.reveal_file(camouflaged_file, revealed_file)
print(f"File revealed: {revealed_file}")

print(f"Animus AI IQ: {animus.get_iq()}")
