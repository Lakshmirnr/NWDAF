class PFCPParser:
    def parse(self, packet):
        return {
            "protocol": packet.get("protocol","PFCP"),
            "message_type": packet.get("message_type"),
            "seid": packet.get("seid"),
            "teid": packet.get("teid"),
            "sequence_number": packet.get("sequence_number"),
            "fragmented": packet.get("fragmented", False),
            "fragment_id": packet.get("fragment_id"),
            "offset": packet.get("offset"),
            "mf": packet.get("mf",0)
        }
