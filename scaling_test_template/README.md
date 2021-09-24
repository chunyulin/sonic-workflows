Here are scripts and template used for scaling test on T2_TW_NCHC. Data files has been copied to the site and no CMS grid certificate is needed for the run.
We also tarball the PR10/PR13 workflow to the site, see `./tpl/sonic.sh` for detail. No need to run `setup.py` from scratch.

1) Copy `./tpl` to, say, the folder `./g1_t4`, `./g2_t4` as difference set of testing.
2) In the folder in step-1, run `prepare.sh` to generate working condor DAG `dagfile.dag` and subfolder `qNNN` for # of clients.
3) Submit condor DAG by `condor_submit_dag dagfile.dag`. Each run should output the cmsRun logs and a json file from FastTimerService.
4) Repeat 2-3 for other cases.
4) Run `. ../collect_runs_sync.sh` to generate summary in `runs.dat` and `sync_tput.dat`.
5) (optional) Run `../pltTimeline.py` to generate timeline plot.
6) Go back to this folder, run `pltAggScale.py` to generate Scaling plot for different set of runs.
7) Other scripts are used to generate plots for Runtime, Time breakdown, and detail verbose information.

--
