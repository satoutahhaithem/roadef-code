conference_sessions = 4
slots = 3
max_var_x = 100  

def var_z(s, c):
    z_offset = max_var_x + 1
    return z_offset + (s - 1) * slots + c


for s in range(1, conference_sessions + 1):
    for c in range(1, slots + 1):
        print(f"Identifier for session {s}, slot {c}: {var_z(s, c)}")
