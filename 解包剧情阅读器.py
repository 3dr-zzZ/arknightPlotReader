import os
import re

def process_file(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as f:
        juqing = f.readlines()

    re_mingzi = re.compile(r'name="(.*)"]')
    re_duihua = re.compile(r']\s*(.*)')
    re_huifu = re.compile(r'"(.*)",')
    re_xuanxiang = re.compile(r'"(.*)"')

    jiexijuqing = []

    for i in juqing:
        if i[:5] == "[Name" or i[:5] == "[name":
            mingzi = re_mingzi.findall(i)
            duihua = re_duihua.findall(i)
            if mingzi and duihua:
                jiexijuqing.append(mingzi[0] + ": " + duihua[0])

        elif i[:5] == "[Dial" or i[:5] == "[dial":
            jiexijuqing.append("")

        elif i[:5] == "[Deci" or i[:5] == "[deci":
            huifulist = re_huifu.findall(i)[0].split(";")
            jiexijuqing.append("\n下面是可选择的回复：")
            for j, huifu in enumerate(huifulist, 1):
                jiexijuqing.append(f"    选项{j}：" + huifu)

        elif i[:5] == "[Pred" or i[:5] == "[pred":
            xuanxianglist = re_xuanxiang.findall(i)
            jiexijuqing.append(f"\n下面是回复选项{xuanxianglist}的剧情：")

        elif not i.startswith("["):
            jiexijuqing.append(i.strip())

    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    with open(output_file_path, 'w', encoding='utf-8') as f:
        for line in jiexijuqing:
            f.write(line + '\n')

def main():
    input_root = input("请输入包含文本文件的文件夹路径: ").strip('"')
    output_root = input("请输入输出处理后文件的文件夹路径: ").strip('"')

    for dirpath, _, filenames in os.walk(input_root):
        for filename in filenames:
            if filename.endswith(".txt"):
                full_input_path = os.path.join(dirpath, filename)

                # Preserve relative path
                rel_path = os.path.relpath(full_input_path, input_root)
                name, _ = os.path.splitext(rel_path)
                rel_output_path = name + "_jiexi.txt"

                full_output_path = os.path.join(output_root, rel_output_path)
                print(f"正在处理: {full_input_path} -> {full_output_path}")
                process_file(full_input_path, full_output_path)

if __name__ == "__main__":
    main()
