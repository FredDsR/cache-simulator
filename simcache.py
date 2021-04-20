import subprocess, os, json
import pandas as pd

PATH = os.getenv('HOME') + '/simplesim-3.0'

def clean_stats(raw_stats: str) -> dict:
    stats_title = 'sim: ** simulation statistics **'

    stats_start_point = raw_stats.find(stats_title) + len(stats_title) + 1

    raw_stats = raw_stats[stats_start_point:].split('\n')

    stats_dict = {}

    for stat in raw_stats:

        stat_components = stat.split('#')[0].strip().split(' ')

        stats_dict[stat_components[0]] = stat_components[-1]

    stats_dict.pop('')

    return stats_dict

def get_stats(stats: dict, config: dict) -> pd.DataFrame:
    new_dict = {'type': [],
                'accesses': [],
                'hits': [],
                'misses': [],
                'replacements': [],
                'writebacks': [],
                'invalidations': [],
                'miss_rate': [],
                'repl_rate': [],
                'wb_rate': [],
                'inv_rate': [],
                'nsets': [],
                'bsize': [],
                'assoc': [],
                'repl': []}

    types = config.keys()

    for key in stats.keys():
        splited_key = key.split('.')
        type = splited_key[0]
        if type in types:
            new_key = splited_key[1]
            new_dict[new_key].append(stats[key])
            if type not in new_dict['type']:
                new_dict['type'].append(type)
                new_dict['nsets'].append(config[type]['nsets'])
                new_dict['bsize'].append(config[type]['bsize'])
                new_dict['assoc'].append(config[type]['assoc'])
                new_dict['repl'].append(config[type]['repl'])

    return pd.DataFrame().from_dict(new_dict)


def run_simcache(config: dict) -> str:
    
    il1 = ['-cache:il1']
    dl1 = ['-cache:dl1']
    il2 = ['-cache:il2']
    dl2 = ['-cache:dl2']

    ul1 = []
    ul2 = []

    if 'ul1' in config.keys():
        ul1.append(f'ul1:{config["ul1"]["nsets"]}:{config["ul1"]["bsize"]}:{config["ul1"]["assoc"]}:{config["ul1"]["repl"]}')
        il1.append('dl1')
    else:
        il1.append(f'il1:{config["il1"]["nsets"]}:{config["il1"]["bsize"]}:{config["il1"]["assoc"]}:{config["il1"]["repl"]}') if config['il1'] else il1.append('none')
        dl1.append(f'dl1:{config["dl1"]["nsets"]}:{config["dl1"]["bsize"]}:{config["dl1"]["assoc"]}:{config["dl1"]["repl"]}') if config['dl1'] else dl1.append('none')
    
    if 'ul2' in config.keys():
        ul2.append(f'ul2:{config["ul2"]["nsets"]}:{config["ul2"]["bsize"]}:{config["ul2"]["assoc"]}:{config["ul2"]["repl"]}')
        il2.append('dl2')
    else:
        il2.append(f'il2:{config["il2"]["nsets"]}:{config["il2"]["bsize"]}:{config["il2"]["assoc"]}:{config["il2"]["repl"]}') if config['il2'] else il2.append('none')
        dl2.append(f'dl2:{config["dl2"]["nsets"]}:{config["dl2"]["bsize"]}:{config["dl2"]["assoc"]}:{config["dl2"]["repl"]}') if config['dl2'] else dl2.append('none')

    general = [
        '-tlb:itlb', 'none',
        '-tlb:dtlb','none',
        f'{PATH}/Benchmarks/gcc/cc1.ss',
        f'{PATH}/Benchmarks/gcc/gcc.i'
    ]

    cmd = [f'{PATH}/sim-cache'] + il1 + dl1 + ul1 + il2 + dl2 + ul2 + general

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    output, error = proc.communicate()

    # print(output.decode('ascii'))
    # print(error.decode('ascii'))

    return error.decode('ascii')

def run_simulation(config: dict) -> pd.DataFrame:
    raw_stats = run_simcache(config)

    stats = clean_stats(raw_stats)

    return get_stats(stats, config)

def run_experiment(config: dict) -> pd.DataFrame:
    
    experiment_df = pd.DataFrame()

    for i, simulation_config in enumerate(config):
        simulation_df = run_simulation(simulation_config)
        simulation_df['label'] = 'simulation_' + str(i)
        experiment_df = pd.concat([experiment_df, simulation_df])

    return experiment_df

def get_experiments_config() -> list:
    abs_path = os.path.abspath(os.path.dirname(""))
    config_path = abs_path + '/experiments'
    config_files = os.listdir(config_path)
    config_files = [config_path + '/' + config_file for config_file in config_files]

    experiments_config = []

    for config_file in config_files:
        with open(config_file, 'r', encoding='utf-8') as file:
            experiments_config.append(json.load(file))

    return experiments_config

def main() -> None:
    experiments_config = get_experiments_config()
    
    for i, experiment_config in enumerate(experiments_config):
        df = run_experiment(experiment_config)
        
        if 'results' not in os.listdir('./'):
            os.mkdir('./results')

        df.to_csv('./results/experiment_' + str(i), index=False)


if __name__ == "__main__":
    main()

# config_2 = {
#     'ul1': {
#         'nsets': '128',
#         'bsize': '64',
#         'assoc': '1',
#         'repl': 'l'
#     },
#     'il2': None,
#     'dl2': None,
# }
