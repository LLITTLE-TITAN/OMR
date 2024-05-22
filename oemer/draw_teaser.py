import typing
from PIL import Image
from typing import List, Optional, Tuple, Union

import cv2
import numpy as np

from oemer import layers
from numpy import ndarray

from oemer.bbox import BBox
from PIL import Image
from oemer.dewarp import estimate_coords, dewarp
# Globals
out: ndarray

def draw_bbox(
    bboxes: List[BBox],
    color: Tuple[int, int, int],
    text: Optional[str] = None,
    labels: Optional[List[str]] = None,
    text_y_pos: float = 1
) -> None:
    for idx, (x1, y1, x2, y2) in enumerate(bboxes):
        x_center = int((x1 + x2) / 2)
        y_center = int((y1 + y2) / 2)
        cv2.line(out, (x_center, y1), (x_center, y2), color, 5)
        # cv2.rectangle(out, (x1, y1), (x2, y2), color, 2)
        # y_pos = y1 + round((y2-y1)*text_y_pos)
        # if text is not None:
        #     cv2.putText(out, text, (x2+2, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 1)
        # elif labels is not None:
        #     cv2.putText(out, labels[idx], (x2+2, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 1)


def teaser() -> Image.Image:
    global out
    ori_img = layers.get_layer('original_image')
    out = np.copy(ori_img).astype(np.uint8)
    notes = layers.get_layer('notes')
    groups = layers.get_layer('note_groups')
    barlines = layers.get_layer('barlines')
    staffs = layers.get_layer('staffs')
    # print(left)
    # print(right)
    # out = np.copy(image).astype(np.uint8)
    # print(len(staffs))
    # for st in staffs.reshape(-1, 1).squeeze():
    #     start = st.y_upper
    #     end = st.y_lower
    #     count = 5
    #     dis = int((end - start) / count)
    #     for i in range(count):
    #         cv2.line(out, (left, start + dis * i), (right, start + dis * i), (0, 0, 0), 1)

    # draw_bbox([gg.bbox for gg in groups], color=(255, 192, 92), text="group")
    # draw_bbox([gg.bbox for gg in groups], color=(255, 192, 92), text="group")
    # draw_bbox([n.bbox for n in notes if not n.invalid], color=(194, 81, 167), labels=[str(n.label)[0] for n in notes if not n.invalid])
    # print(barlines)
    # print(f"len{len(barlines)}")
    # for b in barlines:
    #     # print(b)
    #     flag_start = 0
    #     flag_end = 0
    #     x1, y1, x2, y2 = b.bbox
    #     for st in staffs.reshape(-1, 1).squeeze():
    #         # print(st)
    #         start = st.y_upper
    #         end = st.y_lower
    #         print(f"group{b.group}")
    #         print(f"start{abs(y1 - start)}")
    #         print(f"end{abs(y2 - end)}")
    #         if abs(y1 - start) < 5:
    #             flag_start = 1
    #         if abs(y2 - end) < 3:
    #             flag_end = 1
    #     print(f"barline{[b.bbox]}")
    #     if flag_start and flag_end:
    #         draw_bbox([b.bbox], color=(63, 87, 181))


    # draw_bbox([b.bbox for b in barlines], color=(63, 87, 181))
    # draw_bbox([s.bbox for s in sfns if s.note_id is None], color=(90, 0, 168), labels=[str(s.label.name) for s in sfns if s.note_id is None])
    # draw_bbox([c.bbox for c in clefs], color=(235, 64, 52), labels=[c.label.name for c in clefs])
    # draw_bbox([r.bbox for r in rests], color=(12, 145, 0), labels=[r.label.name for r in rests])

    for note in notes:
        if note.invalid:
            continue
        # print("aaa.{}".format(note))
        if note.track == 0:
            position = note.staff_line_pos
            rest = position % 7
            div = int((position + 1) / 7) + 4

            if rest == 0:
                name = "D"
            elif rest == 1:
                name = "E"
            elif rest == 2:
                name = "F"
            elif rest == 3:
                name = "G"
            elif rest == 4:
                name = "A"
            elif rest == 5:
                name = "B"
            elif rest == 6:
                name = "C"
        else:
            position = note.staff_line_pos
            rest = position % 7
            div = int((position + 1)/ 7) + 2

            if rest == 0:
                name = "F"
            elif rest == 1:
                name = "G"
            elif rest == 2:
                name = "A"
            elif rest == 3:
                name = "B"
            elif rest == 4:
                name = "C"
            elif rest == 5:
                name = "D"
            elif rest == 6:
                name = "E"

        if name == "A":
            color = (128, 194, 21)
        elif name == "B":
            color = (242, 136, 15)
        elif name == "C":
            color = (9, 219, 216)
        elif name == "D":
            color = (14, 89, 230)
        elif name == "E":
            color = (150, 9, 232)
        elif name == "F":
            color = (235, 7, 87)
        elif name == "G":
            color = (235, 5, 208)

        x1, y1, x2, y2 = note.bbox
        g_x1, g_y1, g_x2, g_y2 = groups[note.note_group_id].bbox
        total_length = abs(g_y2 - g_y1)
        x_coor = int((x1 + x2) / 2)
        y_coor = int((y1 + y2) / 2)
        a_lenth = int(abs(x2 - x1) / 2)
        b_lenth = int(abs(y2 - y1) / 2)
        length = abs(y2 - y1)
        delat_length = total_length - length
        angle = -30
        if note.stem_up == None:
            continue
        # print(delat_length)
        # cv2.putText(out, name, (x_coor + 11, y_coor + 11), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 1)
        # cv2.putText(out, str(div), (x_coor + 21, y_coor), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
        if note.label.name[0] == "H":
            # print("H")
            # cv2.circle(out, (x_coor, y_coor), 12, color, 5)
            cv2.ellipse(out, (x_coor, y_coor), (a_lenth + 1, b_lenth - 4), angle, 0, 360, color, 4)
        else:
            # cv2.circle(out, (x_coor, y_coor), 12, color, -1)
            cv2.ellipse(out, (x_coor, y_coor), (a_lenth, b_lenth), angle, 0, 360, color, -1)
        if note.stem_up== True:
            cv2.line(out, (x2 - 1, y_coor + 1), (x2 - 1, g_y1), color, 2)
        else:
            cv2.line(out, (x1 + 1, y_coor - 1), (x1 + 1, g_y2), color, 2)
    return Image.fromarray(out)
