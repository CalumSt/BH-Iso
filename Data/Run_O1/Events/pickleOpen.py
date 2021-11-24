import joblib

file = open("Pofd_GW150914.p",'rb')
object_file = joblib.load(file)
file.close()

print(object_file)