def encrypt_group(group):
    result = []
    for char in group:
        # 获取字符的 ASCII 值
        ascii_value = ord(char)

        # 执行左移3位并与右移5位进行按位或
        encrypted = (ascii_value << 3) | (ascii_value >> 5)

        # 异或0x5A
        encrypted ^= 0x5A

        # 左移2位并与取模6的结果进行按位或
        encrypted = (encrypted << 2) | (encrypted % 6)

        # 再次异或0x3F
        encrypted ^= 0x3F

        # 保持为一个字节范围
        encrypted = encrypted % 0x100

        # 将加密后的字符添加到结果列表中
        result.append(chr(encrypted))

    # 返回加密后的字符串
    return ''.join(result)


def group_message(text, size=4):
    # 将输入字符串按指定大小切分成小组
    return [text[i:i + size] for i in range(0, len(text), size)]


def merge_groups(groups):
    # 合并所有小组，得到一个完整的字符串
    return ''.join(groups)


def to_hex_string(data):
    # 将每个字符转换为其对应的十六进制表示
    return ''.join(f'{ord(c):02x}' for c in data)


def OOOoO(input_string):
    group_size = 4
    # 将输入字符串分组
    groups = group_message(input_string, group_size)
    # 加密每一个分组
    encrypted_groups = [encrypt_group(group) for group in groups]
    # 合并加密后的分组
    merged = merge_groups(encrypted_groups)
    # 将最终结果转换为十六进制
    return to_hex_string(merged)


# 测试
result = OOOoO("123456")
print(result)
