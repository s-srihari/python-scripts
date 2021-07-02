#! /usr/bin/python3
import argparse
import json
from os import path
from subprocess import Popen, PIPE, check_output, run
import subprocess
import sys
import platform
import traceback

arg_parser = argparse.ArgumentParser(prog="dragon", description="Run commands from config file in current host")
arg_parser.add_argument('config', metavar='config', type=str, help='input configuration as json file')
arg_parser.add_argument('job', metavar='job', type=str, help='job to be executed')

args = arg_parser.parse_args()

def verifyCurrentHost(job):
    return (job['host'] == platform.node())
    

def verifyInputConfigConfig():
    if (path.exists(args.config)) == False:
        print('Provided config does not exist')
        return False
    return True
   
def load_json():
    with open(args.config,'r',  encoding='utf-8') as f:
        json_data=json.load(f)
    return json_data['jobs']

def handlePipeCmd(cmd_str):
    r = subprocess.check_output(cmd_str, shell=True, timeout=5)
    print( "Output: {}".format(r.decode('utf-8')))
    

def execJob(job):
    print("about to run job: {}".format(job['name']))
    for cmd in job['cmds']:
        print("Executing {} [ cmd: {} ]".format(cmd['title'], cmd['exec']))
        try:
            cmd_string = str(cmd['exec'])
            result = ''

            if "|" in cmd_string:
                handlePipeCmd(cmd_string)
            else:
                result = subprocess.check_output(cmd['exec'], shell=True, text=True, stderr=subprocess.STDOUT, timeout=5)
                print('output:\n-------begin-------\n{}------finish-------'.format(result))
                print(result)

            if result == cmd['output']:
                print('Output Matches expectation')

        except subprocess.CalledProcessError as ce:
            print('exit code {}'.format(ce.returncode))
            print('stdout: {}'.format(ce.stdout))
            print('stderr: {}'.format(ce.stderr))  
        except subprocess.TimeoutExpired as t:
            print('Execution has timed out. {}'.format(t))          
        except:    
            e = sys.exc_info()[0]
            traceback.print_exception(e)
            print("Encountered exception {}".format(e))
            

def perform():
    if verifyInputConfigConfig():
        jobs = load_json()
        job_found = False
        for job in jobs:
            if args.job == job['name']:
                job_found = True
                if verifyCurrentHost(job):
                    execJob(job)
                else:
                    print('Provided job: {} is for host: {}'.format( job['name'], job['host']))
                break
        if( job_found == False):
            print('Job Provided does not exist')
    else:
        print('Config file missing. Exiting Program')


if __name__=='__main__':
    perform()   