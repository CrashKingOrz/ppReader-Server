import numpy as np
import cv2
import jieba

from kernel.model.baidu_pp_ocr.tools.infer import utility
from kernel.model.baidu_pp_detection.python.infer import Config, Detector
from kernel.model.baidu_pp_detection.python.visualize import visualize_box_mask, lmk2out
from kernel.model.baidu_pp_ocr.tools.infer.predict_system import TextSystem
from kernel.model.baidu_pp_ocr.ppocr.utils.logging import get_logger

logger = get_logger()


class PpDetection:
    # Object recognition
    def __init__(self, device="GPU"):
        """
        Initialize detection models.

        """
        self.model_dir = './kernel/model/baidu_pp_detection/models/cascade_rcnn_dcn_r101_vd_fpn_gen_server_side'
        config = Config(self.model_dir)
        self.labels_en = config.labels
        self.labels_zh = self.get_label_zh()
        self.ob_detector = Detector(
            config,
            self.model_dir,
            device=device,
            run_mode='fluid',
            trt_calib_mode=False)

        # Warm up detection model
        if 1:
            print('Warm up detection model')
            img = np.random.uniform(0, 255, [640, 640, 3]).astype(np.uint8)
            for i in range(3):
                im, results = self.detect_image(img)

    def get_label_zh(self):
        """
        Obtain the corresponding Chinese label.

        @return back_list: Chinese label list
        """
        file_path = self.model_dir + '/generic_det_label_list_zh.txt'
        back_list = []
        with open(file_path, 'r', encoding='utf-8') as label_text:
            for label in label_text.readlines():
                back_list.append(label.replace('\n', ''))
        return back_list

    def detect_image(self, img):
        """
        Detect the image.

        @param img: Represents the three-dimensional matrix of the image
        @return im: Represents the three-dimensional matrix of the image with boxes and label
        @return results: the label of img

        """
        results = self.ob_detector.predict(img, 0.5)
        im = visualize_box_mask(
            img,
            results,
            self.ob_detector.config.labels,
            mask_resolution=self.ob_detector.config.mask_resolution,
            threshold=0.5)
        im = np.array(im)
        return im, results

    def point_detect_image(self, img, index_finger_tip_coordinates=np.array([0, 0])):
        """
        Detect the image according to the point.
        """

        def calculate_relative_distance(point, pt1, pt2):
            pt1_x = pt1[0]
            pt1_y = pt1[1]
            pt2_x = pt2[0]
            pt2_y = pt2[1]
            p_x = point[0]
            p_y = point[1]

            if p_x < pt1_x and p_y < pt1_y:
                distance = max(abs(pt1_x - p_x), abs(pt1_y - p_y))
            elif pt1_x <= p_x <= pt2_x and p_y <= pt1_y:
                distance = abs(pt1_y - p_y)
            elif p_x > pt2_x and p_y < pt1_y:
                distance = max(abs(p_x - pt1_x), abs(pt1_y - p_y))
            elif pt1_y <= p_y <= pt2_y and p_x < pt1_x:
                distance = abs(pt1_x - p_x)
            elif pt1_y <= p_y <= pt2_y and pt1_x <= p_x <= pt2_x:
                distance = min(abs(p_y - pt1_y), abs(pt2_y - p_y), abs(p_x - pt1_x), abs(pt2_x - p_x))
            elif pt1_y <= p_y <= pt2_y and p_x > pt2_x:
                distance = abs(p_x - pt2_x)
            elif pt2_y < p_y and p_x < pt1_x:
                distance = max(abs(pt1_x - p_x), abs(pt1_y - p_y))
            elif pt1_y <= p_y and pt1_x <= p_x <= pt2_x:
                distance = abs(p_y - pt2_y)
            else:
                # pt1_y < p_y and pt2_x < p_x
                distance = max(abs(p_x - pt2_x), abs(p_y - pt2_y))

            return distance

        results = self.ob_detector.predict(img, 0.5)

        im = visualize_box_mask(
            img,
            results,
            self.ob_detector.config.labels,
            mask_resolution=self.ob_detector.config.mask_resolution,
            threshold=0.5)
        im = np.array(im)

        min_distance = 10000
        if len(results['boxes']) > 0:
            for i in range(len(results['boxes'])):
                bbox = results['boxes'][i][2:].astype(int)
                xmin, ymin, xmax, ymax = bbox

                distance = calculate_relative_distance(index_finger_tip_coordinates, np.array([xmin, ymin]), np.array([xmax, ymax]))

                if min_distance > distance:
                    min_distance = distance
                    label_id = results['boxes'][i][0].astype(int)
                    label_en = self.labels_en[label_id]
                    label_zh = self.labels_zh[label_id - 1]
                    detect_res = [label_zh, label_en]
        else:
            detect_res = ['无', 'None']

        # cv2.imshow("detect_img", im)
        # cv2.waitKey(0)

        return im, detect_res, min_distance


class PpOCR:
    # OCR
    def __init__(self, device='GPU'):
        """
        Initialize ocr model.

        """
        args = utility.parse_args()
        args.det_model_dir = "./kernel/model/baidu_pp_ocr/models/ch_PP-OCRv2_det_infer/"
        args.rec_model_dir = "./kernel/model/baidu_pp_ocr/models/ch_PP-OCRv2_rec_infer/"
        args.rec_char_dict_path = "./kernel/model/baidu_pp_ocr/ppocr/utils/ppocr_keys_v1.txt"
        args.use_angle_cls = False
        self.text_sys = TextSystem(args)

        # gpu or cpu
        if device == "GPU":
            args.use_gpu = True
        elif device == "CPU":
            args.use_gpu = False
        else:
            logger.error("Error: device should be GPU or CPU!")

        # Warm up ocr model
        if 1:
            print('Warm up ocr model')
            img = np.random.uniform(0, 255, [640, 640, 3]).astype(np.uint8)
            for i in range(10):
                res = self.text_sys(img)

    def ocr_image(self, img):
        """
        Read image text.

        @param img: Represents the three-dimensional matrix of the image
        @return src_im:  Represents the three-dimensional matrix of the image with boxes and textlabel
        @return text_list:  the textlabel of img
        """
        dt_boxes, rec_res = self.text_sys(img)
        text_list = []
        for text, score in rec_res:
            text_list.append(text)

        src_im = img

        ocr_area = 0
        for box in dt_boxes:
            box = np.array(box).astype(np.int32).reshape(-1, 2)
            cv2.polylines(src_im, [box], True, color=(255, 255, 0), thickness=2)

            ocr_area += abs(box[2][0] - box[0][0]) * abs(box[2][1] - box[0][1])

        return src_im, text_list, ocr_area

    def point_ocr_image(self, img, index_finger_tip_coordinates=np.array([0, 0]), flag='word'):
        """
        Recognize one character, word or one sentence.

        @param img: Represents the three-dimensional matrix of the image
        @return src_im:  Represents the three-dimensional matrix of the image with boxes and textlabel
        @return text_list:  the textlabel of img
        """
        def point_line_distance(point, line_point1, line_point2):
            # 计算向量
            vec1 = line_point1 - point
            vec2 = line_point2 - point
            distance = np.abs(np.cross(vec1, vec2)) / np.linalg.norm(line_point1 - line_point2)
            return distance

        def get_single_character_average_length(box, words_num):
            row_length = box[2][0] - box[3][0]
            single_character_average_length = row_length / words_num
            return single_character_average_length

        min_distance = 10000

        dt_boxes, rec_res = self.text_sys(img)
        text_list = []
        for text, score in rec_res:
            text_list.append(text)

        left_top_x = left_top_y = right_bottom_x = right_bottom_y = 0

        image = img
        text_result = []

        if len(text_list):
            d_list = []
            text_result = []
            for box in dt_boxes:
                d1 = point_line_distance(index_finger_tip_coordinates, box[2], box[3])
                if box[3][0] <= index_finger_tip_coordinates[0] <= box[2][0] and \
                        (index_finger_tip_coordinates[1] > box[0][1] or index_finger_tip_coordinates[1] > box[1][1]):
                    d2 = 0
                else:
                    d2 = 10000
                d_list.append(d1 + d2)

            d_list = np.array(d_list)
            row_index = np.argmin(d_list)
            min_distance = d_list[row_index]

            if flag == 'character':
                single_character_length = get_single_character_average_length(dt_boxes[row_index], len(text_list[row_index]))
                character_index = int(
                    (index_finger_tip_coordinates[0] - dt_boxes[row_index][3][0]) / single_character_length) - 1
                if character_index < 0:
                    character_index = 0
                if character_index >= len(text_list[row_index]):
                    character_index = len(text_list[row_index]) - 1
                text_result = text_list[row_index][character_index]

                left_top_x = dt_boxes[row_index][0][0] + character_index * single_character_length
                left_top_y = dt_boxes[row_index][0][1]
                right_bottom_x = dt_boxes[row_index][2][0] + (character_index + 1) * single_character_length
                right_bottom_y = dt_boxes[row_index][2][1]

            elif flag == 'word':
                sentence = text_list[row_index]
                words = jieba.lcut(sentence)
                # print(words)

                single_character_length = get_single_character_average_length(dt_boxes[row_index], len(text_list[row_index]))
                total_length = dt_boxes[row_index][3][0]
                for word in words:
                    total_length += len(word)*single_character_length
                    if total_length >= index_finger_tip_coordinates[0]:
                        text_result.append(word)

                        left_top_x = dt_boxes[row_index][0][0] + total_length - single_character_length * len(word)
                        left_top_y = dt_boxes[row_index][0][1]
                        right_bottom_x = dt_boxes[row_index][2][0] + total_length
                        right_bottom_y = dt_boxes[row_index][2][1]

                        break

            elif flag == 'sentence':
                if '.' in text_list[row_index]:
                    index = text_list[row_index].find('.')
                    text_result.insert(0, text_list[row_index][:index + 1])
                elif '。' in text_list[row_index]:
                    index = text_list[row_index].find('。')
                    text_result.insert(0, text_list[row_index][:index + 1])
                else:
                    text_result.insert(0, text_list[row_index])

                box = np.array(dt_boxes[row_index]).astype(np.int32).reshape(-1, 2)
                cv2.polylines(image, [box], True, color=(255, 255, 0), thickness=2)
                row_index -= 1
                end_count = 1

                while row_index >= 0:
                    if '.' not in text_list[row_index] and '。' not in text_list[row_index]:
                        text_result.insert(0, text_list[row_index])

                        box = np.array(dt_boxes[row_index]).astype(np.int32).reshape(-1, 2)
                        cv2.polylines(image, [box], True, color=(255, 255, 0), thickness=2)

                        row_index -= 1
                        end_count += 1

                        if end_count > 3:  # 往前搜索3段，若未找到’。‘或’.‘则终止，输出这4段结果
                            break

                    else:
                        before_index = -1
                        if '.' in text_list[row_index]:
                            before_index = text_list[row_index].rfind('.')
                        if '。' in text_list[row_index]:
                            before_index = text_list[row_index].rfind('。')
                        text_result.insert(0, text_list[row_index][before_index + 1:])
                        box = np.array(dt_boxes[row_index]).astype(np.int32).reshape(-1, 2)
                        cv2.polylines(image, [box], True, color=(255, 255, 0), thickness=2)
                        break

                left_top_x = dt_boxes[row_index + 1][0][0]
                left_top_y = dt_boxes[row_index + 1][0][1]
                right_bottom_x = dt_boxes[row_index + end_count][2][0]
                right_bottom_y = dt_boxes[row_index + end_count][2][1]

            else:
                print("ERROR: Do not support this kind of text!")
                raise NotImplementedError

            left_top_x = int(max(left_top_x - 2, 0))
            left_top_y = int(max(left_top_y - 2, 0))
            right_bottom_x = int(min(right_bottom_x + 2, image.shape[1]))
            right_bottom_y = int(min(right_bottom_y + 2, image.shape[0]))

            # image = img[left_top_y:right_bottom_y, left_top_x:right_bottom_x, :]
            image = cv2.rectangle(image, (left_top_x, left_top_y), (right_bottom_x, right_bottom_y),
                                  (0, 255, 0), 2)
            # cv2.imshow("image_ocr", image)
            # cv2.waitKey(0)
            # print(text_result)

        return image, text_result, min_distance

