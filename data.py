import argparse
import json
import os
import glob
import re
from time import sleep
from math import cos, sin, radians, degrees, asin, atan2
import numpy as np

if __name__ == '__main__':
    # https://www.google.com/maps/d/u/0/viewer?mid=1Kn1r0J6jdb6VR1tRXt7dIrJN3LA&ll=24.9682276%2C121.19437649999998&z=17
    gate3 = [(24.96715, 121.18766), (24.96822, 121.19437), (24.97154, 121.19268)]
    file3 = [None] * 3
    file_dict = set()
    file_sz = 0
    sec = 1
    earthR = 6371



    while True:

        for fn in glob.glob('testData/*.txt'):
            # testData\\107522xxx_008000000000e331_1_3_7_5.txt
            # get                                  ↑
            loc = int(re.search(r'[a-zA-Z0-9]+\\[a-zA-Z0-9]+_[a-zA-Z0-9]+_(\d).*', fn).group(1))
            if file3[loc - 1] is None:
                file3[loc - 1] = fn
            # compare time, get the latest file
            elif os.path.getatime(fn) > os.path.getatime(file3[loc - 1]):
                file3[loc - 1] = fn

            file_dict.add(fn)

        if len(file_dict) > file_sz:
            file_sz = len(file_dict)
            if None not in file3:
                point3 = []
                dis3 = []
                for i, fn in enumerate(file3):
                    with open(fn, 'r') as f:
                        line = json.load(f)
                        rssi = line['result']['uplinkFrames'][0]['rxInfo'][0]['rssi']
                        # RSSI = -(10.η.log(d) + A), η = 3 , A = 9
                        # 2^(-rssi - 9) / 30 = d
                        dis = pow(2, (-rssi - 9) / 30)
                        dis /= 10.0
                        x = earthR * cos(radians(gate3[i][0])) * cos(radians(gate3[i][1]))
                        y = earthR * cos(radians(gate3[i][0])) * sin(radians(gate3[i][1]))
                        z = earthR * sin(radians(gate3[i][0]))
                        point3.append(np.array([x, y, z]))
                        dis3.append(dis)
                print(point3)
                # ref: https://gis.stackexchange.com/questions/66/trilateration-using-3-latitude-longitude-points-and-3-distances
                # ref: https://www.wikiwand.com/en/True_range_multilateration
                # ref: https://www.wikiwand.com/en/Geographic_coordinate_conversion
                p1 = point3[0]
                p2 = point3[1]
                p3 = point3[2]
                d1 = dis3[0]
                d2 = dis3[1]
                d3 = dis3[2]
                # print(dis3)
                # pt3 = []
                # for i in range(3):
                #     j = (i + 1) % 3
                #     pq = np.linalg.norm(point3[j] - point3[i])
                #     print(pow(dis3[i], 2))
                #     pc = pq / 2.0 + (pow(dis3[i], 2) - pow(dis3[j], 2)) / (pq * 2)
                #     print('pc: {}'.format(pc))
                #     print('pq: {}'.format(pq))
                #     print('(pow(dis3[i], 2) - pow(dis3[j], 2)): {}'.format((pow(dis3[i], 2) - pow(dis3[j], 2))))
                #     print('point3[i] + pc: {}'.format(point3[i] + pc))
                #     c = point3[i] + (point3[j] - point3[i]) * pc / pq
                #     pt3.append(c)
                # print('pt3: {}'.format(pt3))
                # pt = np.sum(pt3, axis=0) / 3.0
                # print('pt: {}'.format(pt))
                # lat = degrees(asin(pt[2] / earthR))
                # lng = degrees(atan2(pt[1], pt[0]))
                # print(lat, lng)



                norm_x = (p2 - p1) / np.linalg.norm(p2 - p1)
                Vx = np.dot(norm_x, p3 - p1)
                norm_y = (p3 - p1 - Vx * norm_x) / np.linalg.norm(p3 - p1 - Vx * norm_x)
                norm_z = np.cross(norm_x, norm_y)
                Vy = np.dot(norm_y, p3 - p1)
                U = np.linalg.norm(p2 - p1)

                x = (pow(d1, 2) - pow(d2, 2) + pow(U, 2)) / (U * 2)
                y = (pow(d1, 2) - pow(d3, 2) + pow(Vx, 2) + pow(Vy, 2) - 2 * Vx * x) / (2 * Vy)

                z = np.sqrt(abs(pow(d1, 2) - pow(x, 2) - pow(y, 2)))

                triPt = p1 + x * norm_x + y * norm_y + z * norm_z
                print(triPt)
                lat = degrees(asin(triPt[2] / earthR))
                lng = degrees(atan2(triPt[1], triPt[0]))
                print(lat, lng)

                points = []
                if os.path.exists('web/position.json'):
                    with open('web/position.json') as f:
                        points = json.load(f)
                else:
                    points = []
                pt = dict([('lat', lat), ('lng', lng)])
                if pt not in points:
                    points.append(pt)
                res = json.dumps(points)
                with open('web/position.json', 'w') as f:
                    f.write(res)


            else:
                print('miss some locations for positioning')
            sec = 1
        else:
            sleep(sec)
            sec = max(sec + sec, 32)




    # parser = argparse.ArgumentParser()
    # parser.add_argument('-m', '--mode', type=str, help='set action mode, [add, remove, clear]', required=True)
    # parser.add_argument('--lat', type=float, help='lat', required=True)
    # parser.add_argument('--lng', type=float, help='lng', required=True)
    # args = parser.parse_args()
    #
    # if os.path.exists('web/position.json'):
    #     with open('web/position.json') as f:
    #         points = json.load(f)
    # else:
    #     points = []
    #
    # if args.mode == 'add':
    #     pt = dict([('lat', args.lat), ('lng', args.lng)])
    #     if pt not in points:
    #         points.append(pt)
    #
    # res = json.dumps(points)
    # with open('web/position.json', 'w') as f:
    #     f.write(res)


# [{"lat": 24.9689352201779, "lng": 121.191933011529}, {"lat": 24.967277, "lng": 121.187729}]
