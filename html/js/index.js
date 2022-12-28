const btn = $('.swipe_btn');
const silder = $('.swipe_input');
const mask = $('.swipe_progress');
const btn_text = $('.btn_text')
const setting_btn = $('#setting_btn')

const output_text = $('#output')

const success_ui = $('#success_ui')

const open_project_btn = $('#open_project_btn')
const quit_btn = $('#quit_btn')

const install_setting_tip = $('#install_setting_tip')
const install_setting_author = $('#install_setting_author')

let inst_prog_timer = null;

silder.on('input propertychange', setProgessEffect);


window.addEventListener('pywebviewready', function () {
    pywebview.api.getIsCustom().then(function (res) {
        if (res) {
            install_setting_tip.css("display", "flex");
            pywebview.api.getSettingJSON().then(function (res) {
                install_setting_author.text(res['AUTHOR']);
            });

        }
    });
    silder.on('change', () => {
        if (silder.val() > 95) {
            setting_btn.off("click")
            btn.attr("class", "swipe_btn_success")
            setTimeout(function () {
                btn.attr("class", "swipe_btn_none");
                pywebview.api.execute_install();
                inst_prog_timer = setInterval(updateInstallState, 100);
                output_text.css("display", "flex")
            }, 600)
        }
        else {
            silder.val(1);
            setProgessEffect();
        }
    });
})


function setProgessEffect() {
    let L = parseInt(btn.css("width"));
    let R = parseInt(btn.css("border-radius"));
    let k = (L - R) / 100;
    let nval = silder.val();
    nval = (R / 2 + k * nval) / 3
    mask.css("background", `linear-gradient(to right, #00000000 ${nval}%, white ${nval}%, white 100%)`);
    btn_text.css("opacity", 1 - 1.5 * silder.val() / 100.)
}

function updateInstallState() {
    pywebview.api.getInstallCompleted().then((res) => {
        if (res) {
            clearInterval(inst_prog_timer);
            output_text.css("display", "none");
            success_ui.css("display", "flex");
            success_ui.attr("class", "success_ui_display");
            return;
        }
    });
    pywebview.api.getInstallStateText().then((res) => {
        output_text.text(res);
    });
}


setting_btn.click(() => {
    pywebview.api.open_setting_windows();
});

open_project_btn.click(() => {
    pywebview.api.openHelloWorld();
});

quit_btn.click(() => {
    pywebview.api.quit_software();
})



