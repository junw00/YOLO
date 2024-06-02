import shutil
import glob
import os
from random import shuffle

# 대상 폴더 리스트
folders = ['B0', 'B1', 'H0', 'H1', 'M0', 'M1']

# 각 파일마다 복사할 파일 개수
TRAIN_FILE_COUNT = 4000
VAL_FILE_COUNT = 500
TEST_FILE_COUNT = 500
# 
# 각 파일간 최대 복사 가능 파일 수
MAX_FILE_COUNT = 5000

train_path = os.path.dirname(__file__) + '\\train'
val_path = os.path.dirname(__file__) + '\\val'
test_path = os.path.dirname(__file__) + '\\test'
images_path = '\images\\'
labels_path = '\labels\\'

# 학습 데이터 저장 공간
images_train_destination = train_path + images_path
labels_train_destination = train_path + labels_path
images_val_destination = val_path + images_path
labels_val_destination = val_path + labels_path
images_test_destination = test_path + images_path

# annotation이 존재하지 않아 txt가 만들어지지 않는 파일
no_has_annotation_file = "S63_1_DATA3-001\H0\S63_DATA3_H0_L3_D2023-08-16-13-20_001_003265.jpg"


# 폴더가 있는지 확인 후 없으면 폴더 생성
if (not os.path.exists(train_path)):
    os.mkdir(train_path)
    # images와 labels까지 같이 생성
    os.mkdir(train_path + images_path)
    os.mkdir(train_path + labels_path)
else:
    # images가 없을경우 생성
    if (not os.path.exists(train_path + images_path)):
        os.mkdir(train_path + images_path)
    else:
        shutil.rmtree(train_path + images_path, ignore_errors=True)
        os.mkdir(train_path + images_path)
        
    if (not os.path.exists(train_path + labels_path)):
        os.mkdir(train_path + labels_path) 
    else:
        shutil.rmtree(train_path + labels_path, ignore_errors=True)   
        os.mkdir(train_path + labels_path) 

if (not os.path.exists(val_path)):
    os.mkdir(val_path)
    # images와 labels까지 같이 생성
    os.mkdir(val_path + images_path)
    os.mkdir(val_path + labels_path)
else:
    # images가 없을경우 생성
    if (not os.path.exists(val_path + images_path)):
        os.mkdir(val_path + images_path)
    else:
        shutil.rmtree(val_path + images_path, ignore_errors=True)
        os.mkdir(val_path + images_path)

    if (not os.path.exists(val_path + labels_path)):
        os.mkdir(val_path + labels_path) 
    else:
        shutil.rmtree(val_path + labels_path, ignore_errors=True)  
        os.mkdir(val_path + labels_path) 

if (not os.path.exists(test_path)):
    os.mkdir(test_path)
    # images까지 같이 생성
    os.mkdir(test_path + images_path)
else:
    # images가 없을경우 생성
    if (not os.path.exists(test_path + images_path)):
        os.mkdir(test_path + images_path) 
    else:
        shutil.rmtree(test_path + images_path, ignore_errors=True)
        os.mkdir(test_path + images_path) 

file_count = 0

# 각 파일간 복사 시작
for folder in folders:
    # 복사 전 개수 입력 확인
    if (TRAIN_FILE_COUNT + VAL_FILE_COUNT + TEST_FILE_COUNT > MAX_FILE_COUNT + 1):
        print('복사 가능한 파일 개수를 정확히 입력 해주시기 바랍니다.')
        break

    # 복사할 파일 경로
    source = os.path.dirname(__file__) + '\\'

    # 복사할 이미지 파일들
    images = sorted(glob.glob(os.path.join('S63_1_DATA3-001', folder) + '\*.jpg'))
    # 복사할 라벨 파일들
    labels = sorted(glob.glob(os.path.join('S63_1_DATA3-001', folder) + '\*.txt'))

    # annotation이 없는 파일 삭제
    if (len(images) != len(labels)):
        images.remove(no_has_annotation_file)
        print('파일 삭제')

    if (len(images) != len(labels)):
        print(folder, ' 파일에 있는 이미지 수와 라벨 수가 맞지 않습니다.')
        continue
    

    # 이미지와 라벨 파일 섞기
    files = list(zip(images, labels))
    shuffle(files)
    images, labels = zip(*files)

    # 이미지 및 라벨 복사
    for i in range(0, MAX_FILE_COUNT):
            # print(file_count)
            # if (file_count == MAX_FILE_COUNT * len(folders) - 1):
            #     break

            if (len(images) != MAX_FILE_COUNT and i == MAX_FILE_COUNT - 1):
                break

            image_source = source + images[i]
            label_source = source + labels[i]

            image_name = images[i].split('\\')[2]
            label_name = labels[i].split('\\')[2]

            image_destination = ''
            label_destination = ''

            if (i < TRAIN_FILE_COUNT):
                image_destination = images_train_destination + image_name
                label_destination = labels_train_destination + label_name
            elif (i < TRAIN_FILE_COUNT + VAL_FILE_COUNT):
                image_destination = images_val_destination + image_name
                label_destination = labels_val_destination + label_name
            elif (i < TRAIN_FILE_COUNT + VAL_FILE_COUNT + TEST_FILE_COUNT):
                image_destination = images_test_destination + image_name
            else:
                # 옮기는 파일 개수를 넘었으므로 복사 종료
                break

            if(image_destination == '' or (i < TRAIN_FILE_COUNT + VAL_FILE_COUNT and label_destination == '')):
                print(i, '도착지가 정해지지 않았습니다.')
                continue

            # 파일 복사
            shutil.copyfile(image_source, image_destination)

            if (i < TRAIN_FILE_COUNT + VAL_FILE_COUNT):
            #     test는 이미지만 복사
                shutil.copyfile(label_source, label_destination)
            
            file_count += 1