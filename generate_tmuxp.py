import argparse

import yaml

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument(
    '--num-seeds',
    type=int,
    default=10,
    help='number of random seeds to generate')
parser.add_argument(
    '--env-names',
    default="HalfCheetah-v2",
    help='environment name separated by semicolons')
args = parser.parse_args()

template = "env CUDA_VISIBLE_DEVICES={3} python main.py --env_name {0} --seed {1} --start_timesteps {2} --prefix ={4}"

config = {"session_name": "run-all", "windows": []}

norms = ['', ' --norm_obs', ' --norm_ret',' --norm_obs --norm_ret']

counter = 0
for i in range(args.num_seeds):
    panes_list = []
    for env_name in args.env_names.split(';'):
        if env_name == "HalfCheetah-v2":
            start_timestep = 10000
        else:
            start_timestep = 1000
        for norm in norms:
            panes_list.append(
                        template.format(env_name, i, start_timestep, counter % 4, norm.replace(' ', '').replace('--','').replace('_', '')) + norm)
        counter += 1

    config["windows"].append({
        "window_name": "seed-{}".format(i),
        "panes": panes_list
    })

yaml.dump(config, open("run_all.yaml", "w"), default_flow_style=False)
