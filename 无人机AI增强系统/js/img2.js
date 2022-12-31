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
  var tid = getQueryString("id");
  imgData(tid);
  function imgData(tid) {
    $.ajax({
      url: main + "img_for_task/" + tid + "/",
      type: "get",
      contentType: "application/json", //缺失会出现URL编码，无法转成json对象
      success: function (res) {
        console.log(res);
        var list = res.data;
        if (list.length > 0) {
          var ahtml =
            '<a href="' +
            list[0].img_url +
            '" target="_blank" class="showImg">' +
            '<img src="' +
            list[0].img_url +
            '" />' +
            "<div>" +
            list[0].img_name +
            "</div></a>";
          $(".grad .board-img").empty().append(ahtml);
          var wlist = [];
          list.forEach(function (item) {
            var obj = {};
            obj.id = item.id;
            obj.ceate_time = item.ceate_time;
            obj.img_name = item.img_name;
            obj.img_url = item.img_url;
            obj.is_analysis = item.is_analysis;
            wlist.push(obj);
          });
          var lihtml = "";
          var trhtml = "";
          var is_analysis = "";
          wlist.forEach(function (item) {
            let create_time = gettime(item.ceate_time);
            if (item.is_analysis == 1) {
              is_analysis = "已对比";
            } else if (item.is_analysis == 0) {
              is_analysis = "未对比";
            }
            trhtml +=
              "<tr>" +
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
              create_time +
              "</td>" +
              '<td> <a href="' +
              item.img_url +
              '" class="bigimg" target="_blank">' +
              ' <img src="' +
              item.img_url +
              '" title="点击查看大图" style="width:50px;height:auto"  />' +
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
              'url="' +
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
          $(".tableView .taskList").empty().append(trhtml);
        }
      },
    });
  }
});
