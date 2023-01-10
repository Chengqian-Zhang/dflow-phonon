# dflow-phonon
## Overview
This workflow is a part of [AI Square](https://aissquare.com/).I want to make the process of computing phonon more automatic.So I write this workflow based on [dflow](https://github.com/deepmodeling/dflow).The related computational tasks are submitted to the [Bohrium](https://bohrium.dp.tech/) platform.

This workflow supports phonon calculations based on both DFT and DP potential.More specifically, DFT calculations support VASP code and ABACUS code.The part of phonon computation is implemented by using Phonopy code and Phonolammps code.
## Easy Install：
```
pip install --index-url https://pypi.org/simple/ dflow-phonon
```
## Quick Start
You can go to the `example` folder.You can see that there are some examples for reference.You can go to one of them and fill in the `global.json` file.Then you can submit the workflow.

If you want to use VASP code to do the DFT calculation,like the folder `vasp_dfpt_demo` and `vasp_displacement_demo`：
``` 
dflowphonon --vasp
```
If you want to use ABACUS code：
```
dflowphonon --abacus
```
If you want to use DP potential:
```
dflowphonon --dp
```

Then you can monitor the workflow process on the [website](https://workflows.deepmodeling.com).

## Details of Workflow
If you want to use VASP code.You can choose from two calculation methods.One is `linear response method` and anothers is `finite displacement method`.
