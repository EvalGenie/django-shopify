"use strict";
document.addEventListener("DOMContentLoaded", function () {
    // =========================================================
    // =========    Menu Customizer [ HTML ] code   ============
    // =========================================================
    document.querySelector('body').insertAdjacentHTML("beforeend", '' +
        '<div id="styleSelector" class="menu-styler">' +
        '<div class="style-toggler">' +
        '<a href="#!"></a>' +
        '</div>' +
        '<div class="style-block">' +
        '<h6 class="mb-2">EvalGenie Bug Report</h6>' +
        '<hr class="my-0">' +
        '<div class="theme-color layout-type">' +
        '<iframe src="https://docs.google.com/forms/d/e/1FAIpQLScMUtu8XfUlaz1wtyCGdCFo6YSwg3ZFIzM3sDIK2FhzWmBtOw/viewform?embedded=true" width="400" height="500" frameborder="0" marginheight="0" marginwidth="0">Loading…</iframe>' +
        '</div>' +
        
        '<div class="tab-pane fade" id="pills-pages" role="tabpanel" aria-labelledby="pills-pages-tab">' +
        '<div class="form-group mb-0">' +
        '<div class="switch switch-primary d-inline m-r-10">' +
        '<input type="checkbox" id="theme-rtl">' +
        '<label for="theme-rtl" class="cr"></label>' +
        '</div>' +
        '<label>RTL</label>' +
        '</div>' +
        '<div class="form-group mb-0">' +
        '<div class="switch switch-primary d-inline m-r-10">' +
        '<input type="checkbox" id="menu-fixed" checked>' +
        '<label for="menu-fixed" class="cr"></label>' +
        '</div>' +
        '<label>Menu Fixed</label>' +
        '</div>' +
        '<div class="form-group mb-0">' +
        '<div class="switch switch-primary d-inline m-r-10">' +
        '<input type="checkbox" id="header-fixed">' +
        '<label for="header-fixed" class="cr"></label>' +
        '</div>' +
        '<label>Header Fixed</label>' +
        '</div>' +
        '<div class="form-group mb-0">' +
        '<div class="switch switch-primary d-inline m-r-10">' +
        '<input type="checkbox" id="box-layouts">' +
        '<label for="box-layouts" class="cr"></label>' +
        '</div>' +
        '<label>Box Layouts</label>' +
        '</div>' +
        
        '</div>' +
        '</div>' +
        '</div>' +
        '</div>' +
        '</div>');
    setTimeout(function () {
        document.querySelector('#pills-cust-tabContent').style.cssText = `
            height: calc(100vh - 430px);
            position: relative;
        `;
        var px = new PerfectScrollbar('#pills-cust-tabContent', {
            wheelSpeed: .5,
            swipeEasing: 0,
            suppressScrollX: !0,
            wheelPropagation: 1,
            minScrollbarLength: 40,
        });
    }, 400);
    // =========================================================
    // ==================    Menu Customizer Start   ===========
    // =========================================================
    // open Menu Styler
    var pctoggle = document.querySelector("#styleSelector > .style-toggler");
    if (pctoggle) {
        pctoggle.addEventListener('click', function () {
            if (!document.querySelector("#styleSelector").classList.contains('open')) {
                document.querySelector("#styleSelector").classList.add("open");
            } else {
                document.querySelector("#styleSelector").classList.remove("open");
            }
        });
    }
    // ==================    Menu Customizer End   =============
    // =========================================================
});
// Menu Dropdown icon
function drpicon(temp) {
    if (temp == "style1") {
        removeClassByPrefix(document.querySelector(".pcoded-navbar"), 'drp-icon-');
    } else {
        removeClassByPrefix(document.querySelector(".pcoded-navbar"), 'drp-icon-');
        document.querySelector(".pcoded-navbar").classList.add('drp-icon-' + temp);
    }
}
// Menu subitem icon
function menuitemicon(temp) {
    if (temp == "style1") {
        removeClassByPrefix(document.querySelector(".pcoded-navbar"), 'menu-item-icon-');
    } else {
        removeClassByPrefix(document.querySelector(".pcoded-navbar"), 'menu-item-icon-');
        document.querySelector(".pcoded-navbar").classList.add('menu-item-icon-' + temp);
    }
}

function removeClassByPrefix(node, prefix) {
    for (let i = 0; i < node.classList.length; i++) {
        let value = node.classList[i];
        if (value.startsWith(prefix)) {
            node.classList.remove(value);
        }
    }
}