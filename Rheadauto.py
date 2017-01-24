# coding: utf-8
'''
10:27 2015/05/20
Hiroaki Kikuchi
Fibrous Biomaterials Lab, Division of Forest and Biomaterials Science, Kyoto Univ.
'''

print '\n*******************************'
print '           Rheadauto'
print '*******************************'
print 'Program for editing headers(Gonio vecters and 3 angles) of Rigaku RAPID img files automatically.\n'
print "> Can be used for both of narrow and wide image."
print "> Please type Start/End angles in INTEGER of FLOAT."
print '!!!This program could cause fatal troubles to your files. NEVER FAIL TO BACKUP FOR YOURSELF.!!!\n'


import glob, struct

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
	gonio_vec_inp = raw_input('Rotating or 3D? (y/n)\n')
	if gonio_vec_inp == 'y':
		gonio_vec = 1.000000
	elif gonio_vec_inp == 'n':
		gonio_vec = -1.000000

	c_angle_min = float(raw_input('Start chi angle?\n'))
	c_angle_max = float(raw_input('End chi angle?\n'))
	c_step = (c_angle_max - c_angle_min) / len(file_name)

	o_angle_min = float(raw_input('Start omega angle?\n'))
	o_angle_max = float(raw_input('End omega angle?\n'))
	o_step = (o_angle_max - o_angle_min) / len(file_name)

	p_angle_min = float(raw_input('Start phi angle?\n'))
	p_angle_max = float(raw_input('End phi angle?\n'))
	p_step = (p_angle_max - p_angle_min) / len(file_name)

	# edit
	for i in range(len(file_name)):
		with open(file_name[i], 'r+b') as f:
			# f.read(960) #60 lines
			# gonio vectors
			f.seek((8 * gonio_vec_bin[0] + gonio_vec_bin[1]) * 2)
			f.write(struct.pack('>f', gonio_vec))
			# chi
			f.seek((8 * c_start_bin[0] + c_start_bin[1]) * 2)
			f.write(struct.pack('>f', c_angle_min + c_step * i))
			f.seek((8 * c_end_bin[0] + c_end_bin[1]) * 2)
			f.write(struct.pack('>f', c_angle_min + c_step * (i+1)))
			# omega
			f.seek((8 * o_start_bin[0] + o_start_bin[1]) * 2)
			f.write(struct.pack('>f', o_angle_min + o_step * i))
			f.seek((8 * o_end_bin[0] + o_end_bin[1]) * 2)
			f.write(struct.pack('>f', o_angle_min + o_step * (i+1)))
			# phi
			f.seek((8 * p_start_bin[0] + p_start_bin[1]) * 2)
			f.write(struct.pack('>f', p_angle_min + p_step * i))
			f.seek((8 * p_end_bin[0] + p_end_bin[1]) * 2)
			f.write(struct.pack('>f', p_angle_min + p_step * (i+1)))

elif y_or_n == 'n':
	print 'Please rename files for a proper order.'

else:
	print 'Please type y or n.'
