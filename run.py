import argparse
import glob
import os
import sys
import traceback

import calliope


def get_args():
  parser = argparse.ArgumentParser(description='Tutorial workflow for AWF.')
  parser.add_argument("-i", "--inputDir",
                      help="path to input directory")
  parser.add_argument("-o", "--outputDir",
                      help="path to output directory")
  args = parser.parse_args()
  return args


def read_inputs(args):
  dir = glob.glob(f"{args.inputDir}")[0]
  inputs = []
  for file in os.listdir(dir):
    if file.endswith('.yaml'):
      inputs.append(file)
  print(inputs)
  return inputs


def run_scenario(input_path: str):
  try:
    scenario = calliope.Model(input_path)
  except Exception as e:
    print('ERROR - Model Build')
    res = traceback.print_exc(file=sys.stdout)
    with open('tmp/log.txt', 'w+') as f:
      f.write(str(e))
      f.write(traceback.format_exc())
    return e

  try:
    scenario.run(force_rerun=True)
    return scenario
  except Exception as e:
    print('ERROR - Calliope Run')
    res = traceback.print_exc(file=sys.stdout)
    with open('tmp/log.txt', 'w+') as f:
      f.write(str(e))
      f.write(traceback.format_exc())
    return e


def main():
  args = get_args()
  print(args)
  input_dir = args.inputDir
  data = read_inputs(args)
  if 'model.yaml' in data:
    res = run_scenario(f"{input_dir}/model.yaml")
    print(res.__dict__)
    print(res.run_config)
    print(res.model_config)
    print(res.results)
    res.plot()


if __name__ == "__main__":
  main()
