import pickle

file = open("Pofd_GW150914",'rb')
object_file = pickle.load(file)
file.close()

print(object_file)