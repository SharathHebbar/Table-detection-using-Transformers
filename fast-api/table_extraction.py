from ultralyticsplus import YOLO, render_result
from pathlib import Path, PurePath

class Table_extraction():
    
    def __init__(self, image, OUTPUTS_DIR):
        self.model = YOLO('keremberke/yolov8m-table-extraction')
        self.model.overrides['conf'] = 0.25
        self.model.overrides['iou'] = 0.45
        self.model.overrides['agnostic_nms'] = False 
        self.model.overrides['max_det'] = 1000
        self.image = image
        self.OUTPUTS_DIR = OUTPUTS_DIR

    
    def get_results(self):
        self.results = self.model(self.image)
        render = render_result(model=self.model, image=self.image, result=self.results[0])
        op_img = self.OUTPUTS_DIR + Path(self.image).name
        render.save(op_img)
        return op_img

    # def recognize_coords(self):
    #     final_results = []
    #     result = str(self.results)
    #     print(result)
    #     result = result.split('(')
    #     print('Result', result)
    #     if '\n' not in result[1]:
    #         print('In if')
    #         coords = []
    #         result = result[1][2: -3].split(',')
    #         for i in result:
    #             coords.append(float(i))
    #         final_results.append(coords)
    #         return final_results
    #     else:
    #         result = result[1:][0]
    #         result = result.split('\n')
    #         j = 0
    #         print('Results: ', result)
    #         for i in result:
    #             coords = []
    #             i = i.strip()
    #             if j == 0:
    #                 print(i)
    #                 i = i[2:-2]
    #                 print(i)
    #             elif j == len(result) - 1:
    #                 i = i[1:-3]
    #             else:
    #                 i = i[1:-2]
    #             j+=1
    #             print(i)
    #             i = i.split(',')
    #             print(i)
    #             for k in i:
    #                 coords.append(float(k))
    #             final_results.append(coords)
    #     return final_results
    

# te = Table_extraction('junks\9.png', 'outputs/123')
# te.get_results()
# print(te.recognize_coords())  