function get_ack() {
    s = "internal_src:pushserver|first_req_ms:1748867891845|wss_msg_type:wrds|wrds_v:7511330401164464774"
    e = {
        "SeqID": "1",
        "LogID": "4359682615984603653",
        "service": 8888,
        "method": 8,
        "payload_encoding": "pb",
        "payload_type": "msg",
        "LodIDNew": ""
    }
    encode({
        payload_type: "ack",
        payload: function (e) {
            let n = [];
            for (let i of e) {
                let e = i.charCodeAt(0);
                e < 128 ? n.push(e) : e < 2048 ? (n.push(192 + (e >> 6)),
                    n.push(128 + (63 & e))) : e < 65536 && (n.push(224 + (e >> 12)),
                    n.push(128 + (e >> 6 & 63)),
                    n.push(128 + (63 & e)))
            }
            return new Uint8Array(n)
        }(s),
        LogID: e.LogID
    }, "PushFrame")

    console.log(param_1)
}

get_ack()
