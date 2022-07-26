import argparse
import json
import random
import sys


SITREP_REQUIREMENTS = {
    'recon': {
        'budget_multiplier': 1,
        'instructions': 'Deploy all forces at the beginning of the encounter, or hold some in reserves.'
    },
    'control': {
        'budget_multiplier': 1,
        'instructions': 'Deploy all forces at the beginning of the encounter. No reserves.'
    },
    'escort': {
        'budget_multiplier': 2,
        'instructions': 'Deploy half of your forces at the beginning of the encounter, and hold the rest as reserves for later rounds.'
    },
    'extraction': {
        'budget_multiplier': 2,
        'instructions': 'Deploy no forces at the beginning of the encounter. All forces shoudl be deployed in later rounds as reserves.'
    },
    'gauntlet': {
        'budget_multiplier': 1,
        'instructions': 'Deploy half of your forces at the beginning of the encounter, and hold the rest as reserves for later rounds.'
    },
    'holdout': {
        'budget_multiplier': 2,
        'instructions': 'Deploy half of your forces at the beginning of the encounter, and hold the rest as reserves for later rounds.'
    }
}

TEMPLATES = {
    'Grunt': {
        'name': 'Grunt',
        'activations': 1,
        'structure': 0.25
    },
    'Normal': {
        'name': 'Normal',
        'activations': 1,
        'structure': 1
    },
    'Veteran': {
        'name': 'Veteran',
        'activations': 1,
        'structure': 2
    },
    'Commander': {
        'name': 'Commander',
        'activations': 1,
        'structure':2
    },
    'Elite': {
        'name': 'Elite',
        'activations': 2,
        'structure': 2
    },
    'Ultra': {
        'name': 'Ultra',
        'activations': 4,
        'structure': 4
    },
}

def select_class_count():
    selection = random.randrange(10)
    if selection < 1:
        return 3
    if selection < 7:
        return 4
    return 5

def select_template(has_ultra, has_commander):
    selection = random.randrange(10)
    if selection < 2:
        return TEMPLATES['Grunt']
    if selection < 3:
        return TEMPLATES['Veteran']
    if selection < 4:
        return TEMPLATES['Elite']
    if selection < 5 and (not has_commander or not has_ultra):
        choice = random.randrange(1)
        if choice == 0 and not has_commander:
            return TEMPLATES['Commander']
        if choice == 1 and not has_ultra:
            return TEMPLATES['Ultra']
        if not has_commander:
            return TEMPLATES['Commander']
        return TEMPLATES['Ultra']
    return TEMPLATES['Normal']


def generate_sitrep(npc_data, sitrep, players):
    sitrep_data = SITREP_REQUIREMENTS[sitrep]
    min_structure = 1.5 * players * sitrep_data['budget_multiplier']
    min_activations = 1.5 * players * sitrep_data['budget_multiplier']
    max_structure = 2 * players * sitrep_data['budget_multiplier']
    max_activations = 2 * players * sitrep_data['budget_multiplier']

    class_count = select_class_count()

    has_ultra = False
    has_commander = False

    npc_roster = {
        'sitrep': sitrep,
        'npcs': {},
        'structure': 0,
        'activations': 0,
        'striker_structure_activations': 0
    }

    while (npc_roster['structure'] < min_structure and npc_roster['activations'] < min_activations):
        if len(npc_roster['npcs'].keys()) == class_count:
            (npc_name, npc_class_data) = random.choice(list(npc_roster['npcs'].items()))
            if npc_class_data['template']['name'] == 'Ultra' or npc_class_data['template']['name'] == 'Commander':
                continue
            if npc_roster['activations'] + npc_class_data['template']['activations'] > max_activations or npc_roster['structure'] + npc_class_data['template']['structure'] > max_structure:
                continue

            additional_striker_structure_activations = 0
            if npc_class_data['class']['baseNpc']['role'] in ['Striker', 'Artillery']:
                additional_striker_structure_activations = npc_class_data['template']['structure'] + npc_class_data['template']['activations']
            potential_striker_ratio = (npc_roster['striker_structure_activations'] + additional_striker_structure_activations) / (npc_roster['structure'] + npc_roster['activations'] + additional_striker_structure_activations)
            if potential_striker_ratio > 0.5:
                continue

            npc_roster['npcs'][npc_name]['count'] += 1
            npc_roster['activations'] += npc_class_data['template']['activations']
            npc_roster['structure'] += npc_class_data['template']['structure']
            npc_roster['striker_structure_activations'] += additional_striker_structure_activations
        else:
            npc_class = random.choice(npc_data)
            if npc_class['baseNpc']['name'] in npc_roster['npcs'].keys():
                npc_name = npc_class['baseNpc']['name']
                npc_class_data = npc_roster['npcs'][npc_name]
                if npc_roster['activations'] + npc_class_data['template']['activations'] > max_activations or npc_roster['structure'] + npc_class_data['template']['structure'] > max_structure:
                    continue

                additional_striker_structure_activations = 0
                if npc_class_data['class']['baseNpc']['role'] in ['Striker', 'Artillery']:
                    additional_striker_structure_activations = npc_class_data['template']['structure'] + npc_class_data['template']['activations']
                potential_striker_ratio = (npc_roster['striker_structure_activations'] + additional_striker_structure_activations) / (npc_roster['structure'] + npc_roster['activations'] + additional_striker_structure_activations)
                if potential_striker_ratio > 0.5:
                    continue

                npc_roster['npcs'][npc_name]['count'] += 1
                npc_roster['activations'] += npc_class_data['template']['activations']
                npc_roster['structure'] += npc_class_data['template']['structure']
                npc_roster['striker_structure_activations'] += additional_striker_structure_activations
            else:
                template = select_template(has_ultra, has_commander)
                starting_count = 1
                if template['name'] == 'Grunt':
                    starting_count = 2

                starting_structure = starting_count * template['structure']
                starting_activations = starting_count * template['activations']

                if npc_roster['activations'] + starting_activations > max_activations or npc_roster['structure'] + starting_structure > max_structure:
                    continue

                additional_striker_structure_activations = 0
                if npc_class['baseNpc']['role'] in ['Striker', 'Artillery']:
                    additional_striker_structure_activations = starting_structure + starting_activations

                if npc_roster['striker_structure_activations'] > 0 and additional_striker_structure_activations > 0:
                    potential_striker_ratio = (npc_roster['striker_structure_activations'] + additional_striker_structure_activations) / (npc_roster['structure'] + npc_roster['activations'] + additional_striker_structure_activations)
                    if potential_striker_ratio > 0.5:
                        continue

                npc_name = npc_class['baseNpc']['name']
                npc_roster['npcs'][npc_name] = {
                    'template': template,
                    'count': starting_count,
                    'name': npc_name,
                    'class': npc_class
                }
                npc_roster['activations'] += starting_activations
                npc_roster['structure'] += starting_structure
                npc_roster['striker_structure_activations'] += additional_striker_structure_activations

                if template['name'] == 'Commander':
                    has_commander = True
                if template['name'] == 'Ultra':
                    has_ultra = True

    print(f"Sitrep: {npc_roster['sitrep'].capitalize()} ({sitrep_data['budget_multiplier']}x budget)")
    print(f"Instructions: {sitrep_data['instructions']}")
    print(f"Players: {players}")
    print("Roster:")
    for npc_name, npc_info in npc_roster['npcs'].items():
        optional_systems = ', '.join(npc_info['class']['optionalSystems'])
        print(f"* {npc_info['template']['name']} {npc_name} x{npc_info['count']} ({npc_info['class']['baseNpc']['role']}) (Suggested systems: {optional_systems})")
    print(f"Structure: {npc_roster['structure']} | Activations: {npc_roster['activations']}")
    print(f"Percent strikers/artillery: {round((npc_roster['striker_structure_activations'] / (npc_roster['structure'] + npc_roster['activations'])) * 100)}%")


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Generate sitrep NPC compositions for Lancer")
    parser.add_argument('--sitrep', '-s', type=str, default=None, help="Name of sitrep to generate. Options are: Gauntlet, Holdout, Recon, Extraction, Escort, Control")
    parser.add_argument('--players', '-p', type=int, default=4, help="Number of player characters to generate the sitrep for")
    args = parser.parse_args()

    npc_data = None
    with open('npcs.json') as npc_file:
        npc_data = json.load(npc_file)

    if not npc_data:
        sys.exit()

    sitrep = args.sitrep
    if not sitrep or sitrep not in ['gauntlet', 'holdout', 'recon', 'extraction', 'escort', 'control']:
        sitrep = random.choice(['gauntlet', 'holdout', 'recon', 'extraction', 'escort', 'control'])

    filtered_npc_data = list(filter(lambda n: sitrep.lower() in n['preferredSitreps'], npc_data))

    generate_sitrep(filtered_npc_data, sitrep, args.players)
