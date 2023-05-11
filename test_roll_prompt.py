import random
import json

godzilla_dict_f = open('./ai_app/godzilla.json')
godzilla_dict = json.load(godzilla_dict_f)
godzilla_dict_f.close()

monster_d = godzilla_dict['monster']
monster_l = list(monster_d.keys())
monster_w = [ monster_d[monster] for monster in monster_l ]
verb_d = godzilla_dict['verb']
verb_l = list(verb_d.keys())
verb_w = [ verb_d[verb]['w'] for verb in verb_l ]
style_d = godzilla_dict['style']
style_l = list(style_d.keys())
style_w = [ style_d[style] for style in style_l ]

# Get Words
verb = random.choices(verb_l, verb_w)[0]
monsters = random.choices(monster_l, monster_w, k=verb_d[verb]['max'])
style = random.choices(style_l, style_w)[0]
prompt = f"{monsters[0]} {verb} "
if len(monsters) > 1:
  prompt+=f"{' and '.join(monsters[1:])} "
prompt+=f"in the style of {style}."
print(prompt)