import SPDU_type_1
class SPDU:
    def __init__(self):
        self.parameter = {
            "TX_MODE": None,
            "TX_DATA_RATE": None,
            "TX_MODULATION": None,
            "TX_ENCODING": None,
            "TX_FREQUENCY": None,

            "TIME_SAMPLE": None,
            "DUPLEX": None,
            "RMND": None,
            "TOKEN": None,

            "RX_MODE": None,
            "RX_DATA_RATE": None,
            "RX_MODULATION": None,
            "RX_ENCODING": None,
            "RX_FREQUENCY": None,

            "SEQ_CTRL_FSN": None,

            "STATUS_REPORT_REQUEST": None,
            "TIME_TAG_REQUEST": None,
            "PCID0": None,
            "PCID1": None,

            "DIRECTION": None,
            "FREQUENCY_TABLE": None,
            "RATE_TABLE": None,
            "CARRIER_MODULATION": None,
            "DATA_MODULATION": None,
            "MODE_SELECT": None,
            "SCRAMBLER": None,
            "DIFF_ENCODING": None,
            "RS_CODE": None,

            "SCID": None,

            "DEMAND": None,
            "QUERY_RESPONSE": None,
            "POLARISATION": None,
            "MODULATION_INDEX": None,
            "INSTANT_SNR": None,

            "DIRECTIVE_FUNCTION": None,
            "COHERENCE": None,
            "AOS_FRAME": None
        }

    # Iterate through all the keys in the returned library and update the main library
    def update_parameter(self, dictionary):
        for key in dictionary:
            if key in self.parameter:
                self.parameter[key] = dictionary[key]

    def decode(self,type,data):
        match type:
            case 0:
                spdu = SPDU_type_1(data)
                self.update_parameter(spdu.parameter)
            case 3:



