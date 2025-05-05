import hashlib
import base64

def sha_hash(hash_data, hash_algorithm):
    sha = hashlib.new(hash_algorithm)
    sha.update(hash_data.encode())
    return sha.hexdigest().upper()

def get_sign(data):
    sha1_data = sha_hash(data, "sha1")

    arr1 = [23, 14, 6, 36, 16, 40, 7, 19]
    str1 = ''.join(sha1_data[i] for i in arr1 if i < 40)

    arr2 = [16, 1, 32, 12, 19, 27, 8, 5]
    str2 = ''.join(sha1_data[i] for i in arr2 if i < 40)

    arr3 = [89, 39, 179, 150, 218, 82, 58, 252, 177, 52,
            186, 123, 120, 64, 242, 133, 143, 161, 121, 179]

    # Mapping similar to JS object: {'0': 0, ..., 'F': 15}
    map_hex = {char: i for i, char in enumerate('0123456789ABCDEF')}

    arr4 = []
    for i in range(20):
        c1 = sha1_data[2 * i]
        c2 = sha1_data[2 * i + 1]
        num = map_hex[c1] * 16 + map_hex[c2]
        arr4.append(num ^ arr3[i])

    str3 = base64.b64encode(bytes(arr4)).decode().replace('/', '').replace('+', '').replace('=', '')

    return ('zzc' + str1 + str3 + str2).lower()


