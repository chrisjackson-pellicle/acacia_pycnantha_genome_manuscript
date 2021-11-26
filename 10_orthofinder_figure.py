# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 12:10:01 2017

@author: david

This code creates all the individual plots for a specific dataset.

Modified Chris Jackson 2021 chris.jackson@rbg.vic.gov.au

"""
import os
# import ete2
import ete3
import csv
import numpy as np
from collections import defaultdict
import matplotlib
import matplotlib.pyplot as plt
import svgwrite

matplotlib.rcParams['pdf.fonttype'] = 'truetype'

""" Data to create unbiased heatmaps"""
cmaps = {}
qReverse = False
qColor = True

d_hot = [[0.0225, 0.0121, 0.0121], [0.0363, 0.0154, 0.0154], [0.0493, 0.0188, 0.0188], [0.0604, 0.0221, 0.0221],
         [0.0708, 0.0252, 0.0252], [0.0809, 0.0279, 0.0279], [0.0909, 0.0303, 0.0303], [0.1006, 0.0322, 0.0322],
         [0.1103, 0.0338, 0.0338], [0.1199, 0.0349, 0.0349], [0.1294, 0.0357, 0.0357], [0.1388, 0.036, 0.036],
         [0.1488, 0.0353, 0.0358], [0.1595, 0.0335, 0.0353], [0.1708, 0.0302, 0.0344], [0.182, 0.0264, 0.033],
         [0.1927, 0.0225, 0.0311], [0.2028, 0.0186, 0.0287], [0.2124, 0.0147, 0.0257], [0.2214, 0.0112, 0.0222],
         [0.2297, 0.0083, 0.018], [0.2374, 0.0062, 0.0134], [0.245, 0.0041, 0.0086], [0.2526, 0.002, 0.004],
         [0.2602, 0.0002, 0.0], [0.2685, 0.0023, 0.0], [0.2766, 0.0041, 0.0], [0.2847, 0.0057, 0.0],
         [0.2928, 0.0071, 0.0], [0.3007, 0.0083, 0.0], [0.3086, 0.0093, 0.0], [0.3165, 0.01, 0.0],
         [0.3243, 0.0106, 0.0], [0.332, 0.0109, 0.0], [0.3397, 0.011, 0.0], [0.3474, 0.011, 0.0], [0.3551, 0.0107, 0.0],
         [0.3627, 0.0102, 0.0], [0.3703, 0.0095, 0.0], [0.3779, 0.0086, 0.0], [0.3854, 0.0074, 0.0],
         [0.393, 0.0061, 0.0], [0.4005, 0.0046, 0.0], [0.408, 0.0028, 0.0], [0.4155, 0.0009, 0.0],
         [0.4231, 0.0, 0.0013], [0.4309, 0.0, 0.0037], [0.4386, 0.0, 0.0063], [0.4463, 0.0, 0.0091],
         [0.454, 0.0, 0.0121], [0.4618, 0.0, 0.0153], [0.4695, 0.0, 0.0188], [0.4772, 0.0, 0.0224],
         [0.485, 0.0, 0.0263], [0.4927, 0.0, 0.0304], [0.5005, 0.0, 0.0347], [0.5083, 0.0, 0.0392],
         [0.516, 0.0, 0.0437], [0.5238, 0.0, 0.0482], [0.5316, 0.0, 0.0526], [0.5394, 0.0, 0.057],
         [0.5472, 0.0, 0.0612], [0.555, 0.0, 0.0654], [0.5628, 0.0, 0.0696], [0.5706, 0.0, 0.0737],
         [0.5784, 0.0, 0.0778], [0.5863, 0.0, 0.0818], [0.5941, 0.0, 0.0858], [0.602, 0.0, 0.0898],
         [0.6098, 0.0, 0.0937], [0.6177, 0.0, 0.0976], [0.6256, 0.0, 0.1015], [0.6335, 0.0, 0.1053],
         [0.6414, 0.0, 0.109], [0.6493, 0.0, 0.1126], [0.6572, 0.0, 0.1163], [0.6651, 0.0, 0.1198],
         [0.6731, 0.0, 0.1233], [0.681, 0.0, 0.1268], [0.689, 0.0, 0.1303], [0.6969, 0.0, 0.1337],
         [0.7049, 0.0, 0.1371], [0.7129, 0.0, 0.1404], [0.7209, 0.0, 0.1437], [0.7289, 0.0, 0.147],
         [0.7369, 0.0, 0.1503], [0.745, 0.0, 0.1535], [0.753, 0.0, 0.1567], [0.7611, 0.0, 0.1599], [0.7691, 0.0, 0.163],
         [0.7772, 0.0, 0.1662], [0.7853, 0.0, 0.1693], [0.7934, 0.0, 0.1724], [0.8015, 0.0, 0.1755],
         [0.8096, 0.0, 0.1785], [0.8177, 0.0, 0.1816], [0.8213, 0.0, 0.1792], [0.8249, 0.0, 0.1767],
         [0.8286, 0.0, 0.174], [0.8322, 0.0, 0.1712], [0.8357, 0.0, 0.168], [0.839, 0.0, 0.1643], [0.8422, 0.0, 0.16],
         [0.8452, 0.0, 0.1552], [0.848, 0.0, 0.1497], [0.8507, 0.0, 0.1434], [0.8531, 0.0, 0.1362],
         [0.8554, 0.0, 0.1279], [0.8574, 0.0, 0.1184], [0.8593, 0.0, 0.1072], [0.8609, 0.0, 0.0939],
         [0.8624, 0.0, 0.0776], [0.8636, 0.0, 0.0565], [0.8646, 0.0, 0.0264], [0.8657, 0.0077, 0.0],
         [0.8678, 0.0437, 0.0], [0.8698, 0.073, 0.0], [0.8715, 0.096, 0.0], [0.8732, 0.1158, 0.0],
         [0.8747, 0.1336, 0.0], [0.8761, 0.1499, 0.0], [0.8773, 0.1652, 0.0], [0.8784, 0.1796, 0.0],
         [0.8794, 0.1934, 0.0], [0.8802, 0.2066, 0.0], [0.8809, 0.2194, 0.0], [0.8814, 0.2317, 0.0],
         [0.8818, 0.2438, 0.0], [0.8821, 0.2555, 0.0], [0.8823, 0.2669, 0.0], [0.8823, 0.2781, 0.0],
         [0.8823, 0.2891, 0.0], [0.8821, 0.2999, 0.0], [0.8818, 0.3105, 0.0], [0.8814, 0.321, 0.0],
         [0.8809, 0.3312, 0.0], [0.8802, 0.3414, 0.0], [0.8795, 0.3514, 0.0], [0.8787, 0.3613, 0.0],
         [0.8778, 0.371, 0.0], [0.8768, 0.3807, 0.0], [0.8757, 0.3902, 0.0], [0.8745, 0.3996, 0.0],
         [0.8733, 0.409, 0.0], [0.872, 0.4182, 0.0], [0.8706, 0.4273, 0.0], [0.8691, 0.4364, 0.0],
         [0.8675, 0.4454, 0.0], [0.8659, 0.4542, 0.0], [0.8643, 0.463, 0.0], [0.8625, 0.4718, 0.0],
         [0.8607, 0.4804, 0.0], [0.8589, 0.489, 0.0], [0.857, 0.4975, 0.0], [0.8551, 0.5059, 0.0],
         [0.8531, 0.5143, 0.0], [0.851, 0.5226, 0.0], [0.8489, 0.5309, 0.0], [0.8468, 0.5391, 0.0],
         [0.8446, 0.5472, 0.0], [0.8424, 0.5552, 0.0], [0.8402, 0.5633, 0.0], [0.8379, 0.5712, 0.0],
         [0.8356, 0.5791, 0.0], [0.8332, 0.587, 0.0], [0.8309, 0.5948, 0.0], [0.8285, 0.6025, 0.0],
         [0.826, 0.6102, 0.0], [0.8236, 0.6179, 0.0], [0.8211, 0.6255, 0.0], [0.8186, 0.6331, 0.0],
         [0.8161, 0.6406, 0.0], [0.8135, 0.6481, 0.0], [0.8109, 0.6555, 0.0], [0.8083, 0.6629, 0.0],
         [0.8057, 0.6702, 0.0], [0.8031, 0.6776, 0.0], [0.8004, 0.6849, 0.0], [0.7978, 0.6921, 0.0],
         [0.7951, 0.6993, 0.0], [0.7924, 0.7065, 0.0], [0.7897, 0.7136, 0.0], [0.787, 0.7208, 0.0],
         [0.7842, 0.7278, 0.0], [0.7815, 0.7349, 0.0], [0.7787, 0.7419, 0.0], [0.7759, 0.7489, 0.0],
         [0.7731, 0.7559, 0.0], [0.7703, 0.7628, 0.0], [0.7675, 0.7697, 0.0], [0.7647, 0.7766, 0.0],
         [0.7618, 0.7835, 0.0], [0.7659, 0.787, 0.0], [0.7699, 0.7906, 0.0], [0.7739, 0.7941, 0.0],
         [0.7778, 0.7975, 0.0], [0.7816, 0.8009, 0.0], [0.7854, 0.8041, 0.0], [0.789, 0.8072, 0.0],
         [0.7925, 0.8102, 0.0], [0.7959, 0.813, 0.0], [0.7991, 0.8157, 0.0], [0.8022, 0.8182, 0.0],
         [0.8052, 0.8206, 0.0], [0.8079, 0.8228, 0.0], [0.8105, 0.8248, 0.0], [0.8129, 0.8266, 0.0],
         [0.815, 0.8282, 0.0], [0.817, 0.8296, 0.0], [0.8189, 0.8309, 0.0043], [0.8235, 0.8349, 0.0687],
         [0.8281, 0.8389, 0.1109], [0.8326, 0.8429, 0.144], [0.8372, 0.8468, 0.1726], [0.8417, 0.8508, 0.1987],
         [0.8462, 0.8547, 0.223], [0.8507, 0.8586, 0.2461], [0.8551, 0.8625, 0.2684], [0.8595, 0.8664, 0.2899],
         [0.8639, 0.8703, 0.3109], [0.8682, 0.8742, 0.3315], [0.8725, 0.8781, 0.3518], [0.8768, 0.8819, 0.3718],
         [0.8811, 0.8857, 0.3917], [0.8853, 0.8896, 0.4113], [0.8895, 0.8934, 0.4308], [0.8936, 0.8972, 0.4502],
         [0.8977, 0.9009, 0.4695], [0.9018, 0.9047, 0.4887], [0.9059, 0.9084, 0.5078], [0.9099, 0.9122, 0.5269],
         [0.9138, 0.9159, 0.546], [0.9178, 0.9196, 0.565], [0.9217, 0.9233, 0.584], [0.9256, 0.9269, 0.6029],
         [0.9294, 0.9306, 0.6219], [0.9332, 0.9342, 0.6408], [0.937, 0.9379, 0.6597], [0.9407, 0.9415, 0.6786],
         [0.9444, 0.945, 0.6976], [0.9481, 0.9486, 0.7165], [0.9518, 0.9522, 0.7354], [0.9554, 0.9557, 0.7543],
         [0.959, 0.9592, 0.7732], [0.9625, 0.9627, 0.7921], [0.9661, 0.9662, 0.811], [0.9696, 0.9697, 0.8299],
         [0.973, 0.9731, 0.8488], [0.9765, 0.9766, 0.8677], [0.9799, 0.98, 0.8866], [0.9833, 0.9834, 0.9055],
         [0.9867, 0.9867, 0.9244], [0.9901, 0.9901, 0.9433], [0.9934, 0.9934, 0.9622], [0.9967, 0.9967, 0.9811],
         [1.0, 1.0, 1.0]]
n = len(d_hot)

_plasma_data = [[0.050383, 0.029803, 0.527975],
                [0.063536, 0.028426, 0.533124],
                [0.075353, 0.027206, 0.538007],
                [0.086222, 0.026125, 0.542658],
                [0.096379, 0.025165, 0.547103],
                [0.105980, 0.024309, 0.551368],
                [0.115124, 0.023556, 0.555468],
                [0.123903, 0.022878, 0.559423],
                [0.132381, 0.022258, 0.563250],
                [0.140603, 0.021687, 0.566959],
                [0.148607, 0.021154, 0.570562],
                [0.156421, 0.020651, 0.574065],
                [0.164070, 0.020171, 0.577478],
                [0.171574, 0.019706, 0.580806],
                [0.178950, 0.019252, 0.584054],
                [0.186213, 0.018803, 0.587228],
                [0.193374, 0.018354, 0.590330],
                [0.200445, 0.017902, 0.593364],
                [0.207435, 0.017442, 0.596333],
                [0.214350, 0.016973, 0.599239],
                [0.221197, 0.016497, 0.602083],
                [0.227983, 0.016007, 0.604867],
                [0.234715, 0.015502, 0.607592],
                [0.241396, 0.014979, 0.610259],
                [0.248032, 0.014439, 0.612868],
                [0.254627, 0.013882, 0.615419],
                [0.261183, 0.013308, 0.617911],
                [0.267703, 0.012716, 0.620346],
                [0.274191, 0.012109, 0.622722],
                [0.280648, 0.011488, 0.625038],
                [0.287076, 0.010855, 0.627295],
                [0.293478, 0.010213, 0.629490],
                [0.299855, 0.009561, 0.631624],
                [0.306210, 0.008902, 0.633694],
                [0.312543, 0.008239, 0.635700],
                [0.318856, 0.007576, 0.637640],
                [0.325150, 0.006915, 0.639512],
                [0.331426, 0.006261, 0.641316],
                [0.337683, 0.005618, 0.643049],
                [0.343925, 0.004991, 0.644710],
                [0.350150, 0.004382, 0.646298],
                [0.356359, 0.003798, 0.647810],
                [0.362553, 0.003243, 0.649245],
                [0.368733, 0.002724, 0.650601],
                [0.374897, 0.002245, 0.651876],
                [0.381047, 0.001814, 0.653068],
                [0.387183, 0.001434, 0.654177],
                [0.393304, 0.001114, 0.655199],
                [0.399411, 0.000859, 0.656133],
                [0.405503, 0.000678, 0.656977],
                [0.411580, 0.000577, 0.657730],
                [0.417642, 0.000564, 0.658390],
                [0.423689, 0.000646, 0.658956],
                [0.429719, 0.000831, 0.659425],
                [0.435734, 0.001127, 0.659797],
                [0.441732, 0.001540, 0.660069],
                [0.447714, 0.002080, 0.660240],
                [0.453677, 0.002755, 0.660310],
                [0.459623, 0.003574, 0.660277],
                [0.465550, 0.004545, 0.660139],
                [0.471457, 0.005678, 0.659897],
                [0.477344, 0.006980, 0.659549],
                [0.483210, 0.008460, 0.659095],
                [0.489055, 0.010127, 0.658534],
                [0.494877, 0.011990, 0.657865],
                [0.500678, 0.014055, 0.657088],
                [0.506454, 0.016333, 0.656202],
                [0.512206, 0.018833, 0.655209],
                [0.517933, 0.021563, 0.654109],
                [0.523633, 0.024532, 0.652901],
                [0.529306, 0.027747, 0.651586],
                [0.534952, 0.031217, 0.650165],
                [0.540570, 0.034950, 0.648640],
                [0.546157, 0.038954, 0.647010],
                [0.551715, 0.043136, 0.645277],
                [0.557243, 0.047331, 0.643443],
                [0.562738, 0.051545, 0.641509],
                [0.568201, 0.055778, 0.639477],
                [0.573632, 0.060028, 0.637349],
                [0.579029, 0.064296, 0.635126],
                [0.584391, 0.068579, 0.632812],
                [0.589719, 0.072878, 0.630408],
                [0.595011, 0.077190, 0.627917],
                [0.600266, 0.081516, 0.625342],
                [0.605485, 0.085854, 0.622686],
                [0.610667, 0.090204, 0.619951],
                [0.615812, 0.094564, 0.617140],
                [0.620919, 0.098934, 0.614257],
                [0.625987, 0.103312, 0.611305],
                [0.631017, 0.107699, 0.608287],
                [0.636008, 0.112092, 0.605205],
                [0.640959, 0.116492, 0.602065],
                [0.645872, 0.120898, 0.598867],
                [0.650746, 0.125309, 0.595617],
                [0.655580, 0.129725, 0.592317],
                [0.660374, 0.134144, 0.588971],
                [0.665129, 0.138566, 0.585582],
                [0.669845, 0.142992, 0.582154],
                [0.674522, 0.147419, 0.578688],
                [0.679160, 0.151848, 0.575189],
                [0.683758, 0.156278, 0.571660],
                [0.688318, 0.160709, 0.568103],
                [0.692840, 0.165141, 0.564522],
                [0.697324, 0.169573, 0.560919],
                [0.701769, 0.174005, 0.557296],
                [0.706178, 0.178437, 0.553657],
                [0.710549, 0.182868, 0.550004],
                [0.714883, 0.187299, 0.546338],
                [0.719181, 0.191729, 0.542663],
                [0.723444, 0.196158, 0.538981],
                [0.727670, 0.200586, 0.535293],
                [0.731862, 0.205013, 0.531601],
                [0.736019, 0.209439, 0.527908],
                [0.740143, 0.213864, 0.524216],
                [0.744232, 0.218288, 0.520524],
                [0.748289, 0.222711, 0.516834],
                [0.752312, 0.227133, 0.513149],
                [0.756304, 0.231555, 0.509468],
                [0.760264, 0.235976, 0.505794],
                [0.764193, 0.240396, 0.502126],
                [0.768090, 0.244817, 0.498465],
                [0.771958, 0.249237, 0.494813],
                [0.775796, 0.253658, 0.491171],
                [0.779604, 0.258078, 0.487539],
                [0.783383, 0.262500, 0.483918],
                [0.787133, 0.266922, 0.480307],
                [0.790855, 0.271345, 0.476706],
                [0.794549, 0.275770, 0.473117],
                [0.798216, 0.280197, 0.469538],
                [0.801855, 0.284626, 0.465971],
                [0.805467, 0.289057, 0.462415],
                [0.809052, 0.293491, 0.458870],
                [0.812612, 0.297928, 0.455338],
                [0.816144, 0.302368, 0.451816],
                [0.819651, 0.306812, 0.448306],
                [0.823132, 0.311261, 0.444806],
                [0.826588, 0.315714, 0.441316],
                [0.830018, 0.320172, 0.437836],
                [0.833422, 0.324635, 0.434366],
                [0.836801, 0.329105, 0.430905],
                [0.840155, 0.333580, 0.427455],
                [0.843484, 0.338062, 0.424013],
                [0.846788, 0.342551, 0.420579],
                [0.850066, 0.347048, 0.417153],
                [0.853319, 0.351553, 0.413734],
                [0.856547, 0.356066, 0.410322],
                [0.859750, 0.360588, 0.406917],
                [0.862927, 0.365119, 0.403519],
                [0.866078, 0.369660, 0.400126],
                [0.869203, 0.374212, 0.396738],
                [0.872303, 0.378774, 0.393355],
                [0.875376, 0.383347, 0.389976],
                [0.878423, 0.387932, 0.386600],
                [0.881443, 0.392529, 0.383229],
                [0.884436, 0.397139, 0.379860],
                [0.887402, 0.401762, 0.376494],
                [0.890340, 0.406398, 0.373130],
                [0.893250, 0.411048, 0.369768],
                [0.896131, 0.415712, 0.366407],
                [0.898984, 0.420392, 0.363047],
                [0.901807, 0.425087, 0.359688],
                [0.904601, 0.429797, 0.356329],
                [0.907365, 0.434524, 0.352970],
                [0.910098, 0.439268, 0.349610],
                [0.912800, 0.444029, 0.346251],
                [0.915471, 0.448807, 0.342890],
                [0.918109, 0.453603, 0.339529],
                [0.920714, 0.458417, 0.336166],
                [0.923287, 0.463251, 0.332801],
                [0.925825, 0.468103, 0.329435],
                [0.928329, 0.472975, 0.326067],
                [0.930798, 0.477867, 0.322697],
                [0.933232, 0.482780, 0.319325],
                [0.935630, 0.487712, 0.315952],
                [0.937990, 0.492667, 0.312575],
                [0.940313, 0.497642, 0.309197],
                [0.942598, 0.502639, 0.305816],
                [0.944844, 0.507658, 0.302433],
                [0.947051, 0.512699, 0.299049],
                [0.949217, 0.517763, 0.295662],
                [0.951344, 0.522850, 0.292275],
                [0.953428, 0.527960, 0.288883],
                [0.955470, 0.533093, 0.285490],
                [0.957469, 0.538250, 0.282096],
                [0.959424, 0.543431, 0.278701],
                [0.961336, 0.548636, 0.275305],
                [0.963203, 0.553865, 0.271909],
                [0.965024, 0.559118, 0.268513],
                [0.966798, 0.564396, 0.265118],
                [0.968526, 0.569700, 0.261721],
                [0.970205, 0.575028, 0.258325],
                [0.971835, 0.580382, 0.254931],
                [0.973416, 0.585761, 0.251540],
                [0.974947, 0.591165, 0.248151],
                [0.976428, 0.596595, 0.244767],
                [0.977856, 0.602051, 0.241387],
                [0.979233, 0.607532, 0.238013],
                [0.980556, 0.613039, 0.234646],
                [0.981826, 0.618572, 0.231287],
                [0.983041, 0.624131, 0.227937],
                [0.984199, 0.629718, 0.224595],
                [0.985301, 0.635330, 0.221265],
                [0.986345, 0.640969, 0.217948],
                [0.987332, 0.646633, 0.214648],
                [0.988260, 0.652325, 0.211364],
                [0.989128, 0.658043, 0.208100],
                [0.989935, 0.663787, 0.204859],
                [0.990681, 0.669558, 0.201642],
                [0.991365, 0.675355, 0.198453],
                [0.991985, 0.681179, 0.195295],
                [0.992541, 0.687030, 0.192170],
                [0.993032, 0.692907, 0.189084],
                [0.993456, 0.698810, 0.186041],
                [0.993814, 0.704741, 0.183043],
                [0.994103, 0.710698, 0.180097],
                [0.994324, 0.716681, 0.177208],
                [0.994474, 0.722691, 0.174381],
                [0.994553, 0.728728, 0.171622],
                [0.994561, 0.734791, 0.168938],
                [0.994495, 0.740880, 0.166335],
                [0.994355, 0.746995, 0.163821],
                [0.994141, 0.753137, 0.161404],
                [0.993851, 0.759304, 0.159092],
                [0.993482, 0.765499, 0.156891],
                [0.993033, 0.771720, 0.154808],
                [0.992505, 0.777967, 0.152855],
                [0.991897, 0.784239, 0.151042],
                [0.991209, 0.790537, 0.149377],
                [0.990439, 0.796859, 0.147870],
                [0.989587, 0.803205, 0.146529],
                [0.988648, 0.809579, 0.145357],
                [0.987621, 0.815978, 0.144363],
                [0.986509, 0.822401, 0.143557],
                [0.985314, 0.828846, 0.142945],
                [0.984031, 0.835315, 0.142528],
                [0.982653, 0.841812, 0.142303],
                [0.981190, 0.848329, 0.142279],
                [0.979644, 0.854866, 0.142453],
                [0.977995, 0.861432, 0.142808],
                [0.976265, 0.868016, 0.143351],
                [0.974443, 0.874622, 0.144061],
                [0.972530, 0.881250, 0.144923],
                [0.970533, 0.887896, 0.145919],
                [0.968443, 0.894564, 0.147014],
                [0.966271, 0.901249, 0.148180],
                [0.964021, 0.907950, 0.149370],
                [0.961681, 0.914672, 0.150520],
                [0.959276, 0.921407, 0.151566],
                [0.956808, 0.928152, 0.152409],
                [0.954287, 0.934908, 0.152921],
                [0.951726, 0.941671, 0.152925],
                [0.949151, 0.948435, 0.152178],
                [0.946602, 0.955190, 0.150328],
                [0.944152, 0.961916, 0.146861],
                [0.941896, 0.968590, 0.140956],
                [0.940015, 0.975158, 0.131326]]

from matplotlib.colors import ListedColormap

cmaps['plasma'] = ListedColormap(_plasma_data, name='plasma')
plasma = cmaps['plasma']


def SetThreeXTicks(ax):
    X = ax.get_xlim()[1]
    r = np.arange(0, X * 1.1, X / 2.)
    ax.set_xticks(r)


def SetThreeYTicks(ax):
    X = ax.get_ylim()[1]
    r = np.arange(0, X * 1.1, X / 2.)
    ax.set_yticks(r)


def OrderedSpecies(treeFN):
    # print(f'treeFN is \n{treeFN}\n')
    # with open(treeFN) as tree:
    #     lines = tree.read()
    #     print(lines)
    t = ete3.Tree(treeFN, format=1)
    t.ladderize()
    return [n.name for n in t]


def ReadData(statsOverlapFN):
    data = []
    # print(statsOverlapFN)
    with open(statsOverlapFN, 'r') as infile:
        reader = csv.reader(infile, delimiter="\t")
        # print(dir(reader))
        # species = infile.next()[1:].split()
        species = infile.__next__()[1:].split()
        # print(species)
        for line in reader:
            # print(line)
            data.append(list(map(float, line[1:])))
            # print(data)
    return species, data


def GetOrder(species, treeFN, qLadderize=False):
    # print(treeFN)
    # t = ete3.Tree(treeFN)
    t = ete3.Tree(treeFN, format=1)
    # print(t)
    if qLadderize:
        t.ladderize()
    treeOrder = t.get_leaf_names()
    #    print(treeOrder)
    order = [[i for i, name in enumerate(species) if target in name][0] for target in treeOrder]
    return order


def HeatMap(data, I, outputFN, m1=None):
    # print(data)
    s = 40
    drawing = svgwrite.Drawing(outputFN, profile='full')
    n = len(data)
    if m1 == None:
        m1 = max([max(d) for d in data])
    #        print(m1)
    cmap = plasma if qColor else plt.get_cmap('binary')
    # for i in xrange(n):
    for i in range(n):
        # for j in xrange(n):
        for j in range(n):
            y = data[I[i]][I[j]] / m1
            if qReverse: y = 1. - y
            c = tuple([int(np.floor(255. * x)) for x in cmap(y)[:3]])
            drawing.add(drawing.rect(insert=(s * i, s * j),
                                     size=("%dpx" % s, "%dpx" % s),
                                     stroke_width="1",
                                     stroke="black",
                                     fill="rgb(%d,%d,%d)" % c))
    #            drawing.add(drawing.text("%d" % data[I[i]][I[j]], insert = (s*(i+0.1), s*(j+0.5))))    # don't write numbers

    drawing.save()
    # Key
    drawing = svgwrite.Drawing(os.path.splitext(outputFN)[0] + "_key.svg", profile='full')
    # key = [4000, 6000, 8000, 10000, 12000, 16000]  # CJJ key is hardcoded!
    key = [10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000]
    goldenRatio = 1.61803398875
    for j, v in enumerate(reversed(key)):
        c = tuple([int(np.floor(255. * x)) for x in cmap(v / m1)[:3]])
        drawing.add(drawing.rect(insert=(0, s * goldenRatio * j),
                                 size=("%dpx" % s, "%dpx" % (s * goldenRatio)),
                                 stroke_width="1",
                                 stroke="black",
                                 fill="rgb(%d,%d,%d)" % c))
        drawing.add(drawing.text("%d" % v, insert=(s * 1.2, s * (j + 0.5) * goldenRatio)))
    drawing.save()


def CreateHeatmap(statsOverlapFN, outputFN, treeFN, qLadderize=False):
    species, data = ReadData(statsOverlapFN)
    order = GetOrder(species, treeFN, qLadderize)
    print(f'CJJ order is {order}')
    HeatMap(data, order, outputFN)


def ConvertToCladogram(tree, ts):
    for node in tree.traverse():
        ts.show_scale = False  # scale bar will no longer have meaning
        # width of circles for nodes means the alignment isn't exact, correct this
        node.set_style(ete3.NodeStyle(size=0))
        if node.is_root():
            continue
        notUsed, dist = node.get_farthest_leaf(topology_only=True)
        notUsed, dist_above = node.up.get_farthest_leaf(topology_only=True)
        node.dist = dist_above - dist
    return tree


def DrawSpeciesTree(dResults, treeFN):
    t = ete3.Tree(treeFN, format=1)
    t.ladderize()
    for n in t.traverse():
        #        print((n.name, n.dist))
        n.set_style(ete3.NodeStyle(size=0))
    #        if n.is_leaf(): n.add_face(ete2.faces.TextFace(n.name), 1)
    t.render(d_out + "SpeciesTree.pdf")
    ts = ete3.TreeStyle()
    t = ConvertToCladogram(t, ts)
    t.render(d_out + "SpeciesTree_cladogram.pdf")
    # write out species names as proper strings instead of individual characters
    f, ax = plt.subplots()
    ordered_names = [n.name for n in t]
    for i, n in enumerate(ordered_names):
        ax.annotate(n, xy=(0, 1. - 0.1 * i))
    f.savefig(d_out + "SpeciesTreeTaxonNames.pdf")
    return ordered_names


def HeatMaps(dResults, treeFN):
    statsOverlapFN = dResults + "Comparative_Genomics_Statistics/Orthogroups_SpeciesOverlaps.tsv"
    ordered_names = DrawSpeciesTree(dResults, treeFN)

    # Orthogroups
    outputFN = d_out + "heatmap_orthogroups.svg"
    CreateHeatmap(statsOverlapFN, outputFN, treeFN, qLadderize=True)  # , m1=16000)

    # Orthologues
    orthologuesFN = dResults + "Comparative_Genomics_Statistics/OrthologuesStats_Totals.tsv"
    outputFN = d_out + "heatmap_orthologues.svg"
    # CreateHeatmap(orthologuesFN, outputFN, treeFN)
    CreateHeatmap(orthologuesFN, outputFN, treeFN, qLadderize=True)  # CJJ added qLadderize=True


def ReadDataMatrix(statsOverlapFN):
    data = []
    with open(statsOverlapFN, 'r') as infile:
        reader = csv.reader(infile, delimiter="\t")
        species = infile.__next__()[1:].split()
        for line in reader:
            data.append(list(map(float, line[1:])))
    return species, np.matrix(data)


def PlotPercentForSpecies(dResults, ordered_species):
    data_to_plot = ["Percentage of genes in orthogroups", "Number of species-specific orthogroups"]
    for d_name in data_to_plot:
        # print(d_name)
        with open(dResults + "Comparative_Genomics_Statistics/Statistics_PerSpecies.tsv", 'r') as infile:
            reader = csv.reader(infile, delimiter="\t")
            species = reader.__next__()[1:]
            # print(species)
            for line in reader:
                if len(line) > 0:
                    if line[0] == d_name:
                        data = list(map(float, line[1:]))
                        # print(data)
        ordered_data = [data[species.index(s)] for s in ordered_species]
        # print(ordered_data)
        fig, ax = plt.subplots()
        n = len(ordered_species)
        Y = list(range(n, 0, -1))
        ax.barh(Y, ordered_data, align="center")
        ax.set_yticks(Y)
        ax.set_yticklabels(ordered_species)
        SetThreeXTicks(ax)
        ax.set_xlabel(d_name)
        fig.savefig(dResults + d_name.replace(" ", "_") + ".pdf")
        fig.savefig(d_out + d_name.replace(" ", "_") + ".pdf")


def PlotSizeDistribution(dResults):
    # with open(dResults + "Comparative_Genomics_Statistics/Statistics_Overall.tsv", 'rb') as infile:
    with open(dResults + "Comparative_Genomics_Statistics/Statistics_Overall.tsv", 'r') as infile:
        reader = csv.reader(infile, delimiter="\t")
        qStart = False
        Xlabels = []
        Ygroups = []
        Ygenes = []
        for line in reader:
            if qStart:
                if len(line) == 0 or line[0] == "": break
                Xlabels.append(line[0].replace("'", ""))
                Ygroups.append(float(line[2]))
                Ygenes.append(float(line[4]))
            if len(line) > 0 and line[0] == "Average number of genes per-species in orthogroup":
                qStart = True
    # Plot data
    iMax = 0
    for i, d in enumerate(Ygenes):
        if d > 0: iMax = i
    fig, ax = plt.subplots()
    nData = len(Xlabels)
    X = np.arange(nData)
    ax.bar(X[:iMax + 1], Ygroups[:iMax + 1], width=0.45)
    ax.bar(X[:iMax + 1] + 0.45, Ygenes[:iMax + 1], width=0.45, color='g')
    ax.set_xticks(X[:iMax + 1] + 0.45)
    ax.set_xticklabels(Xlabels[:iMax + 1])
    SetThreeYTicks(ax)
    fig.savefig(d_out + "SizeDistribution.pdf")


def PlotTerminalDups(dResults, ordered_species):
    n = len(ordered_species)
    dSpecies = {s: i for i, s in enumerate(ordered_species)}
    data = np.zeros(n)
    with open(dResults + "Gene_Duplication_Events/Duplications.tsv", 'r') as infile:
        reader = csv.reader(infile, delimiter="\t")
        reader.__next__()
        for line in reader:
            if line[4] == "Terminal":
                data[dSpecies[line[1]]] += 1
    fig, ax = plt.subplots()
    Y = range(n, 0, -1)
    ax.barh(Y, data, align='center', color='k', linewidth=0)
    ax.set_yticks(Y)
    ax.set_yticklabels(ordered_species)
    SetThreeXTicks(ax)
    fig.savefig(d_out + "SpeciesSpecificDuplications.pdf")


def StackedBar_onetomany(d11, d1m, dm1, dmm, species, ordered_species, species_to_plot, outDir):
    """
    matrices are ordered accroding to species
    plot should be ordered by ordered_species
    """
    print(species)
    print(ordered_species)
    fig, ax = plt.subplots()

    n = len(species)
    # print(n)
    I = [species.index(s) for s in ordered_species]
    # print(I)
    isp = species.index(species_to_plot)
    print('CJJ isp index position', isp)
    dtot = d11 + d1m + dm1 + dmm
    # [print(d11)]
    # print('CJJ dtot is:', dtot)

    # Y = range(n, 0, -1)
    Y = list(range(n, 0, -1))
    print('CJJ Y is ', Y)
    I = [species.index(s) for s in ordered_species if s != species_to_plot]
    print('CJJ I', I)
    print('CJJ value to pop:', ordered_species.index(species_to_plot))
    Y.pop(ordered_species.index(species_to_plot))
    print('CJJ popped Y is', Y)

    pos = np.ones((1, n - 1))
    print('CJJ unaltered pos is:', pos)
    ax.barh(Y, 100. * pos[0, :], color='k', linewidth=0, align='center')
    pos -= (dmm[isp, I] / dtot[isp, I])
    # print('CJJ pos is:', pos)
    ax.barh(Y, 100. * pos[0, :], color='g', linewidth=0, align='center')
    pos -= (dm1[isp, I] / dtot[isp, I])
    ax.barh(Y, 100. * pos[0, :], color='b', linewidth=0, align='center')
    pos -= (d1m[isp, I] / dtot[isp, I])
    ax.barh(Y, 100. * pos[0, :], color='r', linewidth=0, align='center')
    # SetThreeXTicks(ax)
    # ax.set_yticks(range(7, 0, -1))  #CJJ changes from 10 to 15
    ax.set_yticks(range(15, 0, -1))  # CJJ changes from 10 to 15
    ax.set_yticklabels(ordered_species)
    fig.savefig(outDir + "StackedBar_%s.pdf" % species_to_plot)


def OneToManyPlot(dResults, ordered_species):
    species, d11 = ReadDataMatrix(dResults + "Comparative_Genomics_Statistics/OrthologuesStats_one-to-one.tsv")
    species, d1m = ReadDataMatrix(dResults + "Comparative_Genomics_Statistics/OrthologuesStats_one-to-many.tsv")
    species, dm1 = ReadDataMatrix(dResults + "Comparative_Genomics_Statistics/OrthologuesStats_many-to-one.tsv")
    species, dmm = ReadDataMatrix(dResults + "Comparative_Genomics_Statistics/OrthologuesStats_many-to-many.tsv")
    # print(ordered_species)
    # print(species)
    # print(d11)
    # print(d1m)
    # print(dm1)
    # print(dmm)

    # StackedBar_onetomany(d11, d1m, dm1, dmm, species, ordered_species, "Homo_sapiens", d_out)
    # StackedBar_onetomany(d11, d1m, dm1, dmm, species, ordered_species, "Ciona_intestinalis", d_out)
    StackedBar_onetomany(d11, d1m, dm1, dmm, species, ordered_species, "Aca_pyc", d_out)
    # StackedBar_onetomany(d11, d1m, dm1, dmm, species, ordered_species, "P_alb", d_out)




def NumberOfDuplications(treeFN, dResults, cutoff=1.0):
    dups = defaultdict(int)
    with open(dResults + "Gene_Duplication_Events/Duplications.tsv", 'r') as infile:
        reader = csv.reader(infile, delimiter="\t")
        reader.__next__()
        for line in reader:
            if float(line[3]) >= 0.999:
                dups[line[1]] += 1
    t = ete3.Tree(treeFN, format=1)
    t.ladderize()
    for k, v in dups.items():
        if k == "N0": continue
        try:
            n = t & k
            if n.is_leaf(): continue
            n.add_face(ete3.TextFace(str(v), fgcolor='green'), 1, 'branch-top')
        except:
            pass
    ts = ete3.TreeStyle()
    t = ConvertToCladogram(t, ts)
    t.render(d_out + "DuplicationsTree.pdf")


def GenesWithOrthologues(dResults, ordered_species):
    d_orthos = dict()
    for sp1 in ordered_species:
        for sp2 in ordered_species:
            if sp2 == sp1: continue
            with open(dResults + "Orthologues/Orthologues_%s/%s__v__%s.tsv" % (sp1, sp1, sp2), 'r') as infile:
                s1_with_ortho = []
                s2_with_ortho = []
                reader = csv.reader(infile, delimiter="\t")
                reader.__next__()
                for line in reader:
                    _, g1, g2 = line
                    s1_with_ortho.extend(g1.split(", "))
                    s2_with_ortho.extend(g2.split(", "))
                d_orthos[(sp1, sp2)] = set(s1_with_ortho)
                d_orthos[(sp2, sp1)] = set(s2_with_ortho)
    # find all genes per species with orthologues
    nOrtho = []
    nOrthoInAll = []
    for sp1 in ordered_species:
        genes = set.union(*[d_orthos[(sp1, sp2)] for sp2 in ordered_species if sp2 != sp1])
        nOrtho.append(len(genes))
        # now, how many with orthologues in all species
        nOrthoInAll.append(
            len([True for g in genes if all([g in d_orthos[(sp1, sp2)] for sp2 in ordered_species if sp2 != sp1])]))
    #    print(nOrtho)
    #    print(nOrthoInAll)
    Y = range(len(nOrtho), 0, -1)
    fig, ax = plt.subplots()
    ax.barh(Y, nOrtho, color='b', linewidth=0)
    ax.barh(Y, nOrthoInAll, color='g', linewidth=0)
    SetThreeXTicks(ax)
    fig.savefig(d_out + "GenesWithOrthologues.pdf")
    return fig, ax


if __name__ == "__main__":
    """ Input data """
    # dResults = "orthofinder_out_simpleNames_fabales_only/Results_Aug26/"
    dResults = "orthofinder_out_simpleNames_angiosperms_only/Results_Aug30/"
    # dResults = "orthofinder_out_simpleNames/Results_May26/"
    # dResults = "orthofinder_out_simpleNames_fabales_only/Results_Oct20/"
    # dResults = "orthofinder_out_simpleNames_angiosperms_only/Results_Oct05/"
    date = dResults.split("/")[-2].split("_")[-1]
    treeFN = dResults + "Species_Tree/SpeciesTree_rooted_node_labels.txt"
    ordered_species = OrderedSpecies(treeFN)
    print(f'ordered_species is: {ordered_species}')
    d_out = "Figures/"
    if not os.path.exists(d_out):
        os.mkdir(d_out)


    """ Plots """
    HeatMaps(dResults, treeFN)
    OneToManyPlot(dResults, ordered_species)
    PlotPercentForSpecies(dResults, ordered_species)
    PlotSizeDistribution(dResults)
    PlotTerminalDups(dResults, ordered_species)
    NumberOfDuplications(treeFN, dResults)
    fig, ax = GenesWithOrthologues(dResults, ordered_species)
