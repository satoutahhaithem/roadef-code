import numpy as np

# Define problem parameters
conference_sessions = 5
slots = 2
papers_range = np.arange(1, 3)  # Range of papers per session
working_groups = 5

# Function to generate identifiers for x variables
# def var_x(s, c, l):
#     s_index = conference_sessions * slots * len(papers_range)
#     c_index = slots * len(papers_range)
#     l_index = len(papers_range)
#     # return s_index - (conference_sessions - s) * c_index - (slots - c) * l_index - (len(papers_range) - l)
#     return (s-1)*slots * len(papers_range)  + (c-1)*len(papers_range) + l

# Calculate the maximum identifier for x variables
# max_var_x = var_x(conference_sessions, slots, papers_range[-1])

# Function to generate identifiers for z variables
# def var_z(s, c):
#     z_offset = max_var_x   # Ensure z variables start after x variables
#     return z_offset + (s - 1) * slots + c
#     # return z_offset + conference_sessions*slots - (conference_sessions-s)*slots - (slots - c)
    

# Calculate the maximum identifier for z variables
# max_var_z = var_z(conference_sessions, slots)





def var_x(s, c, l):
    return (s-1)*slots * len(papers_range)  + (c-1)*len(papers_range) + l


######################################################################""
def decode_var_x(x, slots, papers_range_length):
    x -= 1  # Adjusting because the original function seems 1-indexed
    l = x % papers_range_length + 1
    x //= papers_range_length
    c = x % slots + 1
    s = x // slots + 1
    return s, c, l
#############################################################################

# def var_y(s1, s2, c, g):

#     s1_index = conference_sessions* conference_sessions * slots * working_groups
#     s2_index = conference_sessions * slots * working_groups
#     c_index =  slots * working_groups
#     g_index =  working_groups
#     return s1_index - (conference_sessions - s1) * s2_index - (conference_sessions - s2) * c_index - (slots - c) * g_index - (g_index - g)
    # # Calculating the total number of x variables
    # total_x_vars = conference_sessions * slots * len(papers_range)

    # # Calculating the total number of z variables
    # total_z_vars = conference_sessions * slots

    # # The offset for y variables should be total_x_vars + total_z_vars + 1
    # y_offset = total_x_vars + total_z_vars + 1

    # # Calculate the unique identifier for y variables
    # unique_index = ((s1 - 1) * conference_sessions + (s2 - 1)) * slots * working_groups + (c - 1) * working_groups + (g - 1)  
    # return y_offset + unique_index
# def var_y(s1, s2, c, g, max_sessions, max_slots, max_groups):
#     # Triangular mapping for s1 and s2 combination
#     s1_s2_index = (s2 - 1) * (s2 - 2) // 2 + s1 - 1

#     # Extending the mapping to include c and g
#     extended_index = s1_s2_index * max_slots * max_groups + (c - 1) * max_groups + g - 1

#     return extended_index

# Print examples for var_x, var_z, and var_y
for s in range(1, conference_sessions + 1):
    for c in range(1, slots + 1):
        for l in papers_range:
            print(f"var_x({s}, {c}, {l}): {var_x(s, c, l)}")
            s1, c1, l1 = decode_var_x(var_x(s, c, l),slots=slots,papers_range_length=len(papers_range))
            print(f"Decoded from {var_x(s, c, l)}: Session = {s1}, Slot = {c1}, Paper Range Index = {l1}")

        # print(f"var_z({s}, {c}): {var_z(s, c)}")

# Example usage

# for s1 in range(1, conference_sessions + 1):
#     for s2 in range(s1 + 1, conference_sessions + 1):
#         for c in range(1, slots + 1):
#             for g in range(1, working_groups + 1):
#                 print(f"var_y({s1}, {s2}, {c}, {g}): {var_y(s1, s2, c, g)}")
#                 if g == 1:  # Limit the output
#                     break
#             if c == 1:  # Limit the output
#                 break
#         if s2 == s1 + 1:  # Limit the output
#             break


# print(var_z(conference_sessions,slots))



# for s1 in range(1, conference_sessions + 1):
#     for s2 in range(s1 + 1, conference_sessions + 1):
#         for c in range(1, slots + 1):
#             for g in range(1, working_groups+ 1):
#                 print(f"var_y({s1}, {s2}, {c}, {g}): {var_y(s1, s2, c, g)}")
#                 if g == 2:  # Limiting output for demonstration
#                     break
#             if c == 2:  # Limiting output for demonstration
#                 break
#         if s2 == s1 + 2:  # Limiting output for demonstration
#             break
# print(var_y(1,2,1,1))
# print(var_y(1,3,1,1))
# print(var_y(1,4,1,1))
# print(var_y(1,5,1,1))
# print(var_y(1,5,2,1))
# print(var_y(1,5,2,1))
# print(var_y(1,5,2,1))
# print(var_y(2,3,1,1))
# print(var_y(2,4,1,1))
# print(var_y(2,5,1,1))











