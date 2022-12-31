$(function () {
  // http://192.168.4.52:27419/shareDoc?salt=c1e19e31130e34e3
  $(".file").on("change", "input[type='file']", function (e) {
    console.log(e);
    // var files = $(this).prop("files");
    // console.log(files);
    // var filename = files[0].name; //获取上传的文件名
    // $(".showName").text(filename);
  });
  $(".file2").on("change", "input[type='file']", function (e) {
    // var files = $(this).prop("files");
    // console.log(files);
    // var filename = files[0].name; //获取上传的文件名
    // $(".showName2").text(filename);
  });
  $.ajax({
    url: "http://124.89.8.210:3008/view_history",
    // url: "http://124.89.8.210:3008/floder_data",
    type: "get",
    // data: data,
    contentType: "application/json", //缺失会出现URL编码，无法转成json对象
    success: function (res) {
      console.log(res);
      var list = res.data;
      if (list.length > 0) {
        var wlist = [];
        list.forEach(function (item) {
          var obj = {};
          obj.create_time = item.create_time;
          obj.img1 = item.img1;
          obj.img2 = item.img2;
          obj.img_url = item.img_url;
          obj.status = item.status;
          obj.tag = item.tag;
          wlist.push(obj);
        });
        var trhtml = "";
        var str = "";
        wlist.forEach(function (item) {
          if (item.tag == 0) {
            str = "无异常";
          } else if (item.tag == 1) {
            str = "有异常";
          }
          let create_time = gettime(item.create_time);
          trhtml +=
            ' <div class="exp-title">' +
            ' <span class="exp-company">' +
            create_time +
            "</span>" +
            '<span class="exp-tag">' +
            str +
            "</span>" +
            " </div>" +
            ' <div class="exp-detail">' +
            '<b class="exp-tag code">' +
            item.img1 +
            "</b>" +
            '<b class="exp-tag design">' +
            item.img2 +
            "</b>" +
            '<img src="' +
            item.img_url +
            '" alt="">' +
            "</div>";

          // "<tr>" +
          // '<td class="center">' +
          // '<label class="position-relative">' +
          // ' <span class="lbl"></span>' +
          // create_time +
          // "</label>" +
          // "</td>" +
          // "<td>" +
          // '<a href="#">' +
          // item.img1 +
          // "</a>" +
          // "</td>" +
          // "<td>" +
          // item.img2 +
          // "</td>" +
          // "<td>" +
          // '<img src="' +
          // item.img_url +
          // '" >' +
          // "</td>" +
          // "<td>" +
          // '<div class="btn-group">' +
          // '<a class="btn btn-xs btn-info " href="' +
          // item.img_url +
          // '" target="_blank">' +
          // ' <i class="fa fa-edit "></i>查看大图' +
          // " </a>" +
          // "</div>" +
          // "</td>" +
          // " </tr>";
          // $(".experience").empty().append(trhtml);
        });
      } else {
        trhtml = '<tr><td  colspan="7">没有查询到对比结果</td></tr>';
        $(".experience").empty().append(trhtml);
      }
    },
  });
  $(".submit").on("click", function () {
    var filename = $(".showName").text();
    var filename2 = $(".showName2").text();
    if (filename == "" || filename == null || filename == undefined) {
      alert("请添加要对比的原始图片！");
      return false;
    } else if (filename2 == "" || filename2 == null || filename2 == undefined) {
      alert("请添加要对比的目标图片！");
      return false;
    } else {
      $("body").loading({
        loadingWidth: 240,
        title: "正在加载...",
        name: "test",
        discription: "正在拼命对比中，请耐心等候p...",
        direction: "column",
        type: "origin",
        originDivWidth: 40,
        originDivHeight: 40,
        originWidth: 6,
        originHeight: 6,
        smallLoading: false,
        loadingMaskBg: "rgba(0,0,0,0.2)",
      });
    }
  });

  // $(".resultimg").attr("src","data:image/jpg;base64,"+ data.imgOut);
  $("#usercard").ajaxForm(function (res) {
    // console.log(res);
    var data = JSON.parse(res.data);
    console.log(data);
    var a = true;
    if (data.tag == a) {
      // alert("上传成功")
      $(".resultimg").attr("src", "data:image/jpg;base64," + data.imgOut);
      //关闭loadding加载中的效果
      removeLoading("test");
    } else if (data.false == 2) {
      alert("照片对比结果完全相同。");
    } else {
      alert("上传失败");
    }
  });

  //格式 Tue Oct 26 2021 20:58:39 GMT+0800 (中国标准时间)格式化
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
});
