import json
import os

# 바운딩 박스의 좌표를 YOLO 형식으로 변환하는 함수
def convert(size, box):
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]
    x = (box[0] + box[2]) / 2.0
    y = (box[1] + box[3]) / 2.0
    w = box[2] / 2.0
    h = box[3] / 2.0
    x = round(x * dw, 6)
    w = round(w * dw, 6)
    y = round(y * dh, 6)
    h = round(h * dh, 6)
    return (x, y, w, h)

# 대상 폴더 리스트
folders = ['B0', 'B1', 'H0', 'H1', 'M0', 'M1']

# 오류가 발생한 JSON 파일명을 담을 리스트
error_files = []

# 'S63_1_DATA3-001' 폴더 내의 각 폴더에 대해
for index, folder in enumerate(folders):
    folder_path = os.path.join('S63_1_DATA3-001', folder)

    # 각 폴더에 있는 모든 JSON 파일에 대해
    for json_file_name in os.listdir(folder_path):
        if not json_file_name.endswith('.json'):
            continue  # JSON 파일이 아니면 건너뜀

        with open(os.path.join(folder_path, json_file_name), encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                error_files.append(json_file_name)
                continue

        size = [data['images']['width'], data['images']['height']]

        # .txt 파일을 같은 폴더에 저장
        txt_file_name = json_file_name.replace('.json', '.txt')
        txt_file_path = os.path.join(folder_path, txt_file_name)

        if(not data['annotations']):
            print('annotations 없음')
            continue

        try:
            with open(txt_file_path, 'w') as tf:
                for ann in data['annotations']:
                    bbox = ann['bbox']
                    if (not bbox):
                        continue
                    class_id = index
                    bb = convert(size, bbox)

                    line = f"{class_id} {bb[0]} {bb[1]} {bb[2]} {bb[3]}\n"
                    tf.write(line)
        except IndexError:
            error_files.append(json_file_name)
            continue

# 오류가 발생한 JSON 파일명 출력
print("오류가 발생한 파일들:")
for file_name in error_files:
    print(file_name)

# 오류가 발생한 파일명과 개수를 텍스트 파일로 저장
output_file_path = "error_files.txt"
with open(output_file_path, 'w') as output_file:
    output_file.write(f"오류가 발생한 파일 개수: {len(error_files)}\n")
    output_file.write("오류가 발생한 파일들:\n")
    for file_name in error_files:
        output_file.write(file_name + "\n")

## 지금 변환이 안되는파일이 많음 --> index array 문제인데 가끔 바운딩 박스 영역이 없는 json 파일 있음