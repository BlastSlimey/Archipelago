# Pokémon BW Plugin Template

When making a plugin, the apworld (and the folder inside like with all apworlds) need to be named "pokemon_bw_[...]" so that the main apworld can actually detect them.
The best way to use this template is by setting up a local AP repo (like you would do for developing "normal" apworlds) and putting the plugin as well as the pokemon_bw aworld next to the other worlds.
The explanations in here and in the other files don't expect the reader to be an expert in Python.
When you're done writing the plugin, just run the __init__.py script file with Python (you can probably just double-click it) and it will pack the folder into an apworld next to it and with the same name.

The archipelago.json file inside is needed for when AP 0.7.0 releases at some point, else the whole apworld will just be rejected.
However, if you pack the apworld by running the __init__.py script, the file will be ignored and a file with the correct information gets put into the apworld instead.

The __init__.py file is the entry point and contains the code.
More info can be found inside.
