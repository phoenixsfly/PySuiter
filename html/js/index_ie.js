const inst_btn = $('#inst_btn');
const setting_btn = $('#setting_btn')
const output_text = $('#output')


const open_project_btn = $('#open_project_btn')
const quit_btn = $('#quit_btn')

let inst_prog_timer = null;

inst_btn.click(function () {
    setting_btn.off("click")
    inst_btn.css('display', 'none');
    output_text.css("display", "flex");
    pywebview.api.execute_install();
    inst_prog_timer = setInterval(updateInstallState, 100);
});


function updateInstallState() {
    pywebview.api.getInstallCompleted().then(function (res) {
        if (res) {
            clearInterval(inst_prog_timer);
            return;
        }
    });
    pywebview.api.getInstallStateText().then(function (res) {
        output_text.text(res);
    });
}


setting_btn.click(function () {
    pywebview.api.open_setting_windows();
});

open_project_btn.click(function () {
    pywebview.api.openHelloWorld();
});

quit_btn.click(function () {
    pywebview.api.quit_software();
})


