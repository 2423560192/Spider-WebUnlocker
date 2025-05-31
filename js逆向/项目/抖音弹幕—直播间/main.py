import re


def get_room_id():
    """获取room_id"""
    import requests

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
    }
    cookies = {
        "bd_ticket_guard_client_web_domain": "2",
        "passport_csrf_token": "bff09562aba641f5ac36e668d8706f86",
        "passport_csrf_token_default": "bff09562aba641f5ac36e668d8706f86",
        "ttwid": "1%7Ce6Eo2mKEO7SLzn2DuFQ1fgmK6s12WA1dqmq5c7YILTk%7C1748434877%7C1560d5c7c8429f37f83f0819e0ff7e40ce919211fcdfd427dbbc46649b7da218",
        "UIFID_TEMP": "e71d819f1cb72e7166823ce125547a3e5a83b631a52f7c0b3c34cd9714dd602d173e7c6ad55dda5d6b02a8a796310d9a98a5f1219c5558780d2373cf5d49f265bc41ec458281cf398879d8d16bf9792e",
        "hevc_supported": "true",
        "stream_recommend_feed_params": "%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1920%2C%5C%22screen_height%5C%22%3A1080%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A16%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A100%7D%22",
        "strategyABtestKey": "%221748676400.762%22",
        "volume_info": "%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Afalse%2C%22volume%22%3A0.5%7D",
        "FORCE_LOGIN": "%7B%22videoConsumedRemainSeconds%22%3A180%7D",
        "__security_mc_1_s_sdk_crypt_sdk": "13df0c97-492f-a924",
        "biz_trace_id": "b6eab471",
        "download_guide": "%221%2F20250531%2F0%22",
        "passport_mfa_token": "CjjqA8qfDcM%2FnSKIwPPgV0YGDoXpwEfFzPQBLaCpsYBQ5nYBg%2Bs2u8xRVImzjlFBFwt6IgVLbl%2BkdBpKCjw3e%2B2%2Fn%2Fm7I7oQKdK9x3bU4rpSlH5zTbaAFIBW5vkhqkajm70UuBOBwDmsdRUB1uwrgSfbv%2BwvIBhyKbgQ7unyDRj2sdFsIAIiAQMl59Ol",
        "d_ticket": "67e7b04bd8885499d363e3b7d330ce1954a9c",
        "passport_assist_user": "CkH8VMeJWFNUS7JHzZVNCqZscXImWLdqA87_ebewoqf8gdCjklzdO_dP4HjtbfnLIujabSLBD3enFrvX5p5PI82LiBpKCjwRptGfO-hgsqr1GNPxtoj-moBX6RrcMIHXM5MrBWyyEhxXLlK51_xcP1krjUZ2yL9bRRp4_WWNVLfcho0Q3uvyDRiJr9ZUIAEiAQPIbULR",
        "n_mh": "68eR4AFN8Bz1kkZYAplE9lSkBgSuUKDjxYMU3m709Io",
        "sid_guard": "7bf2c234e13b81b6a8580eb6e82635a9%7C1748676553%7C5184000%7CWed%2C+30-Jul-2025+07%3A29%3A13+GMT",
        "uid_tt": "d4014cdf850a34e7d603c5f622d898df",
        "uid_tt_ss": "d4014cdf850a34e7d603c5f622d898df",
        "sid_tt": "7bf2c234e13b81b6a8580eb6e82635a9",
        "sessionid": "7bf2c234e13b81b6a8580eb6e82635a9",
        "sessionid_ss": "7bf2c234e13b81b6a8580eb6e82635a9",
        "is_staff_user": "false",
        "sid_ucp_v1": "1.0.0-KDJkZDhjNTBiNmFmZThiNTY3OWY4MjhkNjA1OWU5NDIwOWY0ZTkwOWMKIQjd6-DHwYz7BxDJ3-rBBhjvMSAMMLOfhpoGOAdA9AdIBBoCaGwiIDdiZjJjMjM0ZTEzYjgxYjZhODU4MGViNmU4MjYzNWE5",
        "ssid_ucp_v1": "1.0.0-KDJkZDhjNTBiNmFmZThiNTY3OWY4MjhkNjA1OWU5NDIwOWY0ZTkwOWMKIQjd6-DHwYz7BxDJ3-rBBhjvMSAMMLOfhpoGOAdA9AdIBBoCaGwiIDdiZjJjMjM0ZTEzYjgxYjZhODU4MGViNmU4MjYzNWE5",
        "login_time": "1748676551702",
        "_bd_ticket_crypt_cookie": "b0c60ef9e531c2c03ed9af88123dd59c",
        "is_dash_user": "1",
        "__security_mc_1_s_sdk_sign_data_key_web_protect": "a9e7b090-4e96-96ef",
        "__security_mc_1_s_sdk_cert_key": "caf89c3b-4fa9-b749",
        "__security_server_data_status": "1",
        "UIFID": "e71d819f1cb72e7166823ce125547a3e5a83b631a52f7c0b3c34cd9714dd602d60b18eb7f95660a4696293ea1b4af67020cc4ea3f0f8f6ea838ad8ca0355b2d7456abdc4cfecfa689ab1b5d9cf5d5309fb6c21f09047449eef905cf3226ef89294ace1bb7a9d7a6645444c92b671a378ae93359277fbf53fc67be8f912e588b4cac51fecd2b36c880680083d58abdde72798563ca4e002caae1cffaf9811ae71",
        "SelfTabRedDotControl": "%5B%5D",
        "FOLLOW_NUMBER_YELLOW_POINT_INFO": "%22MS4wLjABAAAAm8QjhvLtshyvbQYahsqIKlbu3bJ1nINERhajKNKJ47xQALJ2MGmmeJg9bedB-11K%2F1748707200000%2F0%2F1748676553537%2F0%22",
        "home_can_add_dy_2_desktop": "%221%22",
        "FOLLOW_LIVE_POINT_INFO": "%22MS4wLjABAAAAm8QjhvLtshyvbQYahsqIKlbu3bJ1nINERhajKNKJ47xQALJ2MGmmeJg9bedB-11K%2F1748707200000%2F0%2F1748676645299%2F0%22",
        "stream_player_status_params": "%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A0%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A0%7D%22",
        "__ac_nonce": "0683ab03200786e902e82",
        "__ac_signature": "_02B4Z6wo00f010fesaQAAIDA2boRNqyZpc9H.rUAALnY11",
        "x-web-secsdk-uid": "c9f84431-13db-485e-b995-7ff3f36010d4",
        "xgplayer_device_id": "69060821187",
        "xgplayer_user_id": "35689931448",
        "has_avx2": "null",
        "device_web_cpu_core": "16",
        "device_web_memory_size": "8",
        "live_use_vvc": "%22false%22",
        "csrf_session_id": "cdd0e6c99d28fd7c095a856c25240c53",
        "h265ErrorNumNew": "-1",
        "webcast_local_quality": "origin",
        "fpk1": "U2FsdGVkX18/vbbPnIhGErRvmtNYDBJu13em2fowy14YedA5dvwWO9CNSjxMPFZLTvSFVgJUGA0yDsZ/KDHRLA==",
        "fpk2": "0fe6feb54289f4c67027ec06cc2131f8",
        "xg_device_score": "7.6883778912304805",
        "__live_version__": "%221.1.3.3087%22",
        "live_can_add_dy_2_desktop": "%221%22",
        "bd_ticket_guard_client_data": "eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCR3I3RkE2Qlo2c3pSL1NRTnVhaHYvQWxHckhkSVJpNUFadXlSNURyeDRkaUJkQm9sTzQ2cDFWalphYmJOWnZrclhyU2twQXl1aDhYdGwwajNRZzhjNmM9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoyfQ%3D%3D",
        "publish_badge_show_info": "%220%2C0%2C0%2C1748676712631%22",
        "odin_tt": "bd7a6d7ae30c0ad6460a374c44a6ee9f9e15055cfcf86b6dd8adaa8cdafa1f21f7ce052c421a44161c79605d1b48c1b86d44f3ec822b175e047ff7e3312f1203",
        "IsDouyinActive": "false",
        "passport_fe_beating_status": "false"
    }
    url = "https://live.douyin.com/446424098532"
    response = requests.get(url, headers=headers, cookies=cookies)

    data = response.text
    room_id = str(re.search(r'\\"roomId\\":\\"(\d+)\\"', data).group(1))

    return room_id



if __name__ == '__main__':
    get_room_id()
