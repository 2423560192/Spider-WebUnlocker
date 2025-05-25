splicing = function (data) {
    return data.map(obj => `${obj.x}${obj.y}${obj.time}`).join('');
}
