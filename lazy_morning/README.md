# lazy_morning

    Automate boring mundane morning checks

    Utility to run cmds configured in json and print out output

## Usage
```shell
 > ./dragon.py -h
usage: dragon [-h] config job

Run commands from config file in current host

positional arguments:
  config      input configuration as json file
  job         job to be executed

optional arguments:
  -h, --help  show this help message and exit

>./dragon.py ./config.json morningCheck
about to run job: morningCheck
Executing time [ cmd: date ]
output:
-------begin-------
Fri 02 Jul 2021 03:26:29 AM EDT
------finish-------
Executing memory [ cmd: free ]
output:
-------begin-------
              total        used        free      shared  buff/cache   available
Mem:        8064280     1321396     4445144       44996     2297740     6551580
Swap:        102396           0      102396
------finish-------

> ./dragon.py ./config.json wrongCmd
about to run job: wrongCmd
Executing time [ cmd: date123 ]
Encountered exception <class 'FileNotFoundError'>

>./dragon.py config.json longRun
about to run job: longRun
Executing longRun [ cmd: sleep 7 ]
Execution has timed out. Command 'sleep 7' timed out after 5 seconds

```


## TODO
     -   parallelize tasks based on config