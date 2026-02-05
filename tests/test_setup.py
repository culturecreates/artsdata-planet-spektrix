import unittest


class TestServices(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n[SetupClass] Initializing test resources")

    @classmethod
    def tearDownClass(cls):
        print("\n[TearDownClass] Cleaning up test resources")

    def setUp(self):
        self.events_data = [
            {
                "description": "Tickets sold by ATP",
                "htmlDescription": "<div id=\"test-id\">\r\n\r\n</div>",
                "duration": 0,
                "imageUrl": "",
                "isOnSale": False,
                "name": "Sample Test Event 1",
                "instanceDates": "9 August-10 August",
                "thumbnailUrl": "",
                "webEventId": None,
                "id": "34001AGQQHTLTHTMBJQGPRQRMLLBGHNMV",
                "firstInstanceDateTime": "2024-08-09T19:30:00",
                "lastInstanceDateTime": "2024-08-10T14:00:00",
                "altText": "",
            },
            {
                "description": "2024-25 Season, Feb 25 - 16 Mar, 2025, Slot 5",
                "htmlDescription": "<div id=\"test-id\">\r\n\r\n</div>",
                "duration": 120,
                "imageUrl": "",
                "isOnSale": True,
                "name": "Sample Test Event 12",
                "instanceDates": "25 February-16 March",
                "thumbnailUrl": "",
                "webEventId": None,
                "id": "32801AVMKCMLRNPSSSQQTHRKHHMLJSPPT",
                "firstInstanceDateTime": "2025-02-25T19:30:00",
                "lastInstanceDateTime": "2025-03-16T14:00:00",
                "altText": "",
            },
        ]

        self.mock_venues = [
            {
                "name": "Sample Venue",
                "address": "215 8 Ave SE, Calgary, AB T2G 0K8",
                "id": "201AGBHDRLQHNHPHKKMPKLGPMDRDTDMVL",
            },
            {
                "name": "Unknown",
                "address": "Unknown",
                "id": "401ANPJQJQPQMRSBDNMVNLSPGTRBVQVRH",
            },
            {
                "name": "Sample Online Venue",
                "address": "Online",
                "id": "801ARDQDDMGGJKKRTNTJBMCCMMBCPQKCR",
            },
        ]

        self.mock_instances = [
            {
                "isOnSale": False,
                "planId": "6428ARVBDCVGBMTSRKLDHCQHSPQJQNLSH",
                "priceList": {"id": "122001ARLLQVMHNRLSMQCVBKMJQMVCKHB"},
                "event": {"id": "34001AGQQHTLTHTMBJQGPRQRMLLBGHNMV"},
                "start": "2024-08-09T19:30:00",
                "startUtc": "2024-08-10T01:30:00",
                "startSellingAtWeb": "2024-07-09T13:11:00",
                "startSellingAtWebUtc": "2024-07-09T19:11:00Z",
                "stopSellingAtWeb": "2024-08-09T17:30:00",
                "stopSellingAtWebUtc": "2024-08-09T23:30:00Z",
                "webInstanceId": "backyardbash-24-fri",
                "cancelled": False,
                "id": "67201AVCRKQDBSGLQHRCLJQTBDLCTLNNQ",
                "hasBestAvailableOverlay": False,
                "attribute_MoreInfoTitle": "",
                "attribute_MoreInfoContent": "",
                "attribute_ButtonDisabled": "",
            },
            {
                "isOnSale": False,
                "planId": "6428ARVBDCVGBMTSRKLDHCQHSPQJQNLSH",
                "priceList": {"id": "122001ARLLQVMHNRLSMQCVBKMJQMVCKHB"},
                "event": {"id": "32801AVMKCMLRNPSSSQQTHRKHHMLJSPPT"},
                "start": "2024-08-10T14:00:00",
                "startUtc": "2024-08-10T20:00:00",
                "startSellingAtWeb": "2024-07-09T13:11:00",
                "startSellingAtWebUtc": "2024-07-09T19:11:00Z",
                "stopSellingAtWeb": "2024-08-10T12:00:00",
                "stopSellingAtWebUtc": "2024-08-10T18:00:00Z",
                "webInstanceId": "backyardbash-24-satm",
                "cancelled": False,
                "id": "67401ALTRTTRTPTSQHLNNDTGHMDRBCNBR",
                "hasBestAvailableOverlay": False,
                "attribute_MoreInfoTitle": "",
                "attribute_MoreInfoContent": "",
                "attribute_ButtonDisabled": "",
            }
        ]

        self.mock_plans = [
            {
                "id": "53586",
                "name": "A16",
                "row": "A",
                "number": 16,
                "previousSeatId": 53585,
                "previousIsAcrossAisle": False,
                "nextIsAcrossAisle": False,
                "nextSeatId": 53587,
                "x": 432,
                "y": 454,
                "tabOrder": None,
            },
            {
                "id": "53589",
                "name": "A19",
                "row": "A",
                "number": 19,
                "previousSeatId": 53588,
                "previousIsAcrossAisle": False,
                "nextIsAcrossAisle": False,
                "nextSeatId": 53590,
                "x": 484,
                "y": 419,
                "tabOrder": None,
            },
            {
                "type": "Reserved",
                "name": "Tier 2 Right",
                "venue": {"id": "201AGBHDRLQHNHPHKKMPKLGPMDRDTDMVL"},
                "backgroundImageUrl": "",
                "x": 0,
                "y": 0,
                "areas": [],
                "seats": [
                    {
                        "id": "53613",
                        "name": "A1",
                        "row": "A",
                        "number": 1,
                        "previousSeatId": None,
                        "previousIsAcrossAisle": False,
                        "nextIsAcrossAisle": False,
                        "nextSeatId": 53614,
                        "x": 582,
                        "y": 80,
                        "tabOrder": None,
                    },
                    {
                        "id": "53614",
                        "name": "A2",
                        "row": "A",
                        "number": 2,
                        "previousSeatId": 53613,
                        "previousIsAcrossAisle": False,
                        "nextIsAcrossAisle": False,
                        "nextSeatId": 53615,
                        "x": 567,
                        "y": 95,
                        "tabOrder": None,
                    },
                ],
                "capacity": 13,
                "maxZoomWeb": None,
                "maxZoomMobile": None,
                "id": "6241ANKHKHPTGTLHVJKRTBCBRDBNQPKQD",
            },
            {
                "type": "Unreserved",
                "name": "Backyard TBA in Mount Royal, Calgary",
                "venue": {"id": "401ANPJQJQPQMRSBDNMVNLSPGTRBVQVRH"},
                "backgroundImageUrl": "",
                "x": 0,
                "y": 0,
                "areas": [],
                "seats": None,
                "capacity": 100,
                "maxZoomWeb": None,
                "maxZoomMobile": None,
                "id": "6428ARVBDCVGBMTSRKLDHCQHSPQJQNLSH",
            },
            {
                "type": "Unreserved",
                "name": "Martha Cohen Theatre",
                "venue": {"id": "201AGBHDRLQHNHPHKKMPKLGPMDRDTDMVL"},
                "backgroundImageUrl": "",
                "x": 0,
                "y": 0,
                "areas": [],
                "seats": None,
                "capacity": 419,
                "maxZoomWeb": None,
                "maxZoomMobile": None,
                "id": "6628AHDQNSKCGQHSDLJLJDDGPPKHGQJRC",
            },
            {
                "type": "Unreserved",
                "name": "Fundraising Events",
                "venue": {"id": "801ARDQDDMGGJKKRTNTJBMCCMMBCPQKCR"},
                "backgroundImageUrl": "",
                "x": 0,
                "y": 0,
                "areas": [],
                "seats": None,
                "capacity": 403,
                "maxZoomWeb": None,
                "maxZoomMobile": None,
                "id": "6828ACGTJRJDRLQDHKDKHJCBTRBNVSKPS",
            },
        ]
        print("\n[Setup] Preparing test case")

    def tearDown(self):
        """
        Runs AFTER each test
        """
        print("\n[TearDown] Resetting test case")