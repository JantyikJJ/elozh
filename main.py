import os
import numpy
import math
import matplotlib.pyplot as plt


def main():
    baseline_filename = get_file_in("Kérem az alapvonal fájl elérési helyét: ")
    cuvette_filename = get_file_in("Kérem a küvetta fájl elérési helyét: ")
    measurement_files = []
    output_files = []
    get_n_input(measurement_files, output_files)
    wavelengths = []
    corrections = []
    get_real_num_array(wavelengths, corrections)
    time_correction = get_real_num("Kérem adja meg az idő korrekciót! Ha nem kíván megadni, írjon be, hogy cancel: ",
                                   "cancel")

    baseline = numpy.loadtxt(baseline_filename, delimiter=";", skiprows=2)
    cuvette = numpy.loadtxt(cuvette_filename, delimiter=";", skiprows=2)
    matrices = []
    for i in range(len(measurement_files)):
        matrix = numpy.loadtxt(measurement_files[i], delimiter=";", skiprows=2)
        for l in range(len(wavelengths)):
            for m in range(matrix.shape[0]):
                if matrix[m, 0] == wavelengths[l]:
                    sub_matrix = matrix[m][1:]
                    nx = math.sqrt(len(sub_matrix))
                    sub_matrix = sub_matrix.reshape(nx, nx)
                    sub_matrix = numpy.transpose(sub_matrix)

                    baseline_index = 0
                    for x in range(baseline.shape[0]):
                        if baseline[baseline_index, 0] == matrix[m, 0]:
                            baseline_index = x
                            break
                    sub_baseline = baseline[baseline_index][1:]
                    sub_baseline = sub_baseline.reshape(nx, nx)

                    corr = 0
                    if len(corrections) > 0:
                        corr = corrections[l]

                    for j in range(sub_matrix.shape[0]):
                        cuvette_index = 0
                        for x in range(cuvette.shape[0]):
                            if cuvette[x, 0] == matrix[m, 0]:
                                cuvette_index = x
                                break
                        cuv_avg = ((cuvette[cuvette_index, 1] + cuvette[cuvette_index, 2]) / 2)

                        for k in range(sub_matrix.shape[1]):
                            if k == 0 and time_correction is not None:
                                sub_matrix[j, k] -= time_correction

                            sub_matrix[j, k] -= corr

                            if j != 0 and k != 0:
                                sub_matrix[j, k] -= sub_baseline[j, k]
                                sub_matrix[j, k] -= cuv_avg

                    matrices.append(sub_matrix)
                    save_filename = output_files[i]
                    file_obj = open(save_filename, 'a')
                    arr_obj = sub_matrix.flatten()
                    numpy.insert(arr_obj, 0, matrix[l][0])
                    file_obj.write("\n" + numpy.array2string(arr_obj, precision=6, separator=";"))
                    break


def get_file_in(text, cancel=None):
    file_name = input(text)
    if cancel is not None and file_name == cancel:
        return None
    elif os.path.isfile(file_name):
        return file_name
    else:
        print("Hibás bemenet! Kérem adjon meg egy létező fájlt!")
        return get_file_in(text, cancel)


def get_real_num_array(arr1, arr2):
    wavelength = get_real_num("Kérek egy vizsgálandó hullámhosszat: ")
    while wavelength is not None:
        arr1.append(wavelength)
        wavelength = get_real_num("Kérem a következő vizsgálandó hullámhosszat! Ha nincs következő, akkor nyomjon egy "
                                  "entert érték nélkül: ", "")
    wavelength_len = len(arr1)
    for i in range(wavelength_len):
        num = get_real_num(f"Kérek egy abszorbancia korrekciót ({i}/{wavelength_len})! Ha nem szeretne korrekciót "
                           f"megadni egyáltalán, írja be, hogy cancel: ", "cancel")
        if num is None:
            arr2.clear()
            break
        else:
            arr2.append(num)


def get_real_num(text, cancel=None):
    inp = input(text)
    if cancel is not None and inp == cancel:
        return None
    try:
        return float(inp)
    except ValueError:
        print("Hibás bemenet! Kérem egy valós számot adjon meg!");
        return get_real_num(text, cancel)


def get_n_input(arr1, arr2):
    file_name = get_file_in("Kérem írjon be egy mérési fájl nevet: ")
    while file_name is not None:
        arr1.append(file_name)
        file_name = get_file_in("Kérem a következő mérési fájl nevet! Ha nem szeretne többet megadni, írja be, "
                                "hogy cancel: ", "cancel")
    alen = len(arr1)
    for i in range(alen):
        file_name = input(f"Kérem a következő kimeneti fájl nevet ({i}/{alen}): ")
        arr2.append(file_name)


main()
