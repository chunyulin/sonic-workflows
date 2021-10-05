# Note

Here are the template used for SONIC scaling test on T2_TW_NCHC.

Several things has done on the site to facilitate the testing by local submission:
- Data files has been copied to the site, as modified in `step*.py`. So, no CMS grid certificate is needed.
- We tarball the workflow in each WNs. Therefore, no need to run `setup.py` to setup sonic workflow from scratch each time. See `./tpl/sonic.sh` for detail.
- I modified `run.py` to accommodate multiple Triton servers and FastTimerService for reading out the throughput information.
- Some plot scripts has to be modified to accommodate `REPEATS>1` in the `prepare.sh`.

Typical steps for a simutanious clients run are:
1) Copy `./tpl` to, say, the folder `./g1_t4`, `./g2_t4` as difference set of testing.
2) In the folder of step-(1), run `prepare.sh` to generate condor DAG workflow `dagfile.dag` and working folder `qNNN` for each # of clients.
3) Submit condor DAG by `condor_submit_dag dagfile.dag`. Each run will output the cmsRun logs and a json file from FastTimerService.
4) Execute `. ../collect_runs_sync.sh` to collect summaries from every `qNNN` working folder and output `runs.dat` and `sync_tput.dat`.
5) (optional) Run `../pltTimeline.py` to generate timeline plot.
6) Repeat 2-5 for another cases.
7) Go back to this folder, run `./pltAggScale.py` to produce the scaling plot for different set of runs as in step-(1).
8) There are other scripts used to generate plots for Runtime, Time breakdown, and detail verbose information, etc.


--
