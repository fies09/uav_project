$(function () {
  showData();
  function showData() {
    $.ajax({
      url: main + "show_route",
      type: "get",
      // contentType: "application/json", //缺失会出现URL编码，无法转成json对象
      success: function (res) {
        console.log(res);
        // removeLoading("test");
        var list = res.data;
        if (list.length > 0) {
          taskData(list[0].id); //调取任务数据，默认显示第一个航线的任务列表
          var wlist = [];
          list.forEach(function (item) {
            var obj = {};
            obj.create_time = item.create_time;
            obj.id = item.id;
            obj.route_name = item.route_name;
            wlist.push(obj);
          });
          var trhtml = "";
          wlist.forEach(function (item) {
            let create_time = gettime(item.create_time);
            trhtml +=
              '<div class="intro-ani">' +
              ' <section class="sp"> <span class="iconfont icon-hangpai"></span> ' +
              create_time +
              "</section>" +
              " </div>" +
              '<div class="intro-ani">' +
              ' <div class="intro-name"  data-id="' +
              item.id +
              '">' +
              item.route_name +
              "</div>" +
              "</div>";
            $(".intro").empty().append(trhtml);
            $(".intro").find(".intro-name").eq(0).addClass("nameactive");
          });
        } else {
          trhtml = "没有查询到结果";
          $(".intro").empty().append(trhtml);
        }
      },
    });
  }

  //点击航线查看任务
  $(".intro").on("click", ".intro-name", function () {
    $(".intro").find(".intro-name").removeClass("nameactive");
    $(this).addClass("nameactive");
    var tid = $(this).attr("data-id");
    console.log(tid);
    taskData(tid);
  });

  //根据航线查询任务列表
  function taskData(tid) {
    $.ajax({
      url: main + "show_task/" + tid,
      type: "get",
      success: function (res) {
        console.log(res);
        // removeLoading("test");
        var list = res.data;
        if (list.length > 0) {
          var wlist = [];
          list.forEach(function (item) {
            var obj = {};
            obj.id = item.id;
            obj.create_time = item.create_time;
            obj.is_analysis = item.is_analysis;
            obj.is_orimg = item.is_orimg;
            obj.route_name = item.route_name;
            obj.route_id = item.route_id;
            obj.task_name = item.task_name;
            obj.task_process = item.task_process;
            obj.tag = item.tag;
            wlist.push(obj);
          });
          var trhtml = "";
          var is_analysis = "";
          var is_analysis_str = "";
          var is_orimg = "";
          var is_orimg_str = "";
          var tag = "";

          wlist.forEach(function (item) {
            let create_time = gettime(item.create_time); //转换时间格式
            analysis=item.is_analysis.substr(0,1)
            if (analysis == 0) {
              //判断任务对比状态
              is_analysis = "未对比";
              is_analysis_str =
                '<a data-tid="' +
                item.id +
                '" data-rid="' +
                item.route_id +
                '" class="btn btn-xs jumpBtn  analysis">对比</a>';
            } else if (analysis!== 0) {
              is_analysis = item.is_analysis;
              is_analysis_str =
                '<a href="img.html?id=' +
                item.id +
                "&rid=" +
                item.route_id +
                '" class="btn btn-xs jumpBtn" target="_blank">对比结果</a>';
            } 
            //判断任务模板状
            if (item.is_orimg == 1) {
              is_orimg = "模板任务";
              is_orimg_str =
                '<a class="btn btn-xs imgSet" disabled>设为模板</a>';
              is_analysis_str = "无";
            } else if (item.is_orimg == 0) {
              is_orimg = "普通任务";
              is_orimg_str =
                '<a class="btn btn-xs imgSet" data-id="' +
                item.id +
                '" data-rid="' +
                item.route_id +
                '">设为模板</a>';
            }
            //判断对比状态
            if (item.tag== 0) {
              tag = "正常";
              if (analysis == 0) {
                tag = "未对比";
              }
            } else if (item.tag == 1) {
              tag = '异常<i class="icontag iconfont icon-jinggao"></i>';
            }
            if (item.is_orimg == 1) {
              tag = "";
              is_analysis = "";
              is_analysis_str = "";
            }
            trhtml +=
              "<tr>" +
              "<td>" +
              " <span>" +
              item.id +
              "</span>" +
              " </td>" +
              "<td>" +
              item.task_name +
              "</td>" +
              "<td>" +
              is_orimg +
              "</td>" +
              "<td>" +
              is_analysis +
              "</td>" +
              "<td>" +
              item.task_process +
              "</td>" +
              '<td style="white-space:nowrap">' +
              tag +
              "</td>" +
              "<td>" +
              create_time +
              "</td>" +
              " <td>" +
              '<a href="img2.html?id=' +
              item.id +
              '" class=" btn btn-xs jumpBtn" target="_blank">详情</a>' +
              " </td>" +
              " <td>" +
              is_orimg_str +
              " </td>" +
              '<td class="555555"> ' +
              is_analysis_str +
              "</td>" +
              "</tr>";

            $(".taskList").empty().append(trhtml);
          });
        } else {
          trhtml = '<tr><td  colspan="7">没有查询到结果</td></tr>';
          $(".taskList").empty().append(trhtml);
        }
      },
    });
  }

  //设置模板点击时间
  $(".taskList").on("click", ".imgSet", function () {
    var id = $(this).attr("data-id");
    var rid = $(this).attr("data-rid");
    var obj = { tid: id };
    obj = JSON.stringify(obj);
    // console.log(obj);
    $.ajax({
      url: main + "specify_original",
      type: "POST",
      async: false,
      data: obj,
      contentType: "application/json",
      success: function (res) {
        console.log(res);
        taskData(rid);
      },
    });
  });
  //设置任务图片为原图模板

  //点击对比任务图片事件
  $(".taskList").on("click", ".analysis", function () {
    var tid = $(this).attr("data-tid");
    var rid = $(this).attr("data-rid");
    // $(this).text("对比中");
    $(this).attr("disabled");
    var obj = { rid: rid, tid: tid };
    obj = JSON.stringify(obj);
    console.log(obj);
    $.ajax({
      url: main + "contrast_data",
      type: "POST",
      async: false,
      data: obj,
      contentType: "application/json",
      success: function (res) {
        console.log(res);
        if (res.statusCode == 501) {
          alert("请先设置任务对比模板！");
          return false;
        } else if (res.statusCode == "200") {
          alert("已提交对比任务至后台，请稍后查询对比结果！");
          taskData(rid);
        }
      },
    });
  });

  
});
