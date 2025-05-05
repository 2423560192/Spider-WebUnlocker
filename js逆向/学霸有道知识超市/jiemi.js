const CryptoJS = require("crypto-js");

// 数据定义（使用你提供的 encrypt_body）
const data = {
    "encrypt_body": "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".toLowerCase()
};

// 密钥
const p = "zhl@k*^5f45H$r3*";

// 解密函数
function decrypt(e, o) {
    try {
        const key = CryptoJS.enc.Utf8.parse(o);
        console.log('key::' , key)
        const decrypted = CryptoJS.AES.decrypt(e, key, {
            mode: CryptoJS.mode.ECB,
            padding: CryptoJS.pad.Pkcs7
        });
        const utf8String = decrypted.toString(CryptoJS.enc.Utf8);
        if (!utf8String) {
            throw new Error("解密结果为空或无效 UTF-8");
        }
        return utf8String;
    } catch (error) {
        console.error("解密失败:", error.message);
        // 输出调试信息
        const keyHex = CryptoJS.enc.Utf8.parse(o).toString(CryptoJS.enc.Hex);
        console.log("密钥（Hex）:", keyHex);
        console.log("加密数据长度:", e.length);
        const decryptedHex = CryptoJS.AES.decrypt(e, CryptoJS.enc.Utf8.parse(o), {
            mode: CryptoJS.mode.ECB,
            padding: CryptoJS.pad.Pkcs7
        }).toString(CryptoJS.enc.Hex);
        console.log("解密的二进制数据（Hex）:", decryptedHex);
        return null;
    }
}

// 数据处理函数
function jie(dataObj) {
    try {
        const encryptedData = dataObj.encrypt_body;
        console.log("加密数据（Base64）:", encryptedData.substring(0, 50) + "...");
        const decryptedData = decrypt(encryptedData, p);

        if (!decryptedData) {
            throw new Error("解密结果为空");
        }

        console.log("解密后的字符串:", decryptedData);
        const parsedData = JSON.parse(decryptedData);
        console.log("解析后的 JSON:", parsedData);
        return parsedData;
    } catch (error) {
        console.error("处理失败:", error.message);
    }
}

// 执行解密
jie(data);