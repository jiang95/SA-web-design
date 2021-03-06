window.CLASSES = ["Negative", "Positive"]
window.CSS_CLASSES = ["danger", "success"]

var progressBar = {
    show: function () {
        $(".progress").fadeIn();
    },
    hide: function () {
        $(".progress").hide();
    }
};

$("#showImage").hide();

var show_image = {
    show: function () {
        $("#showImage").show();
    },
    hide: function () {
        $("#showImage").hide();
    }
};

$(function () {
    $("#predict_form").submit(function (e) {
        e.preventDefault();
        show_image.hide();
        progressBar.show();

        $.getJSON("/predict", $(this).serialize()).always(function () {
            progressBar.hide();
        }).done(function (data) {
            //predicted_image.set(data.q, data.image_url);
            $('#predicted_image_url')[0].src = data.image_url;
            console.log($('#predicted_image_url')[0].src);
            //$("#predicted_image_url").attr("src", data.image_url);
            show_image.show();
        });
    });
    $("#train_form").submit(function (e) {
        e.preventDefault();
        progressBar.show();

        $.getJSON("/train", $(this).serialize()).always(function () {
            progressBar.hide();
        }).done(function (data) {
            if (data.result == 1) {
                alert("训练成功！");
            } else {
                alert("亲，出错了？？？？");
            }
        });
    });
});
