#!/bin/python3

# Requirements pip install periodic
# calculates the frequency and wavelength of a photon emitted or absorbed when a hydrogen-like ion changes its quantum state
# requires the user to provide the atomic number of the ion and the principal quantum number of the initial and final states
# tells the user whether the photon is emitted or absorbed.

# Calculate the energy and whether a photon is emitted or absorbed by user entry of initial and final states of an electron

# import libraries
import numpy as np
import periodic
from periodic.table import element # attributes symbol, name, mass, atomic, charge, type

# global variables
screenbreakstring = '_________________________________________________________'
ryd_constant=13.6 # Rydberg constant in eV
plnk_con_eV =4.1357e-15 # Plancks constant in eV
plnk_con_J =6.626e-34 # Plancks constant in J
reduce_plnk_con = plnk_con_J / ( 2 * np.pi)
ryd_constant=13.6 # Rydberg constant in eV
elec_chg_C =-1.602e-19 # Charge of an electron
c = 2.99792458e8 # Speed of Light
l_list = [] # Max range of l values list 
m_list = [] # Max range of m_l values list
spin = ['-1/2','1/2']


# welcome
print 'Calculate the energy and whether a photon is emitted or absorbed by user entry of initial and final states of an electron'

# user entry required for n variable
print screenbreakstring
print 'We need some input from you'
print screenbreakstring

while True:
  n_initial = int(input('Intial state -> What is the principle quantum number [between 1 and 10] :'))
  if n_initial <1 or n_initial > 10:
    print 'Initial n state out of range, try again: '
  else:
    break

while True:
  n_final = int(input('Final state -> What is the principle quantum number [between 1 and 10] :'))
  if n_final < 1 or n_final > 10:
    print 'Final n state out of range, try again: '
  else:
    break

while True:
  atom_num = int(input('Atomic number -> enter the atomic number of the ion [valid periodic table number] :'))
  if atom_num < 1 or atom_num > 118: # unable to validate against range via != ptble_rng - look into this!
    print 'Invalid atomic number, try again: '
  else:
    break

#calculate energy values
def e_val(n):
  e_val = - ryd_constant/(n*n)
  return e_val


def energy_total(initial_e,final_e):
  e_photon = final_e - initial_e  
  return e_photon
  
def wave_from_e(e):
  h = plnk_con_J
  lamda = abs((h * c) / convert_e(e))
  return lamda

def photon_freq(lam):
  pho_fre = abs(c / lam)
  return pho_fre

def convert_e(eJ): # convert energy from eV to J
  e_J = elec_chg_C * eJ
  return e_J

def emit_abso(e_v):
  if e_v < 0:
    in_out = 'absorbed'
  else:
    in_out = 'emitted'
  return in_out

## Final Outputs
e_ni = e_val(n_initial) # initial energy value
e_nf = e_val(n_final) # final energy value
photon_e = energy_total(e_ni,e_nf)
photon_lam = wave_from_e(photon_e)
photon_f = photon_freq(photon_lam)
loss_gain = emit_abso(photon_e)
#element_meta(atom_num)
ele = element(atom_num)
ele_name = ele.name
ele_sym = ele.symbol
ele_mass = ele.mass
k = 2 * np.pi / abs((plnk_con_J * c) / photon_e)
p = reduce_plnk_con / k 

# outputs
print 'You entered the atomic number',atom_num,' and this is ',ele_sym,' being ',ele_name,' with atomic mass ',ele_mass
print 'The energy value of your intitial n state ', n_initial,': ', e_ni,'eV'
print 'The energy value of your final n state ',n_final,': ', e_nf,'eV'
print 'The wave number being ',k,' with momentum ', p
print 'The photon engery of moving from intial to final :', photon_e, 'eV, this photon being ',loss_gain
print 'The wavelength of this photon energy value being :', photon_lam, 'm'
print 'The frequency of this photon energy value being :', photon_f, 'Hz'
print 'Here are all the possible quantum states at your final value of n:'
print screenbreakstring
print 'n =',n_final,'|  l = 0  | m_l =  0 | m_s =  -1/2 |'
print 'n =',n_final,'|  l = 0  | m_l =  0 | m_s =   1/2 |'

# Max Range of l
l_list = range(0,int(n_final))
l_total = len(l_list)

for l in l_list:
  m_list = range(-l,l)
  m_total = len(m_list)
  for m in m_list:
    if int(m) < 0:
      print 'n =',n_final,'|  l =',l,' | m_l =',m,'| m_s =',spin[0],' |'
      print 'n =',n_final,'|  l =',l,' | m_l =',m,'| m_s = ',spin[1],' |'
    else:
      print 'n =',n_final,'|  l =',l,' | m_l = ',m,'| m_s =',spin[0],' |'
      print 'n =',n_final,'|  l =',l,' | m_l = ',m,'| m_s =',spin[1],' |'

# Total quantum states 
qstate = (l_total * m_total)+2

# End
print screenbreakstring
print 'there are a total of ',qstate,' quantum states for n = ',n_final
print screenbreakstring
print 'Heres the periodic table just for reference:'
print periodic.table
print screenbreakstring
print 'bye!'
print screenbreakstring
print screenbreakstring
print screenbreakstring
