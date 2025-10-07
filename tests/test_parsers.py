from app.parsers import ngap_parser, pfcp_parser, http2_parser
import json

def test_ngap():
    line = '2025-10-07T10:32:11Z,AMF1,gNB-23,INITIAL_CONTEXT_SETUP,OK,imsi-00101'
    obj = ngap_parser.parse_line(line)
    assert obj['amf'] == 'AMF1'

def test_pfcp():
    line = '2025-10-07T10:32:12Z,SMF1,UPF-A,SESSION_ESTABLISHMENT,0x9a,0x10'
    obj = pfcp_parser.parse_line(line)
    assert obj['msg_type'] == 'SESSION_ESTABLISHMENT'

def test_http2():
    line = json.dumps({"ts":"2025-10-07T10:32:13Z","src_nf":"AMF1","dst_nf":"PCF1","path":"/nudm-sdm/v2","method":"GET","status":200,"lat_ms":22})
    obj = http2_parser.parse_line(line)
    assert obj['status'] == 200
