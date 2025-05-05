const CryptoJS = require('crypto-js'); // For Node.js environment

function decrypt(hexString) {
    var key = CryptoJS.enc.Utf8.parse("ODoDZkNq5SHCL84F");
    var hexData = CryptoJS.enc.Hex.parse(hexString);
    var base64Data = CryptoJS.enc.Base64.stringify(hexData);
    var decrypted = CryptoJS.AES.decrypt(base64Data, key, {
        mode: CryptoJS.mode.ECB,
        padding: CryptoJS.pad.Pkcs7
    });
    var result = decrypted.toString(CryptoJS.enc.Utf8);
    return JSON.parse(result);
}

function encrypt(data) {
    var key = CryptoJS.enc.Utf8.parse("ODoDZkNq5SHCL84F");
    var jsonString = JSON.stringify(data);
    var encrypted = CryptoJS.AES.encrypt(jsonString, key, {
        mode: CryptoJS.mode.ECB,
        padding: CryptoJS.pad.Pkcs7
    });
    var base64Data = encrypted.toString();
    var hexData = CryptoJS.enc.Hex.stringify(CryptoJS.enc.Base64.parse(base64Data));
    return hexData;
}

// The hex string you provided
const encrypted = "7941e4e91da52275127df3b6448b6e4d065cd528733fbbddb7ccd72405817e2b3261eafe575b445bedb773776687c62c2f5d296c538abab1c72a01e6514d070443984ea815b00573d545d134a0fe3bd1a4cd9f8468aa18a1b80aa46273657edad11608a2942a5e5b066f3d3141a22c00796bee0f99f3eb08245c0b5151130f7b768ebbea3b9d9965d183e9a71ae2378efae579f5d8c89c6a40224ea7c214b3a20f6004b1e91364770a1f89d5ec7fd2a3415fe4b1cba0aedbf4f6ef6251a0c19f";


try {
    const decryptedResult = decrypt(encrypted);
    console.log(decryptedResult);
} catch (e) {
    console.error("Decryption failed:", e);
}