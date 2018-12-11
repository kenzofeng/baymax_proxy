import os


def create_argfile(testpath, runtests):
    try:
        argfiel_path = os.path.join(testpath, 'argfile.txt')
        f = open(argfiel_path, 'w')
        for rt in runtests:
            f.write('\n')
            f.write('--test')
            f.write('\n')
            f.write(rt)
        f.close()
    except Exception as e:
        raise Exception("create_argfile error:{}".format(e))


def create_argfile_parameter(testpath, robot_parameter):
    try:
        argfiel_path = os.path.join(testpath, 'argfile.txt')
        f = open(argfiel_path, 'w')
        robot_parameters = robot_parameter.split(' ')
        for rt in robot_parameters:
            f.write('\n')
            f.write(rt)
            f.write('\n')
        f.close()
    except Exception as e:
        raise Exception("create_argfile_parameter error:{}".format(e))
