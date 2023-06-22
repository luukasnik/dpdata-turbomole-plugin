import numpy as np
from .unit import LengthConversion, EnergyConversion, ForceConversion
from .periodic_table import ELEMENTS

length_convert = LengthConversion("bohr", "angstrom").value()
energy_convert = EnergyConversion("hartree", "eV").value()
force_convert = ForceConversion("hartree/bohr", "eV/angstrom").value()

symbols = ["X"] + ELEMENTS


def to_system_data(file_name, md=False):
    data = {}
    # read from log lines
    energy_t = []
    coords_t = []
    atom_symbols = []
    forces_t = []
    forces = []
    coords = []

    with open(file_name) as fp:
        for line in fp:
            if line.strip().startswith("$grad"):
                continue
            if line.strip().startswith("$end"):
                forces_t.append(forces)
                energy_t.append(energy)
                coords_t.append(coords)
                forces = []
                coords = []
                break
            if line.strip().startswith("cycle =      1"):
                energy = float(line.split()[6].replace('D', 'E'))
                continue
            elif line.strip().startswith("cycle"):
                forces_t.append(forces)
                energy_t.append(energy)
                coords_t.append(coords)
                forces = []
                coords = []
                atom_symbols = []
                energy = float(line.split()[6].replace('D', 'E'))
                continue
            s = line.split()
            try:
                atom_symbols.append(s[3].upper())
                coords.append([float(x.replace('D', 'E')) for x in s[0:3]])
            except:
                forces.append([float(s[0].replace('D', 'E')), float(
                    s[1].replace('D', 'E')), float(s[2].replace('D', 'E'))])
    assert(coords_t), "cannot find coords"
    assert(energy_t), "cannot find energies"
    assert(forces_t), "cannot find forces"

    atom_names, data['atom_types'], atom_numbs = np.unique(
        atom_symbols, return_inverse=True, return_counts=True)
    data['atom_names'] = list(atom_names)
    data['atom_numbs'] = list(atom_numbs)
    if not md:
        forces_t = forces_t[-1:]
        energy_t = energy_t[-1:]
        coords_t = coords_t[-1:]
    data['forces'] = np.array(forces_t) * -force_convert
    data['energies'] = np.array(energy_t) * energy_convert
    data['coords'] = np.array(coords_t) * length_convert
    data['orig'] = np.array([0, 0, 0])
    data['cells'] = np.array(
        [[[100., 0., 0.], [0., 100., 0.], [0., 0., 100.]] for _ in energy_t])
    data['nopbc'] = True
    return data
