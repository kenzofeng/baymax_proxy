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


def set_robot_paramenter_to_argfile(testpath, parameter):
    try:
        argfiel_path = os.path.join(testpath, 'argfile.txt')
        useages = ['-v', '--variable']
        parameter = parameter.strip()
        ps = list(filter(None,parameter.split(" ")))
        f = open(argfiel_path, 'a')
        for i in range(0, len(ps), 2):
            if ps[i] in useages:
                f.write('\n')
                f.write(ps[i])
                f.write('\n')
                f.write(ps[i + 1])
        f.close()
    except Exception as e:
        raise Exception("set_robot_paramenter_to_argfile error:{}".format(e))


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
