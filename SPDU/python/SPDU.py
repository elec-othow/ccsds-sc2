from SPDU_type_1 import SPDU_TYPE_1
class SPDU:
    def __init__(self):
        self.parameter = dict

    # Iterate through all the keys in the returned library and update the main library
    def update_parameter(self, dictionary):
        for key in dictionary:
            if key in self.parameter:
                self.parameter[key] = dictionary[key]

    def decode(self,type,data):
        match type:
            case 0:
                spdu_code = SPDU_TYPE_1(data)
                self.update_parameter(spdu_code.parameter)
            case 3:



