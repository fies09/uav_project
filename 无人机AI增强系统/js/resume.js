$(function () {
  // skill
  // for(var i=0; i<4; i++){
  //     $('.ability li').eq(0).find('i').eq(i).addClass('full')
  // }
  // setTimeout(()=>{
  //     for(var i=0; i<3; i++){
  //         $('.ability li').eq(1).find('i').eq(i).addClass('full')
  //     }
  // },200)
  // setTimeout(()=>{
  //     for(var i=0; i<4; i++){
  //         $('.ability li').eq(2).find('i').eq(i).addClass('full')
  //     }
  // },400)
  // setTimeout(()=>{
  //     for(var i=0; i<2; i++){
  //         $('.ability li').eq(3).find('i').eq(i).addClass('full')
  //     }
  // },600)
  // setTimeout(()=>{
  //     for(var i=0; i<3; i++){
  //         $('.ability li').eq(4).find('i').eq(i).addClass('full')
  //     }
  // },800)
  // setTimeout(()=>{
  //     for(var i=0; i<3; i++){
  //         $('.ability li').eq(5).find('i').eq(i).addClass('full')
  //     }
  // },1000)

  // works
  workShow();

  //点击小图片时使大图切换至当前点击的图片
  $(".thumbnail .ul").on("click","li",function () {
    $(this).siblings().removeClass("active");
    $(this).addClass("active");
    workShow();
  });

  //当鼠标移入或移出图片时，图片自动切换功能暂停。
  var timer = setInterval(() => {
    timerFunc();
  }, 4000);
  $(".grad .board-img").mouseover(function () {
    clearInterval(timer);
  });
  $(".grad .board-img").mouseleave(function () {
    timer = setInterval(() => {
      timerFunc();
    }, 4000);
  });
});

function workShow() {
  var obj = $(".thumbnail ul li.active img");
  $(".grad .board-img").find("img").removeClass("board-ani");
  $(".grad .board-img").find("a").attr("href", obj.attr("url"));
  $(".grad .board-img").find("div").remove();

  setTimeout(function () {
    $(".grad .board-img").find("img").attr("src", obj.attr("data"));
    $(".grad .board-img").find("img").addClass("board-ani");
    $(".grad .board-img")
      .find("img")
      .after('<div class="board-text-ani">' + obj.attr("alt") + "</div>");
  }, 100);
}

function timerFunc() {
  if (
    $(".thumbnail ul li.active").index() ==
    $(".thumbnail ul li").length - 1
  ) {
    $(".thumbnail ul li").eq(0).trigger("click");
  } else {
    $(".thumbnail ul li.active").next().trigger("click");
  }
  workShow();
}

//顶部时间
function getTime() {
  var myDate = new Date();
  var myYear = myDate.getFullYear(); //获取完整的年份(4位,1970-????)
  var myMonth = myDate.getMonth() + 1; //获取当前月份(0-11,0代表1月)
  var myToday = myDate.getDate(); //获取当前日(1-31)
  var myDay = myDate.getDay(); //获取当前星期X(0-6,0代表星期天)
  var myHour = myDate.getHours(); //获取当前小时数(0-23)
  var myMinute = myDate.getMinutes(); //获取当前分钟数(0-59)
  var mySecond = myDate.getSeconds(); //获取当前秒数(0-59)
  var week = [
    "星期日",
    "星期一",
    "星期二",
    "星期三",
    "星期四",
    "星期五",
    "星期六",
  ];
  var nowTime;

  nowTime =
    myYear +
    "-" +
    fillZero(myMonth) +
    "-" +
    fillZero(myToday) +
    "&nbsp;&nbsp;" +
    fillZero(myHour) +
    ":" +
    fillZero(myMinute) +
    ":" +
    fillZero(mySecond) +
    "&nbsp;&nbsp;" +
    week[myDay] +
    "&nbsp;&nbsp;";
  //console.log(nowTime);
  $("#time").html(nowTime);
}
function fillZero(str) {
  var realNum;
  if (str < 10) {
    realNum = "0" + str;
  } else {
    realNum = str;
  }
  return realNum;
}
setInterval(getTime, 1000);

$(document).ready(function () {
  var whei = $(window).width();
  $("html").css({ fontSize: whei / 22 });
  $(window).resize(function () {
    var whei = $(window).width();
    $("html").css({ fontSize: whei / 22 });
  });
});
