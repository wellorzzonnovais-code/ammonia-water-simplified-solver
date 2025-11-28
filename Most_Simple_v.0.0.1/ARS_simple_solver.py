#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 11:00:00 2022

@author: Wellorzzon Novais
"""

"""
Description
--
This code is a simulation of a simplified absorption refrigeration cycle, including:
    - 1 condenser
    - 1 generator
    - 1 evaporator
    - 1 absorber
    - 1 pump
    - 2 expansion valves
The calculation were defined based on energy and mass balance, but with some very simple boundary conditions. That why it is called "Most Simple" version.
"""

"""
Log

--------------------------------------
Version 0.0.1
--
Based on Simple_v0.0.1 and the main goal is to simulate a very simple cycle in EES or RefProp v10 (and not v9.0).
The program is created to accomplish the new model in file "Most Simple Cycle Steps v1"

TO DO:
    - Implementing calls for RefProp v10

--------------------------------------
"""


# --------------------------------------------------------------------------
# Configuring RefProp v10
# --------------------------------------------------------------------------

# This path is suitable for the developer's computer (the developer has multiple 
# copies of REFPROP installed on their computer), but the default configuration 
# with the REFPROP installer on windows should not require this step
import os
os.environ['RPPREFIX'] = r'/home/unknown/REFPROP_v10'

# Import the main class from the Python library
from ctREFPROP.ctREFPROP import REFPROPFunctionLibrary

# Now we instantiate the library, and use the environment variable to
# explicitly state which path we want to use. It was decided to make
# the path handling explicit (though more verbose), because explicit 
# is almost always better than implicit
RP = REFPROPFunctionLibrary(os.environ['RPPREFIX'])

# Now we tell REFPROP what the root directory is that it should use.  This root directory should contain, at least:
# A) REFPRP64.DLL (or REFPROP.dll for 32-bit windows, or librefprop.so or librefprop.dylib, for linux or OSX respectively)
# B) FLUIDS folder (case sensitive)
# C) MIXTURES folder (case sensitive)
RP.SETPATHdll(os.environ['RPPREFIX'])

# Get the unit system we want to use (we will revisit this GETENUM function later)
# According to https://refprop-docs.readthedocs.io/en/latest/DLL/high_level.html#f/_/REFPROPdll
MASS_BASE_SI = RP.GETENUMdll(0, "MASS BASE SI").iEnum


# --------------------------------------------------------------------------
# Calling my own library of equations
# --------------------------------------------------------------------------

import mass_and_energy_balance as meb


# --------------------------------------------------------------------------
# Using SI on each variable, as prof. Simões observed
# 
# Temperature in Kelvin
# --------------------------------------------------------------------------


# -----------------------------
# Operational Conditions
# -----------------------------

## Mass fraction equality:
# x_1 = x_2
# x_3 = x_4 = x_5 = x_6
# x_7 = x_8

## Pressure equality:
# P_4 = P_2 = P_3 = P_7
# P_6 = P_1 = P_5 = P_8

## Mass flow rate equality:
# m_ponto_1 = m_ponto_2
# m_ponto_3 = m_ponto_4 = m_ponto_5 = m_ponto_6
# m_ponto_7 = m_ponto_8

## Isenthalpic Expansion Valve:
# h_4 = h_5
# h_7 = h_8

## Isentropic pump:
# s_1 = s_2

## Input data:
Temp_3 = 373.15 #[K] - Temperature in generator high outlet or condenser inlet
Temp_4 = 313.15 #[K] - Temperature in condenser outlet or EV1 inlet
Temp_6 = 253.15 #[K] - Temperature in evaporator outlet or absorber inlet

Q_eva = 5000 #[W] - Cooling load in evaporator
eff_p = 0.85 # - Thermodynamic pump efficiency

x_1 = x_2 = 0.42 # - Ammonia mass fraction in absorber outlet, pump and generator inlet
x_3 = x_4 = x_5 = x_6 = 1 # - Ammonia mass fraction in generator outlet, condenser, EV1, evaporator and absorber inlet

Qu_1 = 0 # - Vapor quality in generator high outlet or condenser inlet
#Qu_3 = 1 # - Vapor quality in absorber outlet or pump inlet (deleted and changed to Temp_3*)
Qu_4 = 0 # - Vapor quality in condenser outlet or pump inlet
Qu_6 = 1 # - Vapor quality in evaporator outlet or absorber inlet
Qu_7 = 0 # - Vapor quality in generator outlet or EV2 inlet


# call dir and store it in a variable. It stores all the variable names defined before in the form of a list and stores the variable names as a string.
# not_my_data = set(dir())
# all_initial_properties = set(dir()) - not_my_data
# print(all_initial_properties)

# ---------------------------------------
# Solving lines Thermodynamic Properties
# ---------------------------------------


# 1. Search for three variables with properties (for example, P, T, x, Qu, h and s) with the same end number:
# (To be implemented)

# Result = line 4

# # Iterate over the whole list where dir( )
# # is stored.
# for name in all_initial_properties:
    
#     # Print the item if it doesn't start with '__'
#     i = 1
#     count = 0
#     if name.endswith('_'+str(i)):
#         # myvalue = eval(name)
#         print(name)
#         count =+ 1
    

# 2. Taking the thermodynamic properties from an external software and register as a dictionary or list
print("Step 2:")

    # Properties from line 1, 3, 4 and 6 have three properties.
    # First solve which has three properties with numbers (excluding Pressure), which are lines 4 and 6:
 
        # External_program_properties(Temp_4, x_4, Qu_4)
        # ThermoProperties_4 = [P_4, h_4, s_4, ..._4]       
 
ocalc_4 = RP.REFPROPdll("Ammonia * Water","TQ","P;H;S",MASS_BASE_SI,1,0,Temp_4,Qu_4,[x_4, 1-x_4])
assert(ocalc_4.ierr == 0)
P_4, h_4, s_4 = ocalc_4.Output[0:3]
print("P_4 = " + "{:.4g}".format(P_4) + "; h_4 = " + "{:.4g}".format(h_4) + "; s_4 = " + "{:.4g}".format(s_4))

        
        # External_program_properties(Temp_6, x_6, Qu_6)
        # ThermoProperties_6 = [P_6, h_6, s_6, ..._6]


ocalc_6 = RP.REFPROPdll("Ammonia * Water","TQ","P;H;S",MASS_BASE_SI,1,0,Temp_6,Qu_6,[x_6, 1-x_6])
assert(ocalc_6.ierr == 0)
P_6, h_6, s_6 = ocalc_6.Output[0:3]
print("P_6 = " + "{:.4g}".format(P_6) + "; h_6 = " + "{:.4g}".format(h_6) + "; s_6 = " + "{:.4g}".format(s_6))

print()



# 3. Apply pressure equality at lines 1, 2, 3, 5, 7, 8:
print("Step 3:")
    
P_2 = P_3 = P_7 = P_4
print("P_2 = " + "{:.4g}".format(P_2))
print("P_3 = " + "{:.4g}".format(P_3))
print("P_7 = " + "{:.4g}".format(P_7))

P_1 = P_5 = P_8 = P_6 
print("P_1 = " + "{:.4g}".format(P_1))        
print("P_5 = " + "{:.4g}".format(P_5))    
print("P_8 = " + "{:.4g}".format(P_8))

print()



# 4. Try to solve the lines that has three properties (with new properties calculated), which are lines 1 and 3:
print("Step 4:")
 
    # External_program_properties(P_3, Temp_3, x_3)
    # ThermoProperties_3 = [Temp_3, h_3, s_3, ..._3]
    
ocalc_3 = RP.REFPROPdll("Ammonia * Water","PT","Qmass;H;S",MASS_BASE_SI,1,0,P_3,Temp_3,[x_3, 1-x_3])
assert(ocalc_3.ierr == 0)
Qu_3, h_3, s_3 = ocalc_3.Output[0:3]
print("Qu_3 = " + "{:.4g}".format(Qu_3) + "; h_3 = " + "{:.4g}".format(h_3) + "; s_3 = " + "{:.4g}".format(s_3))


    # External_program_properties(P_1, x_1, Qu_1)
    # ThermoProperties_1 = [Temp_1, h_1, s_1, ..._1]
    
ocalc_1 = RP.REFPROPdll("Ammonia * Water","PQ","T;H;S",MASS_BASE_SI,1,0,P_1,Qu_1,[x_1, 1-x_1])
assert(ocalc_1.ierr == 0)
Temp_1, h_1, s_1 = ocalc_1.Output[0:3]
print("Temp_1 = " + "{:.4g}".format(Temp_1) + "; h_1 = " + "{:.4g}".format(h_1) + "; s_1 = " + "{:.4g}".format(s_1))


print()




# 5. Apply isenthalpic expansion valve condition for line 5, and try to solve this one that has three properties (with new properties calculated):
print("Step 5:")
    
h_5 = h_4
    # External_program_properties(P_5, x_5, h_5)
    # ThermoProperties_5 = [Temp_5, Qu_5, s_5, ..._5]

ocalc_5 = RP.REFPROPdll("Ammonia * Water","PH","T;Qmass;S",MASS_BASE_SI,1,0,P_5,h_5,[x_5, 1-x_5])
assert(ocalc_5.ierr == 0)
Temp_5, Qu_5, s_5 = ocalc_5.Output[0:3]
print("Temp_5 = " + "{:.4g}".format(Temp_5) + "; Qu_5 = " + "{:.4g}".format(Qu_5) + "; s_5 = " + "{:.4g}".format(s_5))

print()



# 6. Try to solve the lines that has three properties (with new properties calculated), which is line 7:
print("Step 6:")
  
    # External_program_properties(P_7, Temp_7, Qu_7)
    # ThermoProperties_7 = [x_7, h_7, s_7, ..._7]


x_7_guess = 0
guess_fraction = 0.0001
i = 1
limit_iterations = 1/guess_fraction
while i <= limit_iterations:
    ocalc_7 = RP.REFPROPdll("Ammonia * Water","PQ","T",MASS_BASE_SI,1,0,P_7,Qu_7,[x_7_guess, 1-x_7_guess])
    assert(ocalc_7.ierr == 0)
    Temp_7_calc, = ocalc_7.Output[0:1]
    Temp_diff = Temp_7_calc - Temp_3 # We are trying to reach Temp_7 == Temp_3
    if Temp_diff <= 0.0001:
        x_7 = x_7_guess
        break
    else:
        i += 1
        x_7_guess += guess_fraction
        # print(x_7_guess)

# print("\n" + "{:.4g}".format(x_7))

ocalc_7 = RP.REFPROPdll("Ammonia * Water","PQ","T;H;S",MASS_BASE_SI,1,0,P_7,Qu_7,[x_7, 1-x_7])
assert(ocalc_7.ierr == 0)
Temp_7, h_7, s_7 = ocalc_7.Output[0:3]
print("Temp_7 = " + "{:.4g}".format(Temp_7) + "; Qu_7 = " + "{:.4g}".format(Qu_7) + "; s_7 = " + "{:.4g}".format(s_7) + "; x_7 = " + "{:.4g}".format(x_7))

print()


# 7. Apply isentropic pump condition for line 2 and try to solve because it has three properties (with new properties calculated):
print("Step 7:")

s_2 = s_1
    # External_program_properties(P_2, x_2, s_2)
    # ThermoProperties_2 = [P_2, h_2, Qu_2, ..._2]


ocalc_2 = RP.REFPROPdll("Ammonia * Water","PS","T;Qmass;H",MASS_BASE_SI,1,0,P_2,s_2,[x_2, 1-x_2])
assert(ocalc_2.ierr == 0)
Temp_2, Qu_2, h_2 = ocalc_2.Output[0:3]
print("Temp_2 = " + "{:.4g}".format(Temp_2) + "; Qu_2 = " + "{:.4g}".format(Qu_2) + "; h_2 = " + "{:.4g}".format(h_2))

print()



# 8. Apply isenthalpic expansion valve condition for line 8, and try to solve this one that has three properties (with new properties calculated): 
print("Step 8:")
    
x_8 = x_7 # - Ammonia mass fraction in generator low outlet, EV2 inlet and absorber inlet   
h_8 = h_7
    
    # External_program_properties(P_8, x_8, h_8)
    # ThermoProperties_8 = [P_8, Qu_8, s_8, ..._8]


ocalc_8 = RP.REFPROPdll("Ammonia * Water","PH","T;Qmass;S",MASS_BASE_SI,1,0,P_8,h_8,[x_8, 1-x_8])
assert(ocalc_8.ierr == 0)
Temp_8, Qu_8, s_8 = ocalc_8.Output[0:3]
print("Temp_8 = " + "{:.4g}".format(Temp_8) + "; Qu_8 = " + "{:.4g}".format(Qu_8) + "; s_8 = " + "{:.4g}".format(s_8))

print()




# ---------------------------------------
# Solving Mass and Energy Balance
# ---------------------------------------

# 9. Solving energy balance at evaporator (the only one that has an energy balance depending on properties altready available and that results in almost real-life conditions):
print("Step 9:")

    # (source)
    # Q_eva = (m_ponto_6 * h_6) - (m_ponto_5 * h_5)
    # Q_eva = m_ponto_6 * (h_6 - h_5)
    # m_ponto_6 = Q_eva / (h_6 - h_5)
    
    
m_ponto_6 = meb.m_ponto_calc_eva(Q_eva, h_5, h_6)

print("m_ponto_6 = " + "{:.4g}".format(m_ponto_6))
print()



# 10. Apply mass flow rate equality at lines 3, 4 and 5:
print("Step 10:")
    
m_ponto_3 = m_ponto_4 = m_ponto_5 = m_ponto_6

print("m_ponto_3 = " + "{:.4g}".format(m_ponto_3))
print("m_ponto_4 = " + "{:.4g}".format(m_ponto_4))
print("m_ponto_5 = " + "{:.4g}".format(m_ponto_5))
print()



# 11. Apply mass and energy balance in generator (or absorber) with thermodynamic properties and mass flow rate equality from lines 2, 3 and 7 (or 1, 6, and 8):
print("Step 11:")
    
    # In short:
        
        
m_ponto_7 = meb.m_ponto_low_outlet_calc_gen(m_ponto_3, x_2, x_3, x_7)

print("m_ponto_7 = " + "{:.4g}".format(m_ponto_7))
print()
    
    
    # or    
    # m_ponto_8 = external_calc_abs(m_ponto_6, x_1, x_6 and x_8)

        # (remembering)
        # m_ponto_3 = m_ponto_6
        # x_1 = x_2
        # x_3 = x_6
        # x_7 = x_8
    
        # (mass and energy balance at generator)
        # m_ponto_2 = m_ponto_3 + m_ponto_7 # mass balance
        # m_ponto_2 * x_2 = m_ponto_3 * x_3 + m_ponto_7 * x_7 # energy balance
    
        # (first step - I can switch between m_ponto_2 or m_ponto_7 as the unknown)
        # (m_ponto_3 + m_ponto_7) * x_2 = m_ponto_3 * x_3 + m_ponto_7 * x_7
        
        # (second step)
        # m_ponto_3 * x_2 + m_ponto_7 * x_2 = m_ponto_3 * x_3 + m_ponto_7 * x_7
        
        # (third step)
        # m_ponto_7 = m_ponto_3 * (x_3 - x_2) / (x_2 - x_7)
        
        # ----------------
        # Alternate calculation: (mass and balance at absorber - I can switch between m_ponto_1 or m_ponto_8 as the unknown)
        # m_ponto_1 = m_ponto_6 + m_ponto_8
        # m_ponto_1 * x_1 = m_ponto_6 * x_6 + m_ponto_8 * x_8
        
        # (third step)
        # m_ponto_8 = m_ponto_6 * (x_6 - x_1) / (x_1 - x_7)
        # ----------------



# 12. Apply mass flow rate equality to obtain the other mass flow rate:
print("Step 12:")
    
m_ponto_8 = m_ponto_7

print("m_ponto_8 = " + "{:.4g}".format(m_ponto_8))
print()
    

# 13. Apply the mass balance at generator (or absorber) and the mass flow rate equality to solve the other unknown mass flow rate:
print("Step 13:")
    
    # In short:
        
        
m_ponto_2 = meb.m_ponto_inlet_calc_gen(m_ponto_3, m_ponto_7)
    
print("m_ponto_2 = " + "{:.4g}".format(m_ponto_2))
print()
    
    
        # (source)
        # m_ponto_2 = m_ponto_3 + m_ponto_7 # mass balance
    


# 14. Apply mass flow rate equality to obtain the other mass flow rate:
print("Step 14:")
    
m_ponto_1 = m_ponto_2

print("m_ponto_1 = " + "{:.4g}".format(m_ponto_1))
print()
    

# 15. Calculating heat exchange rate at generator and condenser
print("Step 15:")

Q_gen = m_ponto_3 * h_3 + m_ponto_7 * h_7 - m_ponto_2 * h_2 
Q_con = m_ponto_3 * h_3 - m_ponto_4 * h_4
    

print("Q_gen = " + "{:.4g}".format(Q_gen))
print("Q_con = " + "{:.4g}".format(Q_con))

print()



from tabulate import tabulate

table = [
    ['Point', 'Pressure', 'Temperature', 'Ammonia mass \nfraction', 'Vapor \nquality', 'Specific \nenthalpy', 'Specific \nentropy'],
    ['1', '%.4g ' % P_1, '%.4g' % Temp_1, '%.4g' % x_1, '%.4g' % Qu_1, '%.4g' % h_1, '%.4g' % s_1],
    ['2', '%.4g ' % P_2, '%.4g' % Temp_2, '%.4g' % x_2, '%.4g' % Qu_2, '%.4g' % h_2, '%.4g' % s_2],
    ['3', '%.4g ' % P_3, '%.4g' % Temp_3, '%.4g' % x_3, '%.4g' % Qu_3, '%.4g' % h_3, '%.4g' % s_3],
    ['4', '%.4g ' % P_4, '%.4g' % Temp_4, '%.4g' % x_4, '%.4g' % Qu_4, '%.4g' % h_4, '%.4g' % s_4],
    ['5', '%.4g ' % P_5, '%.4g' % Temp_5, '%.4g' % x_5, '%.4g' % Qu_5, '%.4g' % h_5, '%.4g' % s_5],
    ['6', '%.4g ' % P_6, '%.4g' % Temp_6, '%.4g' % x_6, '%.4g' % Qu_6, '%.4g' % h_6, '%.4g' % s_6],
    ['7', '%.4g ' % P_7, '%.4g' % Temp_7, '%.4g' % x_7, '%.4g' % Qu_7, '%.4g' % h_7, '%.4g' % s_7],
    ['8', '%.4g ' % P_8, '%.4g' % Temp_8, '%.4g' % x_8, '%.4g' % Qu_8, '%.4g' % h_8, '%.4g' % s_8],
]
print(tabulate(table, headers='firstrow')) #, tablefmt='grid'))
