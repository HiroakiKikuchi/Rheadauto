# coding: utf-8
'''
16:38 2015/05/17
Hiroaki Kikuchi
Fibrous Biomaterials Lab, Division of Forest and Biomaterials Science, Kyoto Univ.
'''

print '\n*******************************'
print '           Rheadauto'
print '*******************************'
print 'Program for editing headers of Rigaku RAPID img files automatically.\n'
print "> Can be used for both of narrow and wide image."
print "> 7th Gonio vector is always '1.000000'."
print '> Type omega and phi start/end angles. Step angles are calculated at even intevals. Please use ONLY 0-256 INTEGERS.\n'
print '!!!This program could cause fatal troubles to your files. NEVER FAIL TO BACKUP FOR YOURSELF.!!!\n'


import glob, binascii

# make correspondence dictionary between decimal and hexadecimal. both are strings.
deci = []
for i in range(257):# data format is more complicated from 257.
	deci.append(str(i))

hexa = ['3f80']# '3f80' means '0' in integer
for i in range(1):
	hexa.append(hex(int(hexa[i], 16) + 128).replace('0x', ''))
for i in range(1, 3):
	hexa.append(hex(int(hexa[i], 16) + 64).replace('0x', ''))
for i in range(3, 7):
	hexa.append(hex(int(hexa[i], 16) + 32).replace('0x', ''))
for i in range(7, 15):
	hexa.append(hex(int(hexa[i], 16) + 16).replace('0x', ''))
for i in range(15, 31):
	hexa.append(hex(int(hexa[i], 16) + 8).replace('0x', ''))
for i in range(31, 63):
	hexa.append(hex(int(hexa[i], 16) + 4).replace('0x', ''))
for i in range(63, 127):
	hexa.append(hex(int(hexa[i], 16) + 2).replace('0x', ''))
for i in range(127, 255):
	hexa.append(hex(int(hexa[i], 16) + 1).replace('0x', ''))
hexa.insert(0,'0000')

table = dict(zip(deci, hexa))


# position in binary. [m, n]: m = lines, n = rows (COUNT FROM 0)
gonio_vec_bin = [55, 2]
o_start_bin = [57, 4]
o_end_bin = [58, 6]
c_start_bin = [57, 6]
c_end_bin = [59, 0]
p_start_bin = [58, 0]
p_end_bin = [59, 2]


# get file names in ascending order
print("\nImg files in this directory:")
file_name = []
file_name.extend(glob.glob('*.img'))
for name in file_name:
	print('- ' + name)
print ''

# check order of files
y_or_n = raw_input("Is the order of files correct?(y/n)\n")
if y_or_n == 'y':
	# get input
	gonio_vec = '1'

	c_angle_min = raw_input('Start chi angle?\n')
	c_angle_max = raw_input('End chi angle?\n')
	c_step = (int(c_angle_max) - int(c_angle_min)) / len(file_name)

	o_angle_min = raw_input('Start omega angle?\n')
	o_angle_max = raw_input('End omega angle?\n')
	o_step = (int(o_angle_max) - int(o_angle_min)) / len(file_name)

	p_angle_min = raw_input('Start phi angle?\n')
	p_angle_max = raw_input('End phi angle?\n')
	p_step = (int(p_angle_max) - int(p_angle_min)) / len(file_name)

	# edit
	for i in range(len(file_name)):
		with open(file_name[i], 'r+b') as f:
			f.read(960) #60 lines
			# gonio vectors
			f.seek((8 * gonio_vec_bin[0] + gonio_vec_bin[1]) * 2)
			f.write(binascii.a2b_hex(table[gonio_vec]))
			# chi
			f.seek((8 * c_start_bin[0] + c_start_bin[1]) * 2)
			f.write(binascii.a2b_hex(table[str(int(c_angle_min) + c_step * i)] + '0000'))
			f.seek((8 * c_end_bin[0] + c_end_bin[1]) * 2)
			f.write(binascii.a2b_hex(table[str(int(c_angle_min) + c_step * (i+1))] + '0000'))
			# omega
			f.seek((8 * o_start_bin[0] + o_start_bin[1]) * 2)
			f.write(binascii.a2b_hex(table[str(int(o_angle_min) + o_step * i)] + '0000'))
			f.seek((8 * o_end_bin[0] + o_end_bin[1]) * 2)
			f.write(binascii.a2b_hex(table[str(int(o_angle_min) + o_step * (i+1))] + '0000'))
			# phi
			f.seek((8 * p_start_bin[0] + p_start_bin[1]) * 2)
			f.write(binascii.a2b_hex(table[str(int(p_angle_min) + p_step * i)] + '0000'))
			f.seek((8 * p_end_bin[0] + p_end_bin[1]) * 2)
			f.write(binascii.a2b_hex(table[str(int(p_angle_min) + p_step * (i+1))] + '0000'))

elif y_or_n == 'n':
	print 'Please rename files for a proper order.'

else:
	print 'Please type y or n.'
