# Directives/Reports for UHF operations
import json
class SPDU_TYPE_2:
    def __init__(self,data):
        ##zfill to ensure in the format of 16 bits
        self.data = bin(data).replace("0b","").zfill(16) ## Remove the "0b" from binary string
        self.directive = data[0:8]
        self.parameter = {
            "TRANSCEIVER_CLOCK_ROUGH": None,

            "SEND_SIDE_DELAY": None,
            "ONE_WAY_LIGHT_TIME": None
        }

    def decode(self):
        with open("SPDU.json","r") as file:
            table = json.load(file)
        # No key in .json file for the TIME_SAMPLE
        for key in self.parameter:
            try:
                ##TX and RX data rate since it has different format than the rest(extra field for data rate table)
                if key == "TX_FREQUENCY" or key == "RX_FREQUENCY":
                    self.parameter[key] = table["SPDU2"][key][self.freq_table][self.parameter[key]]
                elif key == "TX_DATA_RATE" or key == "RX_DATA_RATE":
                    self.parameter[key] = table["SPDU2"][key][self.rate_table][self.parameter[key]]
                else:
                    self.parameter[key] = table["SPDU2"][key][self.parameter[key]]
            except KeyError:
                pass

    def select(self):
        match self.directive:
            ## Data rates depend on encoding
            case "00000000":
                for key in self.parameter:
                    self.parameter[key] = "NULL"
            case "00000001":
                self.parameter = {
                    "TOKEN": self.data[12],
                    "RMND": self.data[11],
                    "DUPLEX": self.data[6:8],
                    "TIME_SAMPLE": int(self.data[0:5],2)
                }

        self.decode()