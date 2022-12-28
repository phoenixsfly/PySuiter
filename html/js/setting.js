const save_btn = $('#save_btn');
const export_btn = $('#export_btn')
const cancel_btn = $('#cancel_btn')

const inst_pth_text = $('#install_pth_text')

const pyinst_ver_select = $('#inst_ver_select')
const extra_mod_text = $('#extra_mod_text')

const vscode_inst_chkbox = $('#vscode_inst_chkbox')
const vscode_shortcut_chkbox = $('#vscode_shortcut_chkbox')


let install_pth = null;
let setting_dict = null;

window.addEventListener('pywebviewready', function () {
    pywebview.api.getInstallPath().then(function (result) { install_pth = result });
    pywebview.api.getSettingJSON().then(function (result) {
        setting_dict = result;
        renderSetting();
    });
})

function renderSetting() {
    inst_pth_text.val(install_pth)

    let ava_lst = setting_dict["PYTHON"]["PythonAvailableVersion"]
    for (let i = 0; i < ava_lst.length; i++) {
        pyinst_ver_select.append("<option value=" + ava_lst[i] + ">Python" + ava_lst[i] + "</option>")
    }
    pyinst_ver_select.val(ava_lst[setting_dict["PYTHON"]["PythonSelectVersion"]])


    extra_mod_text.val(setting_dict["PYTHON"]["ExtraModule"].join(" "))

    vscode_inst_chkbox.attr("checked", setting_dict["VSCODE"]["Installation"])
    vscode_shortcut_chkbox.attr("checked", setting_dict["VSCODE"]["Shortcut"])
}

function saveSetting() {
    install_pth = inst_pth_text.val()
    setting_dict["PYTHON"]["PythonSelectVersion"] = pyinst_ver_select.get(0).selectedIndex
    setting_dict["PYTHON"]["ExtraModule"] = extra_mod_text.val().trim().split(/\s+/)
    setting_dict["VSCODE"]["Installation"] = vscode_inst_chkbox.get(0).checked
    setting_dict["VSCODE"]["Shortcut"] = vscode_shortcut_chkbox.get(0).checked
    pywebview.api.setInstallPath(install_pth)
    pywebview.api.setSettingJSON(setting_dict)
}

save_btn.on("click", function () {
    saveSetting();
    alert("保存成功！");
    pywebview.api.close_setting_windows();
});

export_btn.on("click", function () {
    saveSetting();
    pywebview.api.export_setting();
    alert("导出成功！")
    pywebview.api.close_setting_windows();
});

cancel_btn.on("click", function () {
    pywebview.api.close_setting_windows();
});