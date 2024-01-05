import os
import tarfile
import re
import shutil 

def write_star(files, tar: tarfile.TarFile, heading: str, output_path: str):
    junction_filename = next(filter(lambda x: re.search('SJ.out.tab', x), files))
    file = tar.extractfile(junction_filename)
    lines = file.readlines()
    print('...Writing STAR junction file to: %s' % ('.'.join([heading, 'SJ.out.tab'])))
    with open('%s%s.SJ.out.tab' % (output_path, heading), 'wb') as output:
            output.writelines(lines)

def write_star_v2(files, tar: tarfile.TarFile, heading: str, output_path: str):
    junction_filename = next(filter(lambda x: re.search('SJ.out.tab', x), files))
    print(f'...(v2)Copying STAR junction file to: {os.path.join(output_path, f"{heading}.SJ.out.tab")}')
    with tar.extractfile(junction_filename) as src, open(os.path.join(output_path, f"{heading}.SJ.out.tab"), 'wb') as dst:
        shutil.copyfileobj(src, dst)
    

def write_star_v3(files, tar: tarfile.TarFile, heading: str, output_path: str):
    junction_filename = next(filter(lambda x: re.search('SJ.out.tab', x), files))
    print(f'...(v3)Copying STAR junction file to: {os.path.join(output_path, f"{heading}.SJ.out.tab")}')
    with open(os.path.join(output_path, f"{heading}.SJ.out.tab"), 'wb') as dst:
        tar.extract(junction_filename, dst)