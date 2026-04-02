# Duct Surface Implementation in pyGeo

This document summarizes the changes made to `pygeo` to support the native construction of duct and nacelle surfaces, including support for periodic topologies and non-axisymmetric geometries.

## Changes to pyGeo Codebase

### 1. Topology Engine (`pygeo/topology.py`)
- **Periodic Support**: Added a `periodic` attribute to the base `Topology` class and its subclasses (`SurfaceTopology`, `BlockTopology`).
- **Initialization**: Updated `SurfaceTopology.__init__` and `BlockTopology.__init__` to accept and store the `periodic` flag. This allows the topology engine to correctly identify and "weld" edges that connect back to themselves (e.g., the 0/360-degree seam of a duct).

### 2. Surfacing Engine (`pygeo/pyGeo.py`)
- **New Initialization Type**: Added `initType="duct"` to the `pyGeo` constructor.
- **Duct Builder Method**: Implemented `_init_duct_surface`, a "rib-based" lofting method.
    - It lofts between airfoil-like cross-sections.
    - It supports independent 3D placement (`X`), rotation (`rot`), and `scale` for each rib, enabling non-axisymmetric and curved ducts.
    - It automatically closes the circumferential loop and sets the `periodic` flag.
- **Connectivity Integration**: Updated `_calcConnectivity` to pass the `periodic` flag to the `SurfaceTopology` instance, ensuring smooth global numbering and parameterization across the seam.

### 3. Volume Engine (`pygeo/pyBlock.py`)
- **Consistency**: Added the `periodic` attribute to `pyBlock` and updated its `_calcConnectivity` method to pass this flag to `BlockTopology`. This ensures that if an FFD volume is created for a duct, it can also respect periodic boundaries.

### 4. Examples
- **Non-Axisymmetric Duct**: Created `examples/duct/non_axisymmetric_duct.py`. This example demonstrates how to build a nacelle-like duct where the top and bottom sections are scaled differently (1.02 vs 0.98), creating a smooth, non-axisymmetric transition.

---

## Rebuilding the Environment (Linux)

To continue development on Linux and successfully build the `pyspline` Fortran extensions, follow these steps:

### 1. Prerequisites
Ensure you have a Fortran compiler, a C compiler, and `make` installed:
```bash
sudo apt-get update
sudo apt-get install build-essential gfortran make
```

### 2. Create Conda Environment
```bash
# Create the environment
conda create -n pygeo_mod python=3.11 -y
conda activate pygeo_mod

# Install MPI and basic dependencies
conda install -c conda-forge mpi4py numpy scipy packaging -y
```

### 3. Install MDOlab Dependencies
`pyspline` must be built from source to compile the Fortran object files:
```bash
# Clone and build pyspline
git clone https://github.com/mdolab/pyspline.git
cd pyspline
cp config/defaults/config.LINUX_GFORTRAN.mk config/config.mk
make
pip install .
cd ..
```

### 4. Install pygeo in Editable Mode
From the root of this `pygeo` repository:
```bash
pip install mdolab-baseclasses
pip install -e .
```

### 5. Run the Example
```bash
python examples/duct/non_axisymmetric_duct.py
```
This should generate `non_axis_duct.dat` (Tecplot) and `non_axis_duct.igs` (IGES) files.
