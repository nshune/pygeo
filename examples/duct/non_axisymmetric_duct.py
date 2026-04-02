import numpy as np
from pygeo import pyGeo
import os

def create_non_axisymmetric_duct():
    # 1. Configuration
    radius = 1.0
    n_ribs = 4 # Top, Right, Bottom, Left
    angles = [0, 90, 180, 270]
    
    # Scale factors as requested:
    # 0 deg (Top): 1.02
    # 90 deg (Side): 1.0
    # 180 deg (Bottom): 0.98
    # 270 deg (Side): 1.0
    scales = [1.02, 1.0, 0.98, 1.0]
    
    # 2. Setup Airfoil (using a standard NACA 0012)
    airfoil_file = "naca0012.dat"
    if not os.path.exists(airfoil_file):
        with open(airfoil_file, "w") as f:
            f.write("NACA0012\n")
            f.write(" 1.000000  0.001260\n")
            f.write(" 0.950000  0.007640\n")
            f.write(" 0.900000  0.013480\n")
            f.write(" 0.800000  0.023840\n")
            f.write(" 0.700000  0.032640\n")
            f.write(" 0.600000  0.039600\n")
            f.write(" 0.500000  0.044160\n")
            f.write(" 0.400000  0.046160\n")
            f.write(" 0.300000  0.045240\n")
            f.write(" 0.250000  0.043360\n")
            f.write(" 0.200000  0.040400\n")
            f.write(" 0.150000  0.036080\n")
            f.write(" 0.100000  0.029840\n")
            f.write(" 0.075000  0.025720\n")
            f.write(" 0.050000  0.020840\n")
            f.write(" 0.025000  0.014560\n")
            f.write(" 0.012500  0.010160\n")
            f.write(" 0.000000  0.000000\n")
            f.write(" 0.012500 -0.010160\n")
            f.write(" 0.025000 -0.014560\n")
            f.write(" 0.050000 -0.020840\n")
            f.write(" 0.075000 -0.025720\n")
            f.write(" 0.100000 -0.029840\n")
            f.write(" 0.150000 -0.036080\n")
            f.write(" 0.200000 -0.040400\n")
            f.write(" 0.250000 -0.043360\n")
            f.write(" 0.300000 -0.045240\n")
            f.write(" 0.400000 -0.046160\n")
            f.write(" 0.500000 -0.044160\n")
            f.write(" 0.600000 -0.039600\n")
            f.write(" 0.700000 -0.032640\n")
            f.write(" 0.800000 -0.023840\n")
            f.write(" 0.900000 -0.013480\n")
            f.write(" 0.950000 -0.007640\n")
            f.write(" 1.000000 -0.001260\n")

    xsections = [airfoil_file] * n_ribs
    
    # 3. Define the 3D placement of each rib
    Xsec = np.zeros((n_ribs, 3))
    rot = np.zeros((n_ribs, 3))
    
    for i in range(n_ribs):
        theta = np.deg2rad(angles[i])
        
        # Origin of the rib (a ring in the Y-Z plane)
        Xsec[i, 0] = 0.0 # Axial position
        Xsec[i, 1] = radius * np.cos(theta)
        Xsec[i, 2] = radius * np.sin(theta)
        
        # Rotation around X to orient the rib thickness radially
        rot[i, 0] = angles[i]
    
    # 4. Initialize the Duct
    # pyGeo will automatically weld the 270->0 degree seam 
    # and set the topology to periodic for smooth parameterization.
    print("Initializing non-axisymmetric duct...")
    duct = pyGeo(
        "duct",
        xsections=xsections,
        X=Xsec,
        rot=rot,
        scale=scales,
        kSpan=3 # Cubic interpolation around the circumference for smoothness
    )
    
    # 5. Output
    print("Writing output files...")
    duct.writeTecplot("non_axis_duct.dat")
    duct.writeIGES("non_axis_duct.igs")
    
    print("Non-axisymmetric duct created successfully.")
    print(f"Top Scale (0 deg): {scales[0]}")
    print(f"Bottom Scale (180 deg): {scales[2]}")

if __name__ == "__main__":
    create_non_axisymmetric_duct()
