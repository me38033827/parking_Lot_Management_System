import json
import cv2
import numpy as np

if __name__ == '__main__':
    pos_file = json.load(open('./parking.pos', 'rb'))

    image = cv2.imread('./parking.png')
    tempX = 9
    tempY = 7
    print(image.shape)
    parking_lot = []
    enter = []
    exit_ = []
    first_v = []
    second_v = []
    first_h = []
    second_h = []

    for key in pos_file['diagram']['elements']['elements'].keys():
        if pos_file['diagram']['elements']['elements'][key]['textBlock'][0]['text'] == '' and \
                pos_file['diagram']['elements']['elements'][key]['props']['zindex'] != 1:
            if pos_file['diagram']['elements']['elements'][key]['props']['angle'] == 0:
                x = pos_file['diagram']['elements']['elements'][key]['props']['x'] - tempX + 90
                y = pos_file['diagram']['elements']['elements'][key]['props']['y'] + tempY + 40
            else:
                x = pos_file['diagram']['elements']['elements'][key]['props']['x'] + 50 - tempX + 40
                y = pos_file['diagram']['elements']['elements'][key]['props']['y'] - 50 + tempY + 90
            image[y:y+3, x:x+3] = (0, 0, 255)
            parking_lot.append([x, y, pos_file['diagram']['elements']['elements'][key]['props']['zindex']])

    for key in pos_file['diagram']['elements']['elements'].keys():
        if pos_file['diagram']['elements']['elements'][key]['textBlock'][0]['text'] != '':
            x = int(pos_file['diagram']['elements']['elements'][key]['props']['x']) - tempX + 77
            y = int(pos_file['diagram']['elements']['elements'][key]['props']['y']) + tempY + 17
            image[y:y+3, x:x+3] = (255, 0, 0)
            if pos_file['diagram']['elements']['elements'][key]['textBlock'][0]['text'] == 'Enter':
                enter.append([x, y, pos_file['diagram']['elements']['elements'][key]['props']['zindex']])
            else:
                exit_.append([x, y, pos_file['diagram']['elements']['elements'][key]['props']['zindex']])

    for key in pos_file['diagram']['elements']['elements'].keys():
        if pos_file['diagram']['elements']['elements'][key]['textBlock'][0]['text'] == '' and \
                1 < pos_file['diagram']['elements']['elements'][key]['props']['zindex'] < 7:
            x = int(pos_file['diagram']['elements']['elements'][key]['props']['x']) - tempX + 90 + 180
            y = int(pos_file['diagram']['elements']['elements'][key]['props']['y']) + tempY + 40
            image[y:y + 3, x:x + 3] = (0, 255, 0)
            first_v.append([x, y, pos_file['diagram']['elements']['elements'][key]['props']['zindex']])

    for key in pos_file['diagram']['elements']['elements'].keys():
        if pos_file['diagram']['elements']['elements'][key]['textBlock'][0]['text'] == '' and \
                18 < pos_file['diagram']['elements']['elements'][key]['props']['zindex'] < 24:
            print(pos_file['diagram']['elements']['elements'][key]['props'])
            x = int(pos_file['diagram']['elements']['elements'][key]['props']['x']) - tempX + 90 - 180
            y = int(pos_file['diagram']['elements']['elements'][key]['props']['y']) + tempY + 40
            image[y:y + 3, x:x + 3] = (0, 255, 0)
            second_v.append([x, y, pos_file['diagram']['elements']['elements'][key]['props']['zindex']])

    for key in pos_file['diagram']['elements']['elements'].keys():
        if pos_file['diagram']['elements']['elements'][key]['textBlock'][0]['text'] == '' and \
                6 < pos_file['diagram']['elements']['elements'][key]['props']['zindex'] < 13:
            print(pos_file['diagram']['elements']['elements'][key]['props'])
            x = pos_file['diagram']['elements']['elements'][key]['props']['x'] + 50 - tempX + 40
            y = pos_file['diagram']['elements']['elements'][key]['props']['y'] - 50 + tempY + 90 + 160
            image[y:y + 3, x:x + 3] = (0, 255, 0)
            first_h.append([x, y, pos_file['diagram']['elements']['elements'][key]['props']['zindex']])

    for key in pos_file['diagram']['elements']['elements'].keys():
        if pos_file['diagram']['elements']['elements'][key]['textBlock'][0]['text'] == '' and \
                12 < pos_file['diagram']['elements']['elements'][key]['props']['zindex'] < 19:
            print(pos_file['diagram']['elements']['elements'][key]['props'])
            x = pos_file['diagram']['elements']['elements'][key]['props']['x'] + 50 - tempX + 40
            y = pos_file['diagram']['elements']['elements'][key]['props']['y'] - 50 + tempY + 90 + 160
            image[y:y + 3, x:x + 3] = (0, 255, 0)
            second_h.append([x, y, pos_file['diagram']['elements']['elements'][key]['props']['zindex']])

    parking = {'parking_lot': parking_lot, 'enter': enter, 'exit': exit_, 'first_v': first_v, 'second_v': second_v,
               'first_h': first_h, 'second_h': second_h}

    json.dump(parking, open('./parking.json', 'w'))

    cv2.imshow('test', image)
    cv2.waitKey()
