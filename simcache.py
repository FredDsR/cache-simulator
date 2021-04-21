import subprocess, os, json, sys, re
import pandas as pd

ABS_PATH = os.path.abspath(os.path.dirname(""))
CONFIG_PATH = ABS_PATH + '/experiments'
SIMCACHE_PATH = os.getenv('HOME') + '/simplesim-3.0'

sys.path.append(SIMCACHE_PATH)

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
    new_dict = {'cache': [],
                'nsets': [],
                'bsize': [],
                'assoc': [],
                'repl': [],
                'benchmark': [],
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
                'sim_num_insn': [],
                'sim_num_refs': [],
                'sim_elapsed_time': [],
                'sim_inst_rate': []} 

    types = config.keys()

    file_pattern = r'[^-]+.\.+.'
    
    for key in stats.keys():
        splited_key = key.split('.')
        cache = splited_key[0]
        if cache in types:
            new_key = splited_key[1]
            new_dict[new_key].append(stats[key])
            if cache not in new_dict['cache']:
                new_dict['cache'].append(cache)
                new_dict['nsets'].append(config[cache]['nsets'])
                new_dict['bsize'].append(config[cache]['bsize'])
                new_dict['assoc'].append(config[cache]['assoc'])
                new_dict['repl'].append(config[cache]['repl'])

                benchmark_files = [benchmark.split('/')[-1] 
                                   for benchmark in config['benchmark'].split(' ') 
                                   if re.match(file_pattern, benchmark)]  

                new_dict['benchmark'].append('_'.join(benchmark_files))

                new_dict['sim_num_insn'].append(stats['sim_num_insn'])
                new_dict['sim_num_refs'].append(stats['sim_num_refs'])
                new_dict['sim_elapsed_time'].append(stats['sim_elapsed_time'])
                new_dict['sim_inst_rate'].append(stats['sim_inst_rate'])


    return pd.DataFrame().from_dict(new_dict)

def run_simcache(config: dict) -> str:
    
    il1 = ['-cache:il1']
    dl1 = ['-cache:dl1']
    il2 = ['-cache:il2']
    dl2 = ['-cache:dl2']

    ul1 = []
    ul2 = []

    benchmark = []

    benchmark_args = config['benchmark'].split(' ')

    file_pattern = r'[^-]+.+\..+'

    for arg in benchmark_args:
        if re.match(file_pattern, arg):
            benchmark.append(f'{SIMCACHE_PATH}/{arg}')
        else:
            benchmark.append(arg)


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
        '-tlb:dtlb','none'
    ]

    cmd = [f'{SIMCACHE_PATH}/sim-cache'] + il1 + dl1 + ul1 + il2 + dl2 + ul2 + general + benchmark

    print('-> Command executed:')
    print(' '.join(cmd))

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    output, error = proc.communicate()

    return error.decode('ascii')

def run_simulation(config: dict) -> pd.DataFrame:
    raw_stats = run_simcache(config)

    stats = clean_stats(raw_stats)

    return get_stats(stats, config)

def run_experiment(config: dict) -> pd.DataFrame:
    
    experiment_df = pd.DataFrame()

    for i, simulation_config in enumerate(config):
        print(f'-> Running simulation {i}')
        simulation_df = run_simulation(simulation_config)
        simulation_df['label'] = 'simulation_' + str(i)
        experiment_df = pd.concat([experiment_df, simulation_df])

    return experiment_df

def get_experiments_config() -> dict:
    
    config_files = os.listdir(CONFIG_PATH)
    abs_config_files = [CONFIG_PATH + '/' + config_file for config_file in config_files]

    experiments_config = {}

    json_pattern = r'.+\.json'

    for i, config_file in enumerate(abs_config_files):
        if re.match(json_pattern, config_file):
            print(f'-> Reading file: {config_file}')
            with open(config_file, 'r', encoding='utf-8') as file:
                experiments_config[config_files[i]] = json.load(file)

    return experiments_config

def main() -> None:
    experiments_config = get_experiments_config()

    for key in experiments_config.keys():
        
        print(f'-> Running experiment {key}')

        df = run_experiment(experiments_config[key])
        
        if 'results' not in os.listdir('./'):
            os.mkdir('./results')

        df.to_csv('./results/' + key.split('.')[0] + '.csv', index=False)


if __name__ == "__main__":
    main()
