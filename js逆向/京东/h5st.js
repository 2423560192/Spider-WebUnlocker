
require("./07 env")
require("./06 source")

let jsonData = __process.argv[2]

params = JSON.parse(jsonData)
window.PSign.sign(params).then(function (res){
    console.log(":::"+res.h5st+":::")
    __process.exit()
})


