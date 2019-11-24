import zipfile
import os
import configparser

def unzip_with_pwd(filename, path, pwd=b''):
    with zipfile.ZipFile(filename, 'r') as zip_file:
        try:
            print(os.path.exists(filename))
            zip_file.extractall(path=path, pwd=pwd)
            print('extraction is successful!')
        except RuntimeError:
            print('{} is wrong password!'.format(pwd))

if __name__ == "__main__":
    ini = configparser.ConfigParser()
    ini.read('../.htpasswd', 'UTF-8')
    pwd = ini.get('password', 'test').encode('UTF-8')
    zipdir = ini.get('path', 'zipdir')
    filename = ini.get('path', 'filename')
#    print(ini.get('path', 'filename'))
#    exit()

    unzip_with_pwd(filename=filename, path=zipdir, pwd=pwd)