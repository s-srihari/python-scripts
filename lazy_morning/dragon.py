#! /usr/bin/python3
import argparse
import json
from os import path
import subprocess
import sys

arg_parser = argparse.ArgumentParser(prog="dragon", description="Run commands from config file in current host")
arg_parser.add_argument('config', metavar='config', type=str, help='input configuration as json file')
arg_parser.add_argument('job', metavar='job', type=str, help='job to be executed')

args = arg_parser.parse_args()


def verifyInputConfigConfig():
    if (path.exists(args.config)) == False:
        print('Provided config does not exist')
        return False
    else:
        print('Config File {} exists'.format(args.config))
        return True
   
def load_json():
    with open(args.config,'r',  encoding='utf-8') as f:
        json_data=json.load(f)
    return json_data['jobs']

def execJob(job):
    print("about to run job: {}".format(job['name']))
    for cmd in job['cmds']:
        print("Executing cmd id:{} title: {}".format(cmd['id'], cmd['title']))
        try:
            result = subprocess.check_output([cmd['exec']], text=True, stderr=subprocess.PIPE, timeout=5)
            print('output:\n-------begin-------\n{}------finish-------'.format(result))
        except subprocess.CalledProcessError as ce:
            print('exit code {}'.format(ce.returncode))
            print('stdout: {}'.format(ce.stdout))
            print('stderr: {}'.format(ce.stderr))        
        except:    
            e = sys.exc_info()[0]
            print("Encountered exception {}".format(e))
            

def perform():
    if verifyInputConfigConfig():
        jobs = load_json()
        job_found = False
        for job in jobs:
            if args.job == job['name']:
                job_found = True
                execJob(job)
                break
        if( job_found == False):
            print('Job Provided does not exist')
    else:
        print('Config file missing. Exiting Program')


if __name__=='__main__':
    perform()   