# Directives/Reports for UHF operations
import json
class SPDU_TYPE_1:
    def __init__(self,data):
        ##zfill to ensure in the format of 16 bits
        self.data = bin(data).replace("0b","").zfill(16) ## Remove the "0b" from binary string
        self.directive = data[13:15]
        self.parameter = dict()
        ##Would change rx and tx data rate
        self.rate_table = 0
        self.freq_table = 0
        self.select()

    def decode(self):
        with open("SPDU.json","r") as file:
            table = json.load(file)
        # No key in .json file for the TIME_SAMPLE
        for key in self.parameter:
            try:
                ##TX and RX data rate since it has different format than the rest(extra field for data rate table)
                if key == "TX_FREQUENCY" or key == "RX_FREQUENCY":
                    self.parameter[key] = table["SPDU1"][key][self.freq_table][self.parameter[key]]
                elif key == "TX_DATA_RATE" or key == "RX_DATA_RATE":
                    self.parameter[key] = table["SPDU1"][key][self.rate_table][self.parameter[key]]
                else:
                    self.parameter[key] = table["SPDU1"][key][self.parameter[key]]
            except KeyError:
                pass

    def select(self):
        match self.directive:
            ## Data rates depend on encoding
            case "000":
                self.parameter = {
                    "TX_FREQUENCY":  self.data[10:12],
                    "TX_ENCODING":self.data[8:9],
                    "TX_MODULATION": self.data[7],
                    "TX_DATA_RATE": self.data[3:6],
                    "TX_MODE":self.data[0:2]
                }
            case "001":
                self.parameter = {
                    "TOKEN": self.data[12],
                    "RMND": self.data[11],
                    "DUPLEX": self.data[6:8],
                    "TIME_SAMPLE": int(self.data[0:5],2)
                }
            case "010":
                self.parameter = {
                    "RX_FREQUENCY":  self.data[10:12],
                    "RX_ENCODING":self.data[8:9],
                    "RX_MODULATION": self.data[7],
                    "RX_DATA_RATE": self.data[3:6],
                    "RX_MODE":self.data[0:2]
                }
            case "011":
                self.parameter = {
                    "SEQ_CTRL_FSN": int(self.data[0:7], 2)
                }
            case "100":
                self.parameter = {
                    "PCID1": self.data[12],
                    "PCID0": self.data[11],
                    ## Documentation: Proximity-1 Space Link Protocol—Data Link Layer
                    ## Indicate frame number
                    "TIME_TAG_REQUEST": int(self.data[8:10],2),
                    "STATUS_REPORT_REQUEST": self.data[3:7]
                    ## Spares should be "00"
                }
            case "110":
                self.freq_table = self.data[1]
                self.rate_table = self.data[2]
                self.parameter = {
                    "DIRECTION": self.data[0],
                    "CARRIER_MODULATION": self.data[3:4],
                    "DATA_MODULATION": self.data[5:6],
                    "MODE_SELECT": self.data[7:8],
                    "SCRAMBLER": self.data[9:10],
                    "DIFF_ENCODING": self.data[11],
                    "RS_CODE": self.data[12]
                }
            case "111":
                self.parameter = {
                    "SCID": int(self.data[0:9], 2)
                    ## Reserved bits should be "000"
                }
        self.decode()