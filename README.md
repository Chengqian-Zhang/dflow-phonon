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
If you want to use ABACUS code,like the folder `abacus_demo`：
```
dflowphonon --abacus
```
If you want to use DP potential,like the folder `dp_demo`:
```
dflowphonon --dp
```

Then you can monitor the workflow process on the [website](https://workflows.deepmodeling.com).

## Details of Workflow
If you want to use VASP code.You can choose from two calculation methods.One is `linear response method` and anothers is `finite displacement method`.

One advantage of the `linear response method` over the `finite displacement method` is that one does not need to create super-cells, which can be in some cases computationally more efficient. Moreover, in systems where the phonon dispersions behave in an anomalous way (like systems with Kohn anomalies) the linear response method is more suitable, because it is capable of calculating the exact phonons at the requested points.

One advantage of the `finite displacement method` is that it is an add on that can work with any code, also non-density functional theory codes. All is needed is the ability of the external code to compute forces (codes like ABACUS and wien2k for example do not include an implementation of the linear response method, but the small displacement method implemented in phon can be used in conjunction with these codes).

You can read this paper<sup>[1]</sup> to get more information about these methods.

Unlike VASP code, ABACUS code does not support `linear response method` for now, so the `finite displacement method` is used by default when using ABACUS code.

## Reference
[1] Alfe, D. (2007). Tutorial on calculating phonons: comparing the linear response and the small displacement methods. Department of Earth Sciences and Department of Physics and Astronomy, University College, London.
