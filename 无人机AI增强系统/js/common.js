
//接口网址
main="http://124.89.8.210:3008/"



 //1.格式 Tue Oct 26 2021 20:58:39 GMT+0800 (中国标准时间)格式化
function gettime(data) {
    var data = new Date(data);
    var value =
      data.getFullYear() +
      "-" +
      checkTime(data.getMonth() + 1) +
      "-" +
      checkTime(data.getDate()) +
      " " +
      checkTime(data.getHours()) +
      ":" +
      checkTime(data.getMinutes()) +
      ":" +
      checkTime(data.getSeconds());
    return value;
  }
  // 2.如果时间小于10 ，则再前面加一个'0'
  function checkTime(i) {
    if (i < 10) {
      i = "0" + i;
    }
    return i;
  }

  

//获取地址栏的参数
function getQueryString(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);
    if (r != null) return unescape(r[2]);
    return null;
  }
