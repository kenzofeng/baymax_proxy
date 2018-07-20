from proxy.models import Test_Map, Project, Node
import json


def update(request):
    maps = Test_Map.objects.filter(project=request.POST['pk'])
    for m in maps:
        m.delete()
    maptest = "map-test-"
    mapurl = "map-url-"
    maprobot = "map-robot-"
    mapuse = 'map-use-'
    for key in request.POST:
        kid = (key.split('-'))[-1]
        if key.find(maptest) != -1:
            m = Test_Map()
            m.project = request.POST['pk']
            m.test = request.POST['%s%s' % (maptest, kid)]
            m.testurl = request.POST['%s%s' % (mapurl, kid)]
            m.robot_parameter = request.POST['%s%s' % (maprobot, kid)]
            if '%s%s' % (mapuse, kid) in request.POST:
                m.use = True
            else:
                m.use = False
            m.save()
    # servers= request.POST['servers'].split(',')
    p = Project.objects.get(pk=request.POST['pk'])
    p.name = request.POST['name']
    p.email = request.POST['email']
    p.node_set.clear()
    p.save()
    for nodename in request.POST['servers'].split(','):
        n = Node.objects.get(name=nodename)
        n.projects.add(p)
        n.save()


def delete(request):
    p = Project.objects.get(pk=request.POST['pk'])
    maps = Test_Map.objects.filter(project=request.POST['pk'])
    for m in maps:
        m.delete()
    p = Project.objects.get(pk=request.POST['pk'])
    p.delete()


def get_all():
    results = []
    list_project = Project.objects.all()
    for project in list_project:
        tests = []
        maps = Test_Map.objects.filter(project=project.name, use=True)
        mylab = {'name': project.name, 'tests': tests}
        for map in maps:
            tests.append({'name': map.test, 'url': map.testurl, 'parameter': map.robot_parameter})
        results.append(mylab)
    return json.dumps(results)
