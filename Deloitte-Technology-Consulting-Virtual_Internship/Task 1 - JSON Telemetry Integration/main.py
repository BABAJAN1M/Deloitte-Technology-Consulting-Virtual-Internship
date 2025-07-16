import json, unittest
from datetime import datetime

# Load the files
with open("./data-1.json", "r") as f:
    jsonData1 = json.load(f)
with open("./data-2.json", "r") as f:
    jsonData2 = json.load(f)
with open("./data-result.json", "r") as f:
    jsonExpectedResult = json.load(f)


def convert_iso_to_millis(ts):
    ts = ts.replace("Z", "+00:00")
    try:
        dt = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S.%f%z")
    except ValueError:
        dt = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S%z")
    return int(dt.timestamp() * 1000)


def convertFromFormat1(obj):
    # Spliting location string
    parts = obj["location"].split("/")
    return {
        "deviceID": obj["deviceID"],
        "deviceType": obj["deviceType"],
        "timestamp": obj["timestamp"],
        "data": {
            "status": obj["operationStatus"],
            "temperature": obj["temp"]
        },
        "location": {
            "country": parts[0],
            "city": parts[1],
            "area": parts[2],
            "factory": parts[3],
            "section": parts[4]
        }
    }


def convertFromFormat2(obj):
    return {
        "deviceID": obj["device"]["id"],
        "deviceType": obj["device"]["type"],
        "timestamp": convert_iso_to_millis(obj["timestamp"]),
        "data": {
            "status": obj["data"]["status"],
            "temperature": obj["data"]["temperature"]
        },
        "location": {
            "country": obj["country"],
            "city": obj["city"],
            "area": obj["area"],
            "factory": obj["factory"],
            "section": obj["section"]
        }
    }


def main(obj):
    if "device" not in obj:
        return convertFromFormat1(obj)
    else:
        return convertFromFormat2(obj)


class TestSolution(unittest.TestCase):

    def test_sanity(self):
        result = json.loads(json.dumps(jsonExpectedResult))
        self.assertEqual(result, jsonExpectedResult)

    def test_dataType1(self):
        result = main(jsonData1)
        self.assertEqual(result, jsonExpectedResult,
                         'Converting from Type 1 failed')

    def test_dataType2(self):
        result = main(jsonData2)
        self.assertEqual(result, jsonExpectedResult,
                         'Converting from Type 2 failed')


if __name__ == '__main__':
    unittest.main()
