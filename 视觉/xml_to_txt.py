import xml.etree.ElementTree as ET
import os
from os import listdir, getcwd
from os.path import join, exists
import glob

classes = ["友军","人质","敌人1","敌人2"] # xml文件中标记的种类

def convert(size, box):
    """将VOC格式的边界框转换为YOLO格式"""
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)

def convert_annotation(image_name):
    """转换单个图像的标注文件"""
    try:
        xml_path = os.path.join('./data/Annotations', image_name[:-3] + 'xml')#xml文件目录
        with open(xml_path, encoding='utf-8') as in_file:
            tree = ET.parse(in_file)
            root = tree.getroot()

            # 获取图像尺寸
            size = root.find('size')
            if size is None:
                print(f"Warning: No 'size' element found in {xml_path}")
                return

            w = int(size.find('width').text)
            h = int(size.find('height').text)

            # 创建输出文件
            txt_path = os.path.join('./data/label', image_name[:-3] + 'txt')#txt文件目录
            with open(txt_path, 'w', encoding='utf-8') as out_file:
                for obj in root.iter('object'):
                    # 检查difficult标志和类别
                    difficult = obj.find('difficult')
                    difficult = difficult.text if difficult is not None else '0'

                    cls = obj.find('name').text
                    if cls not in classes or int(difficult) == 1:
                        continue

                    # 获取边界框坐标并转换
                    cls_id = classes.index(cls)
                    xmlbox = obj.find('bndbox')
                    if xmlbox is None:
                        print(f"Warning: No 'bndbox' found for object in {xml_path}")
                        continue

                    b = (float(xmlbox.find('xmin').text),
                         float(xmlbox.find('xmax').text),
                         float(xmlbox.find('ymin').text),
                         float(xmlbox.find('ymax').text))

                    bb = convert((w, h), b)
                    out_file.write(f"{cls_id} {' '.join([str(a) for a in bb])}\n")

        print(f"Converted: {image_name}")
    except FileNotFoundError:
        print(f"Warning: XML file for {image_name} not found, skipping.")
    except Exception as e:
        print(f"Error processing {image_name}: {str(e)}")

def main():
    """主函数：批量处理所有图像文件"""
    # 确保输出目录存在
    if not exists('./data/label'):#txt文件目录
        os.makedirs('./data/label')#txt文件目录

    # 获取所有图像文件
    image_extensions = ['jpg', 'jpeg', 'png', 'bmp']
    image_files = []
    for ext in image_extensions:
        image_files.extend(glob.glob(f'./data/images/*.{ext}'))#图片文件目录

    if not image_files:
        print("Error: No image files found in ./images directory")
        return

    # 转换所有图像的标注
    total = len(image_files)
    print(f"Found {total} images to process")

    for i, img_path in enumerate(image_files):
        img_name = os.path.basename(img_path)
        convert_annotation(img_name)
        if (i + 1) % 10 == 0:
            print(f"Progress: {i + 1}/{total}")

    print(f"Successfully converted {total} annotations")


if __name__ == "__main__":
    main()