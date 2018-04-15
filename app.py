#!/usr/bin/env python

from flask import Flask, render_template, request
import math, random, os
import xml.etree.ElementTree as ET
import networkx as nx
import svgwrite
import svgutils.transform as st


CIRCLE_TAG_NAME = "{http://www.w3.org/2000/svg}circle"
app = Flask(__name__)


def circle_to_point(circle):
    return (float(circle.attrib['cx']),
            float(circle.attrib['cy']),
            str(circle.attrib['id']),
            int(circle.attrib['level']))


def read_svg_file(svg_file_name):
    return ET.parse(svg_file_name)


def get_all_points(tree):
    return [circle_to_point(circle)
            for circle in tree.iter(CIRCLE_TAG_NAME)]


def get_point_by_id(tree, point_id):
    return [circle_to_point(circle)
            for circle in tree.iter(CIRCLE_TAG_NAME)
            if 'id' in circle.attrib
            if circle.attrib['id'] == point_id]


def get_rest_points_by_id(tree, excluded_point):
    return [circle_to_point(circle)
            for circle in tree.iter(CIRCLE_TAG_NAME)
            if 'id' in circle.attrib
            if circle.attrib['id'] != excluded_point]


def get_all_point_ids(tree):
    circle_id_list = []
    for circle in tree.iter(CIRCLE_TAG_NAME):
        circle_id_list.append(circle.attrib['id'])
    return circle_id_list


def get_adjacency_from_graph(tree, graph):
    for point in get_all_points(tree):
        closest_point_id = str(closest_point(get_rest_points_by_id(tree, point[2]), point)[2])
        if closest_point_id is not None and point is not None:
            graph.add_edge(closest_point_id, point[2])





def distance(point1, point2):
    x1, y1 = point1[0], point1[1]
    x2, y2 = point2[0], point2[1]
    dx = x2 - x1
    dy = y2 - y1
    return math.sqrt(dx * dx + dy * dy)


def closest_point(all_points, new_point):
    best_point = None
    best_distanse = None

    for current_point in all_points:
        current_distanse = distance(new_point, current_point)

        if best_distanse is None or current_distanse < best_distanse:
            best_distanse = current_distanse
            best_point = current_point

    return best_point





def get_id_by_xy(point, tree):
    x1, y1 = point[0], point[1]
    for circle in tree.iter(CIRCLE_TAG_NAME):
        if ('cx' and 'cy') in circle.attrib and  circle.attrib['cx'] == str(x1) and circle.attrib['cy'] == str(y1):
            return circle.attrib['id']



@app.route('/home', methods=['POST'])
def home():
    return render_template('home.html')


@app.route('/', methods=['GET','POST'])
def index():

    starting_level_is_2 = False
    starting_level_is_3 = False

    if request.method == 'POST':
        message = False
        starting_point = str(request.form['first'])
        starting_level = starting_point[0]
        ending_point = request.form['last']
        starting_point_id = doors_id[starting_point]
        ending_point_id = doors_id[ending_point]
        button_pressed = True

        if starting_level == '0':
            starting_level_is_0 = True
        elif starting_level == '1':
            starting_level_is_1 = True
        elif starting_level == '2':
            starting_level_is_2 = True
        elif starting_level == '3':
            starting_level_is_3 = True

        try:
            path = nx.shortest_path(GRAPH, source=starting_point_id, target=ending_point_id)
        except:
            message = True
            return  render_template('submit.html', button_pressed=button_pressed, message=message)


        path_0 = svgwrite.Drawing('path_0.svg', profile='full')
        path_1 = svgwrite.Drawing('path_1.svg', profile='full')
        path_2 = svgwrite.Drawing('path_2.svg', profile='full')
        path_3 = svgwrite.Drawing('path_3.svg', profile='full')
        for i in range(len(path) - 1):
            for tree in tree_18:
                 p1 = get_point_by_id(tree, path[i])
                 p2 = get_point_by_id(tree, path[i+1])
                 if p1 and p2:
                    if (p1 and p2) is not None:
                         if p1[0][3] == p2[0][3]:
                            if p1[0][3] == 0:
                                path_0.add(path_0.line((p1[0][0], p1[0][1]), (p2[0][0], p2[0][1]), stroke=svgwrite.rgb(60, 10, 16, '%'), stroke_width = '5', opacity='0.7'))
                                has_level_0 = True
                            elif p1[0][3] == 1:
                                path_1.add(path_1.line((p1[0][0], p1[0][1]), (p2[0][0], p2[0][1]), stroke=svgwrite.rgb(60, 10, 16, '%'), stroke_width = '5'))
                                has_level_1 = True
                            elif p1[0][3] == 2:
                                path_2.add(path_2.line((p1[0][0], p1[0][1]), (p2[0][0], p2[0][1]), stroke=svgwrite.rgb(60, 10, 16, '%'), stroke_width = '5'))
                                has_level_2 = True
                            elif p1[0][3] == 3:
                                path_3.add(path_3.line((p1[0][0], p1[0][1]), (p2[0][0], p2[0][1]), stroke=svgwrite.rgb(60, 10, 16, '%'), stroke_width = '5'))
                                has_level_3 = True
                 else:
                     continue

        for tree in tree_18:
            p1 = get_point_by_id(tree, path[0])
            if p1:
                if p1 is not None:
                    if p1[0][3] == 0:
                        path_0.add(path_0.circle((p1[0][0], p1[0][1]), r=10, fill='green', opacity='1',
                                               stroke='none'))
                    elif p1[0][3] == 1:
                        path_1.add(path_1.circle((p1[0][0], p1[0][1]), r=10, fill='green', opacity='1',
                                                 stroke='none'))
                    elif p1[0][3] == 2:
                        path_2.add(path_2.circle((p1[0][0], p1[0][1]), r=10, fill='green', opacity='1',
                                                 stroke='none'))
                    elif p1[0][3] == 3:
                        path_3.add(path_3.circle((p1[0][0], p1[0][1]), r=10, fill='green', opacity='1',
                                                 stroke='none'))

            else:
                continue

        for tree in tree_18:
            p2 = get_point_by_id(tree, path[-1])
            if p2:
                if p2 is not None:
                    if p2[0][3] == 0:
                        path_0.add(path_0.circle((p2[0][0], p2[0][1]), r=10, fill='purple', opacity='1',
                                               stroke='none'))
                    elif p2[0][3] == 1:
                        path_1.add(path_1.circle((p2[0][0], p2[0][1]), r=10, fill='purple', opacity='1',
                                                 stroke='none'))
                    elif p2[0][3] == 2:
                        path_2.add(path_2.circle((p2[0][0], p2[0][1]), r=10, fill='purple', opacity='1',
                                                 stroke='none'))
                    elif p2[0][3] == 3:
                        path_3.add(path_3.circle((p2[0][0], p2[0][1]), r=10, fill='purple', opacity='1',
                                                 stroke='none'))

            else:
                continue

        path_1.save()
        path_0.save()
        path_2.save()
        path_3.save()

        for title in delete_list:
            os.remove(title)
            delete_list.remove(title)

        map_0 = st.fromfile('static/18_0.svg')
        path_svg_0 = st.fromfile('path_0.svg')
        map_0.append(path_svg_0)
        file_name_0 = 'static/route_0_' + str(random.randint(0,100000000)) + '.svg'
        map_0.save(file_name_0)

        map_1 = st.fromfile('static/18_1.svg')
        path_svg_1 = st.fromfile('path_1.svg')
        map_1.append(path_svg_1)
        file_name_1 = 'static/route_1_' + str(random.randint(0, 100000000)) + '.svg'
        map_1.save(file_name_1)

        map_2 = st.fromfile('static/18_2.svg')
        path_svg_2 = st.fromfile('path_2.svg')
        map_2.append(path_svg_2)
        file_name_2 = 'static/route_2_' + str(random.randint(0, 100000000)) + '.svg'
        map_2.save(file_name_2)

        map_3 = st.fromfile('static/18_3.svg')
        path_svg_3 = st.fromfile('path_3.svg')
        map_3.append(path_svg_3)
        file_name_3 = 'static/route_3_' + str(random.randint(0, 100000000)) + '.svg'
        map_3.save(file_name_3)

        delete_list.append(file_name_0)
        delete_list.append(file_name_1)
        delete_list.append(file_name_2)
        delete_list.append(file_name_3)

        return render_template('submit.html', button_pressed=button_pressed, file_name_0=file_name_0, file_name_1=file_name_1,
                               file_name_2=file_name_2, file_name_3=file_name_3, has_level_0=has_level_0, has_level_1=has_level_1,
                               has_level_2=has_level_2, has_level_3=has_level_3, starting_level_is_0=starting_level_is_0,
                               starting_level_is_1=starting_level_is_1, starting_level_is_2=starting_level_is_2,
                               starting_level_is_3=starting_level_is_3, starting_level=starting_level)


    return render_template('submit.html', button_pressed=button_pressed)


if __name__ == '__main__':
    delete_list = []
    GRAPH = nx.Graph()



    doors_id = {'001': 'path4041', '002': 'path4041-3', '003': 'path4041-6', '004': 'path4041-7', '005': 'path4041-5',
                '006': 'path4041-62',
                '007': 'path4041-94', '008': 'path4041-931', '009': 'path4041-35', '010': 'path4041-9', '011': 'path4041-1',
                '012': 'path4041-60',
                '013': 'path4041-626', '014': 'path4041-93', '015': 'path4041-78', '016': 'path4878-65-0-9-0-1', '017': 'path4041-0',
                '018': 'path4041-15',
                '019': 'path4041-63', '020': 'path4041-206', '021': 'path4041-50', '022': 'path4041-937-9',
                '023': 'path4041-361',
                '024': 'path4041-937',
                '025': 'path4041-937-2', '026': 'path4041-56', '027': 'path4041-54', '028': 'path4041-76', '029': 'path4041-76-6',
                '030': 'path4041-44-2',
                '031': 'path4041-23-5', '032': 'path4041-92', '033': 'path4041-23', '034': 'path4041-20', '035': 'path4878-65-856-7',
                '036': 'path4041-18', '037': 'path4039', '038': 'path4041-54-9', '039': 'path4878-65-856-7-35-7-7', '040': 'path4041-76-27',
                '041': 'path4041-76-93',
                '042': 'path4041-76-0-9', '043': 'path4041-76-0-7', '044': 'path4041-76-0-2',

                '101': 'path4041-76-0-2-3-60', '102': 'path4041-76-0-2-3-8', '103': 'path4041-76-0-2-3-0', '104': 'path4041-76-0-2-3-61', '105': 'path4041-76-0-2-3-27',
                '106': 'path4041-76-0-2-3-1', '107': 'path4041-76-0-2-3-2', '108': 'path4041-76-0-2-3-20', '109': 'path4041-76-0-2-3-5', '110': 'path4041-76-0-2-3-56',
                '111': 'path4041-76-0-2-3-3', '112': 'path4041-76-0-2-3-7', '113': 'path4041-76-0-2-3-23', '114': 'path4041-76-0-2-3-75', '115': 'path4041-76-0-2-3-92',
                '116': 'path4041-76-0-2-3', '117': 'path4041-76-0-2-3-97', '118': 'path4041-76-0-2-3-28', '119': 'path4041-76-0-2-3-78', '120': 'path4041-76-0-2-3-30',
                '121': 'path4041-76-0-2-3-178', '122': 'path4041-76-0-2-3-57', '123': 'path4041-76-0-2-3-41', '124': 'path4041-76-0-2-3-859', '125': 'path4041-76-0-2-3-361',
                '126': 'path4041-76-0-2-3-50', '127': 'path4041-76-0-2-3-06', '128': 'path4041-76-0-2-3-64', '129': 'path4041-76-0-2-3-15', '130': 'path4041-76-0-2-3-561-2',
                '131': 'path4041-76-0-2-3-561', '132': 'path4041-76-0-2-3-38', '133': 'path4041-76-0-2-3-096', '134': 'path4041-76-0-2-3-85', '135': 'path4041-76-0-2-3-26',
                '136': 'path4041-76-0-2-3-89', '137': 'path4041-76-0-2-3-86-1', '138': 'path4041-76-0-2-3-86-0', '139': 'path4041-76-0-2-3-07', '140': 'path4041-76-0-2-3-43',
                '141': 'path4041-76-0-2-3-65', '142': 'path4041-76-0-2-3-47', '143': 'path4041-76-0-2-3-55', '144': 'path4041-76-0-2-3-45', '145': 'path4041-76-0-2-3-474',
                '146': 'path4041-76-0-2-3-431', '147': 'path4041-76-0-2-3-49', '148': 'path4041-76-0-2-3-206', '149': 'path4041-76-0-2-3-32', '150': 'path4041-76-0-2-3-04',
                '151': 'path4041-76-0-2-3-87', '152': 'path4041-76-0-2-3-177', '153': 'path4041-76-0-2-3-949-3', '154': 'path4041-76-0-2-3-949', '155': 'path4041-76-0-2-3-17',
                '156': 'path4041-76-0-2-3-0615', '157': 'path4041-76-0-2-3-272', '158': 'path4041-76-0-2-3-261', '159': 'path4041-76-0-2-3-11', '160': 'path4041-76-0-2-3-59',
                '161': 'path4041-76-0-2-3-77', '162': 'path4041-76-0-2-3-67', '163': 'path4041-76-0-2-3-77', '164': 'path4041-76-0-2-3-63', '165': 'path4041-76-0-2-3-365',
                '166': 'path4041-76-0-2-3-48', '167': 'path4041-76-0-2-3-10', '168': 'path4041-76-0-2-3-44', '169': 'path4041-76-0-2-3-447', '170': 'path4041-76-0-2-3-631',
                '171': 'path4041-76-0-2-3-62', '172': 'path4041-76-0-2-3-759', '173': 'path4041-76-0-2-3-948', '174': 'path4041-76-0-2-3-129', '175': 'path4041-76-0-2-3-39',
                '176': 'path4041-76-0-2-3-08', '177': 'path4041-76-0-2-3-753', '178': 'path4041-76-0-2-3-88', '179': 'path4041-76-0-2-3-896',
                '201': 'path4041-76-0-2-3-87-75', '202': 'path4041-76-0-2-3-87-52', '203': 'path4041-76-0-2-3-87-20', '204': 'path4041-76-0-2-3-87-5', '205': 'path4041-76-0-2-3-87-4',
                '206': 'path4041-76-0-2-3-87-91', '207': 'path4041-76-0-2-3-87-910', '208': 'path4041-76-0-2-3-87-8', '209': 'path4041-76-0-2-3-87-48', '210': 'path4041-76-0-2-3-87-0',
                '211': 'path4041-76-0-2-3-87-96', '212': 'path4041-76-0-2-3-87-10', '213': 'path4041-76-0-2-3-87-42', '214': 'path4041-76-0-2-3-87-90', '215': 'path4041-76-0-2-3-87-28',
                '216': 'path4041-76-0-2-3-87-28', '217': 'path4041-76-0-2-3-87-04', '218': 'path4041-76-0-2-3-87-09', '219': 'path4041-76-0-2-3-87-19', '220': 'path4041-76-0-2-3-87-62',
                '221': 'path4041-76-0-2-3-87-54', '222': 'path4041-76-0-2-3-87-49', '223': 'path4041-76-0-2-3-87-93', '224': 'path4041-76-0-2-3-87-60', '225': 'path4041-76-0-2-3-87-50',
                '226': 'path4041-76-0-2-3-87-29', '227': 'path4041-76-0-2-3-87-43', '228': 'path4041-76-0-2-3-87-31', '229': 'path4041-76-0-2-3-87-46', '230': 'path4041-76-0-2-3-87-94',
                '231': 'path4041-76-0-2-3-87-22', '232': 'path4041-76-0-2-3-87-64', '233': 'path4041-76-0-2-3-87-12', '234': 'path4041-76-0-2-3-87-88', '235': 'path4041-76-0-2-3-87-92',
                '236': 'path4041-76-0-2-3-87-888', '237': 'path4041-76-0-2-3-87-68', '238': 'path4041-76-0-2-3-87-383', '239': 'path4041-76-0-2-3-87-9', '240': 'path4041-76-0-2-3-87-2',
                '241': 'path4041-76-0-2-3-87-3', '242': 'path4041-76-0-2-3-87-1', '243': 'path4041-76-0-2-3-87-6', '244': 'path4041-76-0-2-3-87-7', '245': 'path4041-76-0-2-3-87-7-3',

                '301': 'path4041-76-0-2-3-87-910-787', '302': 'path4041-76-0-2-3-87-910-90', '303': 'path4041-76-0-2-3-87-910-41', '304': 'path4041-76-0-2-3-87-910-85', '305': 'path4041-76-0-2-3-87-910-84',
                '306': 'path4041-76-0-2-3-87-910-371', '307': 'path4041-76-0-2-3-87-910-380', '308': 'path4041-76-0-2-3-87-910-979', '309': 'path4041-76-0-2-3-87-910-932', '310': 'path4041-76-0-2-3-87-910-932',
                '311': 'path4041-76-0-2-3-87-910-71', '312': 'path4041-76-0-2-3-87-910-2', '313': 'path4041-76-0-2-3-87-910-20', '314': 'path4041-76-0-2-3-87-910-21', '315': 'path4041-76-0-2-3-87-910-75',
                '316': 'path4041-76-0-2-3-87-910-417', '317': 'path4041-76-0-2-3-87-910-17', '318': 'path4041-76-0-2-3-87-910-11', '319': 'path4041-76-0-2-3-87-910-170', '320': 'path4041-76-0-2-3-87-910-40',
                '321': 'path4041-76-0-2-3-87-910-851', '322': 'path4041-76-0-2-3-87-910-219', '323': 'path4041-76-0-2-3-87-910-64', '324': 'path4041-76-0-2-3-87-910-02', '325': 'path4041-76-0-2-3-87-910-80',
                '326': 'path4041-76-0-2-3-87-910-81', '327': 'path4041-76-0-2-3-87-910-29', '328': 'path4041-76-0-2-3-87-910-756', '329': 'path4041-76-0-2-3-87-910-379', '330': 'path4041-76-0-2-3-87-910-46',
                '331': 'path4041-76-0-2-3-87-910-74', '332': 'path4041-76-0-2-3-87-910-91', '333': 'path4041-76-0-2-3-87-910-70', '334': 'path4041-76-0-2-3-87-910-539', '335': 'path4041-76-0-2-3-87-910-608',
                '336': 'path4041-76-0-2-3-87-910-415', '337': 'path4041-76-0-2-3-87-910-1', '338': 'path4041-76-0-2-3-87-910-0', '339': 'path4041-76-0-2-3-87-910-9', '340': 'path4041-76-0-2-3-87-910-4-3',
                '341': 'path4041-76-0-2-3-87-910-4', '342': 'path4041-76-0-2-3-87-910-5', '343': 'path4041-76-0-2-3-87-910-8', '344': 'path4041-76-0-2-3-87-910-86', '345': 'path4041-76-0-2-3-87-910-3',
                '346': 'path4041-76-0-2-3-87-910-3', '347': 'path4041-76-0-2-3-87-910-04', '348': 'path4041-76-0-2-3-87-910-7', '349': 'path4041-76-0-2-3-87-910-60', '350': 'path4041-76-0-2-3-87-910-59',
                '351': 'path4041-76-0-2-3-87-910-97', '352': 'path4041-76-0-2-3-87-910-78', '353': 'path4041-76-0-2-3-87-910-53', '354': 'path4041-76-0-2-3-87-910-38', '355': 'path4041-76-0-2-3-87-910-37',
                '356': 'path4041-76-0-2-3-87-910-93'
    }



    # Expirement 2
    tree_18 = []
    tree_18.append(read_svg_file('static/18_0.svg'))
    tree_18.append(read_svg_file('static/18_1.svg'))
    tree_18.append(read_svg_file('static/18_2.svg'))
    tree_18.append(read_svg_file('static/18_3.svg'))

    get_adjacency_from_graph(tree_18[0], GRAPH)

    GRAPH.add_edge('path4878-65-15', 'path4878-65-1')
    GRAPH.add_edge('path4878-65-856', 'path4878-65-856-3')
    GRAPH.add_edge('path4041-23', 'path4878-65-98')
    GRAPH.add_edge('path4878-65-856-6', 'path4878-65-856-5')
    GRAPH.add_edge('path4878-65-856-7', 'path4878-65-856-7-6')
    GRAPH.add_edge('path4878-65-856-7-2', 'path4041-18')
    GRAPH.add_edge('path4878-97', 'path4878-76')
    GRAPH.add_edge('path4878-65', 'path4878-65-0')
    GRAPH.add_edge('path4041-0', 'path4878-65-0-9-2')
    GRAPH.add_edge('path4878-71', 'path4041-1')
    GRAPH.add_edge('path4878-49', 'path4878-10')
    GRAPH.add_edge('path4878-10', 'path4878-09')
    GRAPH.add_edge('path4878-09', 'path4041-70')
    GRAPH.add_edge('path4041-2', 'path4878-17')
    GRAPH.add_edge('path4878-17', 'path4878-6')
    GRAPH.add_edge('path4041-76-0-7', 'path4041-76-0-3')
    GRAPH.add_edge('path4041-76-0-5', 'path4041-76-0-9')
    GRAPH.add_edge('path4878-65-856-7-35-2-3', 'path4878-65-856-7-35-2-6')
    GRAPH.add_edge('path4041-76-60', 'path4041-76-93')
    GRAPH.add_edge('path4878-65-856-7-35-7-36', 'path4878-65-856-7-35-1')
    GRAPH.add_edge('path4878-65-856-7-35-7', 'path4878-65-856-7-35-9')
    GRAPH.add_edge('path4878-65-856-7-35-7-6', 'path4878-65-856-7-35-7-7')
    GRAPH.add_edge('path4041-76-27', 'path4041-76-0')
    GRAPH.add_edge('path4878-65-856-7-35-20', 'path4041-44')
    GRAPH.add_edge('path4878-63-90', 'path4878-63-3')
    GRAPH.add_edge('path4041-25', 'path4878-63-1')
    GRAPH.add_edge('path4041-56', 'path4878-63-2')
    GRAPH.add_edge('path4041-937', 'path4878-63-2-3')
    GRAPH.add_edge('path4878-63-2', 'path4878-65-0-9-0')
    GRAPH.add_edge('path4878-65-0-9-0', 'path4878-65-0-9-7')
    GRAPH.add_edge('path4041-50', 'path4878-65-0-9-0-3')
    GRAPH.add_edge('path4878-63-2-5', 'path4878-63-2-7')
    GRAPH.add_edge('path4878-4', 'path4878')
    GRAPH.add_edge('path4878-65-856-7-35', 'path4878-65-856-7-5')
    GRAPH.add_edge('path4041-76', 'path4878-63-4')
    GRAPH.add_edge('path4878-6', 'path4878-722')
    GRAPH.add_edge('path4041-62', 'path4878-15')
    GRAPH.add_edge('path4878-72', 'path4878-1')
    GRAPH.add_edge('path4878-1', 'path4878-7')
    GRAPH.add_edge('path4878-7', 'path4878-8')
    GRAPH.add_edge('path4878-8', 'path4878-8-3')
    GRAPH.add_edge('path4041-70', 'path4878-65-0-9-1')
    GRAPH.add_edge('path4041-2', 'path4878-65-0-9-1')

    get_adjacency_from_graph(tree_18[1], GRAPH)

    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-19', 'path4041-76-0-2-3-0615')
    GRAPH.add_edge('path4041-76-0-2-3-0615', 'path4041-76-0-2-3-27-0-48-9-039')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-039', 'path4041-76-0-2-3-27-0-48-9-4')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-4', 'path4041-76-0-2-3-27-0-48-9-03')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-03', 'path4041-76-0-2-3-27-0-48-9-11')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-11', 'path4041-76-0-2-3-27-0-48-9-8')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-69', 'path4041-76-0-2-3-27-0-48-9-3')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-3', 'path4041-76-0-2-3-27-0-48-9-38')
    GRAPH.add_edge('path4041-76-0-2-3-39', 'path4041-76-0-2-3-27-0-48-9-66')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-66', 'path4041-76-0-2-3-27-0-48-9-05')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-05', 'path4041-76-0-2-3-27-0-1-2-2')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-1-2-2', 'path4041-76-0-2-3-27-0-48-2-5-56')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-2-5-3', 'path4041-76-0-2-3-85')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-7', 'path4041-76-0-2-3-27-0-48-9-24')

    GRAPH.add_edge('path4041-76-0-2-3-6-3', 'path4041-76-0-2-3-27-0-75')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-0', 'path4041-76-0-2-3-27-0-48-9-62')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-2', 'path4041-76-0-2-3-27-0-48-9-7')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-2', 'path4041-76-0-2-3-27-0-48-9-6')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-6', 'path4041-76-0-2-3-15')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-3', 'path4041-76-0-2-3-27-0-48-6')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-1', 'path4041-76-0-2-3-27-0-75')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-75', 'path4041-76-0-2-3-27-0-47')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-47', 'path4041-76-0-2-3-27-0-922')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-922', 'path4041-76-0-2-3-27-0-46')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-46', 'path4041-76-0-2-3-27-0-5')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-5', 'path4041-76-0-2-3-27-0-92')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-92', 'path4041-76-0-2-3-27-0-3')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-3', 'path4041-76-0-2-3-27-0-43')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-43', 'path4041-76-0-2-3-27-0-76')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-76', 'path4041-76-0-2-3-27-0-7')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-9', 'path4041-76-0-2-3-27-0-7')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-9', 'path4041-76-0-2-3-27-0-48-2-5-62')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-4', 'path4041-76-0-2-3-27-0-8')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-2-6', 'path4041-76-0-2-3-27-0-48-2-58')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-2-4', 'path4041-76-0-2-3-27-0-48-2-6')
    GRAPH.add_edge('path4041-76-0-2-3-50', 'path4041-76-0-2-3-27-0-48-2-62')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-2-5-5', 'path4041-76-0-2-3-061')
    GRAPH.add_edge('path4041-76-0-2-3-45', 'path4041-76-0-2-3-25')
    GRAPH.add_edge('path4041-76-0-2-3-65', 'path4041-76-0-2-3-27-0-48-2-8')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-2-8', 'path4041-76-0-2-3-27-0-48-2-10')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-2-50', 'path4041-76-0-2-3-27-0-48-2-10')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-2-50', 'path4041-76-0-2-3-49')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-2', 'path4041-76-0-2-3-27-0-48-80')
    GRAPH.add_edge('path4041-76-0-2-3-47', 'path4041-76-0-2-3-27-0-48-2-8')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-6', 'path4041-76-0-2-3-27-0-48-9-8')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-9', 'path4041-76-0-2-3-04')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-1-2-0', 'path4041-76-0-2-3-27-0-1-2-6')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-1-6', 'path4041-76-0-2-3-27-0-1-2')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-1-6', 'path4041-76-0-2-3-27-0-1-04')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-1-04', 'path4041-76-0-2-3-27-0-1-4')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-1-0', 'path4041-76-0-2-3-27-0-1-9')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-1-8', 'path4041-76-0-2-3-27-0-1-5')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-1-5', 'path4041-76-0-2-3-27-0-1-69')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-1-5', 'path4041-76-0-2-3-27-0-1-67')
    GRAPH.add_edge('path4041-76-0-2-3-27-0', 'path4041-76-0-2-3-27-0-8')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-4-6', 'path4041-76-0-2-3-31')
    GRAPH.add_edge('path4041-76-0-2-3-31', 'path4041-76-0-2-3-27-0-48-2-5-2')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-2-5-2', 'path4041-76-0-2-3-27-0-48-2-5-2')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-2-5-2', 'path4041-76-0-2-3-27-0-48-2-5-1')
    GRAPH.add_edge('path4041-76-0-2-3-631', 'path4041-76-0-2-3-27-0-48-2-5-93')
    GRAPH.add_edge('path4041-76-0-2-3-631', 'path4041-76-0-2-3-27-0-48-2-5-27')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-40', 'path4041-76-0-2-3-5')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-2-5-36', 'path4041-76-0-2-3-27-0-48-2-5')
    GRAPH.add_edge('path4041-76-0-2-3-86-1', 'path4041-76-0-2-3-86-0')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-8', 'path4041-76-0-2-3-27-0-48-9')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-24', 'path4041-76-0-2-3-27-0-48-9-0')
    GRAPH.add_edge('path4041-76-0-2-3-12', 'path4041-95')
    GRAPH.add_edge('path4041-23-3', 'path4041-76-0-2-3-931-6-0')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-1', 'path4041-76-0-2-3-27-0-1-4')

    get_adjacency_from_graph(tree_18[2], GRAPH)
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-019', 'path4041-76-0-2-3-931-6-0-7-6')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-02', 'path4041-76-0-2-3-27-0-48-9-90-49')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-49', 'path4041-76-0-2-3-27-0-48-9-90-53')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-97', 'path4041-76-0-2-3-27-0-48-9-90-73')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-19', 'path4041-76-0-2-3-27-0-48-9-90-45')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-45', 'path4041-76-0-2-3-87-10')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-45', 'path4041-76-0-2-3-27-0-48-9-90-74')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-74', 'path4041-76-0-2-3-931-6-0-6')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-54', 'path4041-76-0-2-3-27-0-48-9-90-91')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-91', 'path4041-76-0-2-3-27-0-48-9-90-91')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-91', 'path4041-76-0-2-3-27-0-48-9-90-01')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-01', 'path4041-76-0-2-3-27-0-48-9-90-92')
    GRAPH.add_edge('path4041-76-0-2-3-931-6-0-8', 'path4041-76-0-2-3-27-0-48-9-90-83')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-83', 'path4041-76-0-2-3-27-0-48-9-90-92')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-92', 'path4041-76-0-2-3-27-0-48-9-90-93')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-93', 'path4041-76-0-2-3-27-0-48-9-90-47')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-62', 'path4041-76-0-2-3-27-0-48-9-90-8')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-8', 'path4041-76-0-2-3-27-0-48-9-90-70')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-70', 'path4041-76-0-2-3-27-0-48-9-90-0')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-1', 'path4041-76-0-2-3-27-0-48-9-90-4')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-4', 'path4041-76-0-2-3-27-0-48-9-90-60')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-60', 'path4041-76-0-2-3-27-0-48-9-90-9')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-7', 'path4041-76-0-2-3-27-0-48-9-90-58')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-58', 'path4041-76-0-2-3-27-0-48-9-90-5')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-5', 'path4041-76-0-2-3-87-22')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-5', 'path4041-76-0-2-3-27-0-48-9-90-6')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-6', 'path4041-76-0-2-3-27-0-48-9-90-2')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-2', 'path4041-76-0-2-3-27-0-48-9-90-3')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-3', 'path4041-76-0-2-3-931-6-9')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-73', 'path4041-76-0-2-3-27-0-48-9-90-11')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-11', 'path4041-76-0-2-3-27-0-48-9-90-56')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-56', 'path4041-76-0-2-3-27-0-48-9-90-77')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-77', 'path4041-76-0-2-3-27-0-48-9-90-40')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-40', 'path4041-76-0-2-3-27-0-48-9-90-64')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-64', 'path4041-76-0-2-3-27-0-48-9-90-748')
    GRAPH.add_edge('path4041-76-0-2-3-36', 'path4041-76-0-2-3-931-6-0-6')
    GRAPH.add_edge('path4041-76-0-2-3-87-383-3', 'path4041-76-0-2-3-27-0-48-9-90-3')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-3-3', 'path4041-76-0-2-3-433')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-49-3', 'path4041-76-0-2-3-27-0-48-9-90-20')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-49-3', 'path4041-76-0-2-3-27-0-48-9-90-97')
    GRAPH.add_edge('path4041-76-0-2-3-931-6-0-7', 'path4041-76-0-2-3-931')

    get_adjacency_from_graph(tree_18[3], GRAPH)
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-82-1', 'path4041-76-0-2-3-27-0-48-9-90-82-5')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-82-5', 'path4041-76-0-2-3-27-0-48-9-90-82-54')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-82-54', 'path4041-76-0-2-3-27-0-48-9-90-82-9')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-82-9', 'path4041-76-0-2-3-27-0-48-9-90-82-8')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-82-8', 'path4041-76-0-2-3-27-0-48-9-90-82-3')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-82-3', 'path4041-76-0-2-3-27-0-48-9-90-82-85')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-82-85', 'path4041-76-0-2-3-27-0-48-9-90-82-2')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-82-2', 'path4041-76-0-2-3-87-910-43')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-82-7', 'path4041-76-0-2-3-27-0-48-9-90-82-0')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-82-34', 'path4041-76-0-2-3-87-910-17')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-82-6-3', 'path4041-76-0-2-3-27-0-48-9-90-82-6')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-82-6', 'path4041-76-0-2-3-27-0-48-9-90-82-36')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-82-36', 'path4041-76-0-2-3-27-0-48-9-90-82-33')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-82-44', 'path4041-76-0-2-3-27-0-48-9-90-82-72')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-82-58', 'path4041-76-0-2-3-27-0-48-9-90-82-90')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-82-72', 'path4041-76-0-2-3-27-0-48-9-90-82-39')
    GRAPH.add_edge('path4041-76-0-2-3-87-910-219', 'path4041-76-0-2-3-27-0-48-9-90-82-24')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-82-39', 'path4041-76-0-2-3-27-0-48-9-90-82-76')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-82-76', 'path4041-76-0-2-3-27-0-48-9-90-82-57')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-82-57', 'path4041-76-0-2-3-27-0-48-9-90-82-13')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-82-13', 'path4041-76-0-2-3-27-0-48-9-90-82-338')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-82-338', 'path4041-76-0-2-3-27-0-48-9-90-82-51')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-82-51', 'path4041-76-0-2-3-27-0-48-9-90-82-08')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-82-08', 'path4041-76-0-2-3-27-0-48-9-90-82-763')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-82-50', 'path4041-76-0-2-3-27-0-48-9-90-82-763')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-82-50', 'path4041-76-0-2-3-931-4')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-82-508', 'path4041-76-0-2-3-27-0-48-9-90-82-761')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-82-761', 'path4041-76-0-2-3-87-910-9')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-82-761', 'path4041-76-0-2-3-27-0-48-9-90-82-63')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-82-63', 'path4041-76-0-2-3-27-0-48-9-90-82-59')
    GRAPH.add_edge('path4041-76-0-2-3-87-910-3', 'path4041-76-0-2-3-27-0-48-9-90-82-907')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-82-59', 'path4041-76-0-2-3-27-0-48-9-90-82-56')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-82-56', 'path4041-76-0-2-3-27-0-48-9-90-82-083')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-82-083', 'path4041-76-0-2-3-27-0-48-9-90-82-415')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-82-415', 'path4041-76-0-2-3-27-0-48-9-90-82-93')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-82-93', 'path4041-76-0-2-3-27-0-48-9-90-82-135')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-82-135', 'path4041-76-0-2-3-27-0-48-9-90-82-41')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-82-41', 'path4041-76-0-2-3-27-0-48-9-90-82-80')
    GRAPH.add_edge('path4041-76-0-2-3-931-6-0-48', 'path4041-76-0-2-3-27-0-48-9-90-82-26')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-82-22-3', 'path4041-76-0-2-3-27-0-48-9-90-82-22')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-82-4-3', 'path4041-76-0-2-3-27-0-48-9-90-82-4-3')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-82-4-3', 'path4041-76-0-2-3-27-0-48-9-90-82-1')
    GRAPH.add_edge('path4041-76-0-2-3-931-6-0-0-3', 'path4041-76-0-2-3-27-0-48-9-90-82-4-3')


    GRAPH.add_edge('path4041-76-0-2-3-931-6-2', 'path4041-76-0-2-3-931-6-0-4')
    GRAPH.add_edge('path4041-76-0-2-3-931-6-9', 'path4041-76-0-2-3-931-4-3')
    GRAPH.add_edge('path4041-76-0-2-3-27-0-48-9-90-82-22-3', 'path4041-76-0-2-3-931-6')
    GRAPH.add_edge('path4041-76-0-2-3-931-6-0-0', 'path4041-76-0-2-3-931-6-0-7-6')
    GRAPH.add_edge('path4041-76-0-2-3-931-6-0-48', 'path4041-76-0-2-3-931-9')

    dwg_0 = svgwrite.Drawing('level_0.svg', profile='full')
    dwg_1 = svgwrite.Drawing('level_1.svg', profile='full')
    dwg_2 = svgwrite.Drawing('level_2.svg', profile='full')
    dwg_3 = svgwrite.Drawing('level_3.svg', profile='full')

    for edge in GRAPH.edges():
        for tree in tree_18:
            p1 = get_point_by_id(tree, edge[0])
            p2 = get_point_by_id(tree, edge[1])
            if p1 and p2:
                if (p1 and p2) is not None:
                    if p1[0][3] == p2[0][3]:
                        if p1[0][3] == 0:
                            dwg_0.add(
                                dwg_0.line((p1[0][0], p1[0][1]), (p2[0][0], p2[0][1]), stroke=svgwrite.rgb(10, 10, 16, '%')))

                        elif p1[0][3] == 1:
                            dwg_1.add(dwg_1.line((p1[0][0], p1[0][1]), (p2[0][0], p2[0][1]),
                                                 stroke=svgwrite.rgb(10, 10, 16, '%')))
                        elif p1[0][3] == 2:
                            dwg_2.add(dwg_2.line((p1[0][0], p1[0][1]), (p2[0][0], p2[0][1]),
                                                 stroke=svgwrite.rgb(10, 10, 16, '%')))
                        elif p1[0][3] == 3:
                            dwg_3.add(dwg_3.line((p1[0][0], p1[0][1]), (p2[0][0], p2[0][1]),
                                                 stroke=svgwrite.rgb(10, 10, 16, '%')))
            else:
                continue
    dwg_1.save()
    dwg_0.save()
    dwg_2.save()
    dwg_3.save()

    template_0 = st.fromfile('static/18_0.svg')
    second_svg_0 = st.fromfile('level_0.svg')
    template_0.append(second_svg_0)
    file_name = 'static/plan_0.svg'
    template_0.save(file_name)

    template_1 = st.fromfile('static/18_1.svg')
    second_svg_1 = st.fromfile('level_1.svg')
    template_1.append(second_svg_1)
    file_name = 'static/plan_1.svg'
    template_1.save(file_name)

    template_2 = st.fromfile('static/18_2.svg')
    second_svg_2 = st.fromfile('level_2.svg')
    template_2.append(second_svg_2)
    file_name = 'static/plan_2.svg'
    template_2.save(file_name)

    template_3 = st.fromfile('static/18_3.svg')
    second_svg_3 = st.fromfile('level_3.svg')
    template_3.append(second_svg_3)
    file_name = 'static/plan_3.svg'
    template_3.save(file_name)


    app.debug = False
    app.run(host='192.168.0.28', port=8080)


