//切换图片或者列表模式
$(".tableViewbtn").on("click", function () {
  $(this).addClass("haighlight");
  $(".tableView").css("display", "block");
  $(".gradbtn").removeClass("haighlight");
  $(".grad").css("display", "none");
});
$(".gradbtn").on("click", function () {
  $(this).addClass("haighlight");
  $(".tableViewbtn").removeClass("haighlight");
  $(".tableView").css("display", "none");
  $(".grad").css("display", "block");
});

$(function () {
  removeLoading("test");
  var tid = getQueryString("id");
  // var rid = getQueryString("rid");
  // var tid = 2;
  var obj = { taskid: tid };
  obj = JSON.stringify(obj);
  $.ajax({
    url: main + "over_img",
    type: "post",
    data: obj,
    contentType: "application/json", //缺失会出现URL编码，无法转成json对象
    success: function (res) {
      console.log(res);
      removeLoading("test");
      var list = res.result;
      if (list.length > 0) {
        var ahtml =
          '<a href="' +
          list[1].img_url +
          '" target="_blank" class="showImg">' +
          '<img src="' +
          list[1].img_url +
          '" />' +
          "<div>" +
          list[1].img_name +
          "</div></a>";
        $(".grad .board-img").empty().append(ahtml);
        var wlist = [];
        list.forEach(function (item) {
          var obj = {};
          obj.id = item.id;
          obj.create_time = item.create_time;
          obj.img_name = item.img_name;
          obj.img_url = item.img_url;
          obj.tag = item.tag;
          wlist.push(obj);
        });
        var lihtml = "";
        var trhtml = "";
        var is_analysis = "";
        wlist.forEach(function (item) {
          // let create_time = gettime(item.ceate_time);
          if (item.tag == 1) {
            is_analysis = "异常";
          } else if (item.tag == 0) {
            is_analysis = "正常";
          }
          trhtml += "<tr>" +
          " <td>" +
          item.id +
          "</td>" +
          "<td>" +
          item.img_name +
          "</td>" +
          "<td>" +
          is_analysis +
          "</td>" +
          " <td>" +
          item.create_time +
          "</td>" +
          '<td> <a href="' +
          item.img_url +
          '" class="bigimg" target="_blank">' +
          ' <img src="' +
          item.img_url +
          '" title="点击查看大图" style="width:50px;height:auto" />' +
          "</a></td>" +
          "</tr>";
          lihtml +=
            ' <li class="">' +
            "<img " +
            'src="' +
            item.img_url +
            '"' +
            ' data="' +
            item.img_url +
            '"' +
            ' url="' +
            item.img_url +
            '"' +
            'alt="' +
              item.img_name +
              '"' +
            "</li>";
          $(".ul").empty().append(lihtml);
          $(".tableView .taskList").empty().append(trhtml);
          $(".ul li").eq(0).addClass("active");
        });
      } else {
        trhtml = "没有查询到结果";
        $(".tableView  .taskList").empty().append(trhtml);
      }
    },
  });
});
