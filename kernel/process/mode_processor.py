import numpy as np

from kernel.model.baidu_pp_wrapper import PpDetection, PpOCR


class ModeProcessor:
    def __init__(self, device="GPU"):
        self.text_result = []

        # import the OCR class
        self.pp_ocr = PpOCR(device=device)

        # import the detection class
        self.pp_dete = PpDetection(device=device)

        # last results
        self.last_detect_res = {'detection': ['无', 'None'], 'ocr': '无'}

        self.button2content = {0: 'character', 1: 'word', 2: 'sentence', 3: 'object', 4: 'general'}

    def point_mode(self, finger_cord, frame, content_class):
        if content_class in ['character', 'word', 'sentence']:
            image, ocr_result, ocr_min_distance = self.pp_ocr.point_ocr_image(frame, finger_cord, flag=content_class)
            if len(ocr_result) > 0:
                ocr_result = ' '.join(ocr_result)

            else:
                # No result
                ocr_result = '无'

            self.text_result = ocr_result
            return ocr_result

        elif content_class == 'object':
            image, detection_result, detection_min_distance = self.pp_dete.point_detect_image(frame, finger_cord)
            detection_result = detection_result[0]
            self.text_result = detection_result
            return detection_result

        else:
            print("Warning: the choose mode may not match to the gesture, "
                  "suggest using button '0-3' for pointing")
            text_result = '无'

            image, ocr_result, ocr_min_distance = self.pp_ocr.point_ocr_image(frame, finger_cord, flag='word')
            # print("ocr:", ocr_result, ocr_min_distance)
            image, detection_result, detection_min_distance = self.pp_dete.point_detect_image(frame, finger_cord)
            # print("detection:", detection_min_distance)
            if len(ocr_result) or detection_result != ['无', 'None']:
                if ocr_min_distance <= detection_min_distance:
                    text_result = ocr_result
                else:
                    text_result = detection_result
                    text_result = text_result[0]

            self.text_result = text_result
            return text_result

    def box_mode(self, pt1, pt2, frame, content_class):
        if (pt1 == np.array([-1, -1])).all() and (pt2 == np.array([-1, -1])).all():
            raw_img = frame
        else:
            # Pass thumbnail
            y_min = min(pt1[1], pt2[1])
            y_max = max(pt1[1], pt2[1])

            x_min = min(pt1[0], pt2[0])
            x_max = max(pt1[0], pt2[0])

            raw_img = frame[y_min:y_max, x_min:x_max, ]

        if content_class == 'object':
            im, results = self.pp_dete.detect_image(raw_img)
            # Take the first identified object
            if len(results['boxes']) > 0:
                label_id = results['boxes'][0][0].astype(int)
                label_en = self.pp_dete.labels_en[label_id]
                label_zh = self.pp_dete.labels_zh[label_id - 1]
                detect_res = [label_zh, label_en]
                detect_res = detect_res[0]
                # print("detection: ", label_zh + label_en)

            else:
                detect_res = ['无', 'None']
                detect_res = detect_res[0]

            self.text_result = detect_res
            return detect_res

        elif content_class in ['character', 'word', 'sentence']:
            src_im, text_list, ocr_area = self.pp_ocr.ocr_image(raw_img)

            if len(text_list) > 0:
                ocr_text = ' '.join(text_list)
                # record
                # print("ocr:", ocr_text)

            else:
                # No res
                ocr_text = '无'

            self.text_result = ocr_text
            return ocr_text

        else:
            print("Warning: the choosen mode may not match to the gesture, "
                  "suggest using button '0-3' for drawing box")

            im, results = self.pp_dete.detect_image(raw_img)
            src_im, text_list, ocr_area = self.pp_ocr.ocr_image(raw_img)
            if len(results['boxes']) > 0 and len(text_list) > 0:
                print(results['boxes'][0])
                bbox = results['boxes'][0][2:]
                xmin, ymin, xmax, ymax = bbox
                w = xmax - xmin
                h = ymax - ymin
                object_area = w * h
                if (object_area > ocr_area):
                    label_id = results['boxes'][0][0].astype(int)
                    label_en = self.pp_dete.labels_en[label_id]
                    label_zh = self.pp_dete.labels_zh[label_id - 1]
                    text_result = [label_zh, label_en]
                    text_result = text_result[0]
                else:
                    text_result = ' '.join(text_list)

            elif len(results['boxes']) > 0 and len(text_list) <= 0:
                label_id = results['boxes'][0][0].astype(int)
                label_en = self.pp_dete.labels_en[label_id]
                label_zh = self.pp_dete.labels_zh[label_id - 1]
                text_result = [label_zh, label_en]
                text_result = text_result[0]

            elif len(results['boxes']) <= 0 and len(text_list) > 0:
                text_result = ' '.join(text_list)

            else:
                text_result = '无'

        self.text_result = text_result
        return text_result

    def mode_execute(self, button: int = 0, frame: np.ndarray = None, finger_coord1: np.ndarray = np.array([-1, -1]),
                     finger_coord2: np.ndarray = np.array([-1, -1])):
        """
        Execute recognition according to the button mode.

        @param button: 0: 'character'识字, 1: 'word'识词, 2: 'sentence'识句, 3: 'object'识物,
                        4: 'general'通用（自主确定识别内容,目前点读只支持识别'词'或'物'）
        @param frame: the original frame
        @param finger_coord1: one index finger tip coordinates
        @param finger_coord2: another index finger tip coordinates
        @return: recognized results (no result: '无' or ['无', 'None'])
        """

        if not (finger_coord1 == np.array([-1, -1])).all() and not (finger_coord2 == np.array([-1, -1])).all():
            text_results = self.box_mode(finger_coord1, finger_coord2, frame, self.button2content[button])
        elif not (finger_coord1 == np.array([-1, -1])).all():
            text_results = self.point_mode(finger_coord1, frame, self.button2content[button])
        elif not (finger_coord2 == np.array([-1, -1])).all():
            text_results = self.point_mode(finger_coord2, frame, self.button2content[button])
        else:
            text_results = self.box_mode(finger_coord1, finger_coord2, frame, self.button2content[button])

        return text_results

    def get_detection_label(self):
        return self.last_detect_res['detection']

    def get_ocr_text(self):
        return self.last_detect_res['ocr']

    def get_text_result(self):
        return self.text_result

