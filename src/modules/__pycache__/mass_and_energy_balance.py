#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 14:49:55 2022

@author: Wellorzzon Novais (with Larissa Sobral)
"""

"""
Description
--
This code has useful equations to solve mass and energy balance for components of a simplified absorption refrigeration cycle, which includes:
    - 1 condenser
    - 1 generator
    - 1 evaporator
    - 1 absorber
    - 1 pump
    - 2 expansion valves
"""

"""
Log

--------------------------------------
Version 0.0.1
--
Introduced simple equations for generator, absorber and evaporator.

TO DO:
    - I;

--------------------------------------
"""

def m_ponto_calc_eva(Q_eva,h_inlet,h_outlet):
    # (source)
    # Q_eva = (m_ponto_outlet * h_outlet) - (m_ponto_inlet * h_inlet)
    # Q_eva = m_ponto_eva * (h_outlet - h_inlet)
    m_ponto_eva = Q_eva / (h_outlet - h_inlet)
    return m_ponto_eva


def m_ponto_low_outlet_calc_gen(m_ponto_high_outlet, x_inlet, x_high_outlet, x_low_outlet):
    # (remembering for generator [or absorver])
    # m_ponto_high_outlet = m_ponto_3 [or m_ponto_6]
    # x_2 [or x_1] = x_inlet
    # x_high_outlet = x_3 [or x_6]
    # x_low_outlet = x_7 [or x_8]

    # (mass and energy balance at generator)
    # m_ponto_inlet = m_ponto_high_outlet + m_ponto_low_outlet # mass balance
    # m_ponto_inlet * x_inlet = m_ponto_high_outlet * x_high_outlet + m_ponto_low_outlet * x_low_outlet # energy balance

    # (first step - I can switch between m_ponto_inlet or m_ponto_low_outlet as the unknown)
    # (m_ponto_high_outlet + m_ponto__low_outlet) * x_inlet = m_ponto_high_outlet * x_high_outlet + m_ponto_low_outlet * x_low_outlet
    
    # (second step)
    # m_ponto_high_outlet * x_inlet + m_ponto_low_outlet * x_inlet = m_ponto_high_outlet * x_high_outlet + m_ponto_low_outlet * x_low_outlet
    
    # (third step)
    # m_ponto_low_outlet = m_ponto_high_outlet * (x_high_outlet - x_inlet) / (x_inlet - x_low_outlet)
    m_ponto_low_outlet_gen = m_ponto_high_outlet * (x_high_outlet - x_inlet) / (x_inlet - x_low_outlet)
    return m_ponto_low_outlet_gen


def m_ponto_inlet_calc_gen(m_ponto_high_outlet, m_ponto_low_outlet):
    # (source)
    # m_ponto_2 = m_ponto_3 + m_ponto_7 # mass balance
    m_ponto_inlet_gen = m_ponto_high_outlet + m_ponto_low_outlet
    return m_ponto_inlet_gen






