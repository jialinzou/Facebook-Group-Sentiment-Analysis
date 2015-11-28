import us

# yelp_extractor_settings.py contains all the settings the yelp_extractor.py requires

# Get all the states in US by mapping us.states.States which gives an array of object
# and can call .name to get the name of the state
states_of_us = map(lambda x : x.name, us.states.STATES)

# The number of states
num_of_states = len(states_of_us)

# The number of businesses we should get
num_businesses = 20