#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 12:08:35 2022

@author: Wellorzzon Novais (with Larissa Sobral)
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
The calculation were defined based on energy and mass balance.
"""

"""
Log

--------------------------------------
Version 0.0.1
--
Introduced input data the simple code, operational conditions and pressure equality.
Created based on sheet "Simple Cycle Stepsv2", but some indications of changes were made to create the verison 0.0.2.

TO DO:
    - Check Thermodynamic Properties with RefProp v9.0;
    - Recreate program to accomplish new model in file "Simple Cycle Stepsv3";
    - Introduce csv file from RefProp to be an input to this software.
--------------------------------------


--------------------------------------
Version 0.0.2
--

Created based on sheet "Simple Cycle Stepsv3";
Solving methodology checked with tables from RefProp v9.0 (Specified State Points (variable composition);

TO DO:
    - Introduce csv file from RefProp to be an input to this software.
--------------------------------------


"""

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
Modify --> Temp_7 = Temp_3 = defined by equations #[K] - Temperature in generator low outlet or EV2 inlet
Temp_4 = 313.15 #[K] - Temperature in condenser outlet or EV1 inlet
Temp_6 = 263.15 #[K] - Temperature in evaporator outlet or absorber inlet

Q_eva = 5000 #[W] - Cooling load in evaporator
eff_p = 0.85 # - Thermodynamic pump efficiency

x_1 = x_2 = 0.35 # - Ammonia mass fraction in absorber outlet, pump and generator inlet
x_3 = x_4 = x_5 = x_6 = 0.97 # - Ammonia mass fraction in generator outlet, condenser, EV1, evaporator and absorber inlet
Qu_1 = 0 # - Vapor quality in generator high outlet or condenser inlet
Qu_3 = 1 # - Vapor quality in absorber outlet or pump inlet
Qu_4 = 0 # - Vapor quality in condenser outlet or pump inlet
Qu_6 = 0.9 # - Vapor quality in evaporator outlet or absorber inlet
Qu_7 = 0 # - Vapor quality in generator outlet or EV2 inlet


# call dir and store it in a variable. It stores all the variable names defined before in the form of a list and stores the variable names as a string.
not_my_data = set(dir())
all_initial_properties = set(dir()) - not_my_data
print(all_initial_properties)

# ---------------------------------------
# Solving lines Thermodynamic Properties
# ---------------------------------------


NEED TO UPDATE!! CHANGED Temp_3* to Qu_3*

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
# (To be implemented)

    # Properties from line 1, 3, 4 and 6 have three properties.
    # First solve which has three properties with numbers (excluding Pressure), which are lines 4 and 6:
        External_program_properties(Temp_4, x_4, Qu_4)
        ThermoProperties_4 = [P_4, h_4, s_4, ..._4]
        
        External_program_properties(Temp_6, x_6, Qu_6)
        ThermoProperties_6 = [P_6, h_6, s_6, ..._6]



# 3. Apply pressure equality at lines 1, 2, 3, 5, 7, 8:

    P_2 = P_3 = P_7 = P_4
    P_1 = P_5 = P_8 = P_6 
        
    

# 4. Try to solve the lines that has three properties (with new properties calculated), which are lines 1, 3 and 7:
# (To be implemented)
 
    External_program_properties(P_1, x_1, Qu_1)
    ThermoProperties_1 = [Temp_1, h_1, s_1, ..._1]
    
    External_program_properties(P_3, x_3, Qu_3)
    ThermoProperties_3 = [Temp_3, h_3, s_3, ..._3]
    
    External_program_properties(P_7, x_7, Qu_7)
    ThermoProperties_7 = [Temp_7, h_7, s_7, ..._7]



# 5. Apply isenthalpic expansion valve condition for lines 5 and 7, and try to solve these lines that has three properties (with new properties calculated):
    
    h_5 = h_4
    External_program_properties(P_5, x_5, h_5)
    ThermoProperties_5 = [Temp_5, Qu_5, s_5, ..._5]
    
    h_8 = h_7
    External_program_properties(P_8, x_8, h_8)
    ThermoProperties_8 = [P_8, Qu_8, s_8, ..._8]



# 6. Apply isentropic pump condition for line 2 and try to solve because it has three properties (with new properties calculated):
# (To be implemented)

    s_2 = s_1
    External_program_properties(P_2, x_2, s_2)
    ThermoProperties_2 = [P_2, h_2, Qu_2, ..._2]



# ---------------------------------------
# Solving Mass and Energy Balance
# ---------------------------------------

# 7. Solving energy balance at evaporator (the only one that has an energy balance depending on properties altready available and that results in almost real-life conditions):
# (To be implemented)

    # (source)
    # Q_eva = (m_ponto_6 * h_6) - (m_ponto_5 * h_5)
    # Q_eva = m_ponto_6 * (h_6 - h_5)
    # m_ponto_6 = Q_eva / (h_6 - h_5)
    m_ponto_6 = meb.m_ponto_calc_eva(Q_eva, h_5, h_6)



# 8. Apply mass flow rate equality at lines 3, 4 and 5:
# (To be implemented)
    
    m_ponto_3 = m_ponto_4 = m_ponto_5 = m_ponto_6



# 9. Apply mass and energy balance in generator (or absorber) with thermodynamic properties and mass flow rate equality from lines 2, 3 and 7 (or 1, 6, and 8):
    
    # In short:
    m_ponto_7 = meb.m_ponto_low_outlet_calc_gen(m_ponto_3, x_2, x_3, x_7)
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



# 10. Apply mass flow rate equality to obtain the other mass flow rate:
    
    m_ponto_7 = m_ponto_8
    
    

# 11. Apply the mass balance at generator (or absorber) and the mass flow rate equality to solve the other unknown mass flow rate:
    
    # In short:
    m_ponto_2 = meb.m_ponto_inlet_gen(m_ponto_3, m_ponto_7)
    
        # (source)
        # m_ponto_2 = m_ponto_3 + m_ponto_7 # mass balance
    


# 12. Apply mass flow rate equality to obtain the other mass flow rate:
   
    m_ponto_1 = m_ponto_2
    

# 13. Calculating heat exchange rate at generator and condenser

    Q_gen = m_ponto_3 * h_3 + m_ponto_7 * h_7 - m_ponto_2 * h_2 
    Q_con = m_ponto_3 * h_3 - m_ponto_4 * h_4
    

