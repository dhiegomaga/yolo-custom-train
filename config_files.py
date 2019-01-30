import glob, os

# DEFINE FOLDER WITH ALL IMAGES
files_folder = 'files'

# DEFINE CLASS NAMES
# ex: classes = ["house", "car", "goat"]
classes = ["door", "bench", "trash", "fire", "water"]

# Config folder & files
config_folder = 'cfg2'
obj_data = 'obj.data'
obj_names = 'obj.names'
img_ext = 'jpg'

# .txt files & .jpg files
txt_paths = glob.glob(os.path.join(files_folder, "*.txt"))
img_files = glob.iglob(os.path.join(files_folder, "*."+img_ext))
titles = set()

print "Generating train and test files\n"

for txt in txt_paths:
    titles.add(os.path.splitext(os.path.basename(txt))[0])

# Percentage of images to be used for the test set
percentage_test = 15

# Create train.txt and test.txt
file_train = open('train.txt', 'w')  
file_test = open('test.txt', 'w')

# Populate train.txt and test.txt
counter = 1
index_test = round(100 / percentage_test)

for pathAndFilename in img_files:  
    title, ext = os.path.splitext(os.path.basename(pathAndFilename))

    # Test if .txt file exists for given image file
    if title not in titles:
        continue

    if counter == index_test:
            counter = 1
            file_test.write(files_folder + "/" + title + '.'+ img_ext + "\n")
    else:
        file_train.write(files_folder + "/" + title + '.'+ img_ext + "\n")
        counter = counter + 1

print "Generating config files\n"

data_path = os.path.join(config_folder, obj_data)
names_path = os.path.join(config_folder, obj_names)

# obj.data
data_file = open(data_path, 'w')
data_file.write('classes= '+ str(len(classes))+'\n')
data_file.write('train  = train.txt\n')
data_file.write('valid  = test.txt\n')
data_file.write('names  = '+names_path+'\n')
data_file.write('backup  = backup/\n') 

# obj.names
names_file = open(names_path, 'w')
for c in classes:
    names_file.write(c+'\n')

print data_path + " generated"
print names_path + " generated"