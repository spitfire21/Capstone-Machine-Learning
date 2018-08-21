var daysOfMonth = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
function dateConvert(data) {
    var res = data.split("/");
    var m = (res[0])*1;
    var monthD = daysOfMonth[res[0]];
    var day = res[1];
    var point = (day/monthD)*1;
    var monthDecimal = (m+point).toFixed(3);
    return monthDecimal;
}
