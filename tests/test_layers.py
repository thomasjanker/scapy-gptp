import unittest
from scapy.compat import raw

from gptp.layers import PTPv2


SYNC_MESSAGE_TRACE = [
    0x10,                                           # transport specific + message type
    0xA2,                                           # reserved(0) + PTP version
    0x00, 0x2C,                                     # message length
    0x00,                                           # domain number
    0x42,                                           # reserved(1)
    0x02, 0x08,                                     # flags
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, # correction field
    0x12, 0x34, 0x56, 0x78,                         # reserved(2)
    0x66, 0x55, 0x44, 0xFF, 0xFE, 0x33, 0x22, 0x11, 0x00, 0x01, # source port id
    0x01, 0xD4,                                                 # sequence id
    0x00,                                                       # control
    0xFE,                                                       # logMessageInterval
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, # reserved
]

FOLLOW_UP_MESSAGE_TRACE = [
    0x18,                                           # transport specific + message type
    0x02,                                           # reserved(0) + PTP version
    0x00, 0x4C,                                     # message length
    0x00,                                           # domain number
    0x00,                                           # reserved(1)
    0x00, 0x08,                                     # flags
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, # correction field
    0x00, 0x00, 0x00, 0x00,                         # reserved(2)
    0x66, 0x55, 0x44, 0xFF, 0xFE, 0x33, 0x22, 0x11, 0x00, 0x01, # source port id
    0x01, 0xD4,                                                 # sequence id
    0x02,                                                       # control
    0xFE,                                                       # logMessagePeriod
    0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x02, # preciseOriginTimestamp
    0x00, 0x03,                                                 # tlvType
    0x00, 0x1C,                                                 # lengthField
    0x00, 0x80, 0xC2,                                           # organizationId
    0x00, 0x00, 0x01,                                           # organizationSubType
    0x00, 0x00, 0x00, 0x00,                                     # cummulativeRateOffset
    0x00, 0x00,                                                 # gmTimeBaseIndicator
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,                         # lastGmPhasechange
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,                         # lastGmPhaseChange
    0x00, 0x00, 0x00, 0x00,                                     # scaled lastGmPhaseChange
]

PDELAY_REQ_MESSAGE_TRACE = [
    0x12,                                           # transport specific + message id
    0x02,                                           # reserved(0) + PTP version
    0x00, 0x36,                                     # message length
    0x00,                                           # domain number
    0x00,                                           # reserved(1)
    0x00, 0x08,                                     # flags
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, # correction field
    0x00, 0x00, 0x00, 0x00,                         # reserved(2)
    0x66, 0x55, 0x44, 0xff, 0xfe, 0x33, 0x22, 0x12, 0x00, 0x01, # source port id
    0x01, 0xD4,                                                 # sequence id
    0x05,                                                       # control
    0xFE,                                                       # logMessageInterval
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, # reserved
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, # reserved
]

PDELAY_RESP_MESSAGE_TRACE = [
    0x13,                                           # transport specific + message id
    0x02,                                           # reserved(0) + PTP version
    0x00, 0x36,                                     # message length
    0x00,                                           # domain number
    0x00,                                           # reserved(1)
    0x02, 0x08,                                     # flags
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, # correction field
    0x00, 0x00, 0x00, 0x00,                         # reserved(2)
    0x66, 0x55, 0x44, 0xff, 0xfe, 0x33, 0x22, 0x11, 0x00, 0x01, # source port id
    0x01, 0xD4,                                                 # sequence id
    0x05,                                                       # control
    0x7f,                                                       # logMessageInterval
    0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x02, # requestReceiptTimestamp
    0x66, 0x55, 0x44, 0xff, 0xfe, 0x33, 0x22, 0x12, 0x00, 0x01  # requestingPortIdentity
]

PDELAY_RESP_FOLLOW_UP_MESSAGE_TRACE = [
    0x1a,                                           # transport specific + message id
    0x02,                                           # reserved(0) + PTP version
    0x00, 0x36,                                     # message length
    0x00,                                           # domain number
    0x00,                                           # reserved(1)
    0x00, 0x08,                                     # flags
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, # correction field
    0x00, 0x00, 0x00, 0x00,                         # reserved(2)
    0x66, 0x55, 0x44, 0xff, 0xfe, 0x33, 0x22, 0x11, 0x00, 0x01, # source port id
    0x01, 0xD4,                                                 # sequence id
    0x05,                                                       # control
    0x7f,                                                       # logMessageInterval
    0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x02, # responseOriginTimestamp
    0x66, 0x55, 0x44, 0xff, 0xfe, 0x33, 0x22, 0x12, 0x00, 0x01  # requestingPortIdentity
]


class PTPv2LayerTest(unittest.TestCase):

    def test_dissect_sync_message(self):
        p = PTPv2(bytes(SYNC_MESSAGE_TRACE))
        self.assertEqual(0x1, p.transportSpecific)
        self.assertEqual(0x0, p.messageType)
        self.assertEqual(0xA, p.reserved0)
        self.assertEqual(0x2, p.versionPTP)
        self.assertEqual(0x2C, p.messageLength)
        self.assertEqual(0x00, p.domainNumber)
        self.assertEqual(0x42, p.reserved1)
        self.assertEqual(0x0208, p.flags)
        self.assertEqual(0x00, p.correctionField)
        self.assertEqual(0x12345678, p.reserved2)
        self.assertEqual('66:55:44:33:22:11/1', p.sourcePortIdentity)
        self.assertEqual(0x1D4, p.sequenceId)
        self.assertEqual(0x00, p.control)
        self.assertEqual(-2, p.logMessageInterval)
        self.assertEqual(0x00, p.reserved3)

    def test_dissect_followup_message(self):
        bytestr = bytes(FOLLOW_UP_MESSAGE_TRACE)
        p = PTPv2(bytestr)
        self.assertEqual(0x1, p.transportSpecific)
        self.assertEqual(0x8, p.messageType)
        self.assertEqual(0x0, p.reserved0)
        self.assertEqual(0x2, p.versionPTP)
        self.assertEqual(0x4C, p.messageLength)
        self.assertEqual(0x00, p.domainNumber)
        self.assertEqual(0x00, p.reserved1)
        self.assertEqual(0x0008, p.flags)
        self.assertEqual(0x00, p.correctionField)
        self.assertEqual(0x00, p.reserved2)
        self.assertEqual('66:55:44:33:22:11/1', p.sourcePortIdentity)
        self.assertEqual(0x1D4, p.sequenceId)
        self.assertEqual(0x02, p.control)
        self.assertEqual(-2, p.logMessageInterval)
        self.assertEqual(1.000000002, p.preciseOriginTimestamp)
        self.assertEqual(bytestr[-32:], p.informationTlv)

    def test_dissect_pdelay_req_message(self):
        p = PTPv2(bytes(PDELAY_REQ_MESSAGE_TRACE))
        self.assertEqual(0x1, p.transportSpecific)
        self.assertEqual(0x2, p.messageType)
        self.assertEqual(0x0, p.reserved0)
        self.assertEqual(0x2, p.versionPTP)
        self.assertEqual(0x36, p.messageLength)
        self.assertEqual(0x00, p.domainNumber)
        self.assertEqual(0x00, p.reserved1)
        self.assertEqual(0x0008, p.flags)
        self.assertEqual(0x00, p.correctionField)
        self.assertEqual(0x00, p.reserved2)
        self.assertEqual('66:55:44:33:22:12/1', p.sourcePortIdentity)
        self.assertEqual(0x1D4, p.sequenceId)
        self.assertEqual(0x05, p.control)
        self.assertEqual(-2, p.logMessageInterval)
        self.assertEqual(0, p.reserved3)
        self.assertEqual(0, p.reserved4)

    def test_dissect_pdelay_resp_message(self):
        p = PTPv2(bytes(PDELAY_RESP_MESSAGE_TRACE))
        self.assertEqual(0x1, p.transportSpecific)
        self.assertEqual(0x3, p.messageType)
        self.assertEqual(0x0, p.reserved0)
        self.assertEqual(0x2, p.versionPTP)
        self.assertEqual(0x36, p.messageLength)
        self.assertEqual(0x00, p.domainNumber)
        self.assertEqual(0x00, p.reserved1)
        self.assertEqual(0x0208, p.flags)
        self.assertEqual(0x00, p.correctionField)
        self.assertEqual(0x00, p.reserved2)
        self.assertEqual('66:55:44:33:22:11/1', p.sourcePortIdentity)
        self.assertEqual(0x1D4, p.sequenceId)
        self.assertEqual(0x05, p.control)
        self.assertEqual(127, p.logMessageInterval)
        self.assertEqual(1.000000002, p.requestReceiptTimestamp)
        self.assertEqual('66:55:44:33:22:12/1', p.requestingPortIdentity)

    def test_dissect_pdelay_resp_followup_message(self):
        p = PTPv2(bytes(PDELAY_RESP_FOLLOW_UP_MESSAGE_TRACE))
        self.assertEqual(0x1, p.transportSpecific)
        self.assertEqual(0xA, p.messageType)
        self.assertEqual(0x0, p.reserved0)
        self.assertEqual(0x2, p.versionPTP)
        self.assertEqual(0x36, p.messageLength)
        self.assertEqual(0x00, p.domainNumber)
        self.assertEqual(0x00, p.reserved1)
        self.assertEqual(0x0008, p.flags)
        self.assertEqual(0x00, p.correctionField)
        self.assertEqual(0x00, p.reserved2)
        self.assertEqual('66:55:44:33:22:11/1', p.sourcePortIdentity)
        self.assertEqual(0x1D4, p.sequenceId)
        self.assertEqual(0x05, p.control)
        self.assertEqual(127, p.logMessageInterval)
        self.assertEqual(1.000000002, p.responseOriginTimestamp)
        self.assertEqual('66:55:44:33:22:12/1', p.requestingPortIdentity)
