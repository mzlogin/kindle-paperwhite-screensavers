import hashlib
import os
import json

def get_file_md5(file_path):
    with open(file_path, 'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        _hash = md5obj.hexdigest()
        return str(_hash).lower()

if __name__ == '__main__':
    screensavers_path = 'screensavers'
    file_md5_dict = {}
    for dir_path, dir_names, filenames in os.walk(screensavers_path):
        for filename in filenames:
            if os.path.splitext(filename)[1] == '.png':
                file_path = os.path.join(screensavers_path, filename)
                file_md5_dict[filename] = get_file_md5(file_path)

    with open('meta.json', 'w') as outfile:
        json.dump(file_md5_dict, outfile)
