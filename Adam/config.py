# -*- encoding:utf-8 -*-
import os

class Config(object):
    DEBUG = True
    RETRY_COUNT = 3
    REMOTE_ELEMENT_URL = "http://localhost:8888/get_page_elements"
    driver_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chromedriver")
    username = os.environ.get("username")
    password = os.environ.get("password")
    mysql = {
        "host": "",
        "port": "3310",
        "db": "",
        "user": "",
        "password": ""
    }


report_template = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8"/>
    <title>WEB前端测试报告</title>
    <style>body {
	font-family: Helvetica, Arial, sans-serif;
	font-size: 12px;
	min-width: 1200px;
	color: #999;
}
h2 {
	font-size: 16px;
	color: black;
}

p {
    color: black;
}

a {
	color: #999;
}

table {
	border-collapse: collapse;
}

/******************************
 * SUMMARY INFORMATION
 ******************************/

#environment td {
	padding: 5px;
	border: 1px solid #E6E6E6;
}

#environment tr:nth-child(odd) {
	background-color: #f6f6f6;
}

/******************************
 * TEST RESULT COLORS
 ******************************/
span.passed, .passed .col-result {
	color: green;
}
span.skipped, span.xfailed, span.rerun, .skipped .col-result, .xfailed .col-result, .rerun .col-result {
	color: orange;
}
span.error, span.failed, span.xpassed, .error .col-result, .failed .col-result, .xpassed .col-result  {
	color: red;
}


/******************************
 * RESULTS TABLE
 *
 * 1. Table Layout
 * 2. Extra
 * 3. Sorting items
 *
 ******************************/

/*------------------
 * 1. Table Layout
 *------------------*/

#results-table {
	border: 1px solid #e6e6e6;
	color: #999;
	font-size: 12px;
	width: 100%
}

#results-table th, #results-table td {
	padding: 5px;
	border: 1px solid #E6E6E6;
	text-align: left
}
#results-table th {
	font-weight: bold
}

/*------------------
 * 2. Extra
 *------------------*/

.log:only-child {
	height: inherit
}
.log {
	background-color: #e6e6e6;
	border: 1px solid #e6e6e6;
	color: black;
	display: block;
	font-family: "Courier New", Courier, monospace;
	height: 230px;
	overflow-y: scroll;
	padding: 5px;
	white-space: pre-wrap
}
div.image {
	border: 1px solid #e6e6e6;
	float: right;
	height: 240px;
	margin-left: 5px;
	overflow: hidden;
	width: 320px
}
div.image img {
	width: 320px
}
.collapsed {
	display: none;
}
.expander::after {
	content: " (展开明细)";
	color: #BBB;
	font-style: italic;
	cursor: pointer;
}
.collapser::after {
	content: " (收起明细)";
	color: #BBB;
	font-style: italic;
	cursor: pointer;
}

/*------------------
 * 3. Sorting items
 *------------------*/
.sortable {
	cursor: pointer;
}

.sort-icon {
	font-size: 0px;
	float: left;
	margin-right: 5px;
	margin-top: 5px;
	/*triangle*/
	width: 0;
	height: 0;
	border-left: 8px solid transparent;
	border-right: 8px solid transparent;
}

.inactive .sort-icon {
	/*finish triangle*/
	border-top: 8px solid #E6E6E6;
}

.asc.active .sort-icon {
	/*finish triangle*/
	border-bottom: 8px solid #999;
}

.desc.active .sort-icon {
	/*finish triangle*/
	border-top: 8px solid #999;
}
</style>

<link type="text/css" href="static/left.css" rel="stylesheet" />
<script type="text/javascript" src="static/jquery.js"></script>
<script type="text/javascript" src="static/jquery.pikachoose.js"></script>
</head>
  <body>
    <script>/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this file,
 * You can obtain one at http://mozilla.org/MPL/2.0/. */
$(document).ready(function (){
        $("#pikame").PikaChoose({carousel:true, carouselVertical:true});
    });

function toArray(iter) {
    if (iter === null) {
        return null;
    }
    return Array.prototype.slice.call(iter);
}

function find(selector, elem) {
    if (!elem) {
        elem = document;
    }
    return elem.querySelector(selector);
}

function find_all(selector, elem) {
    if (!elem) {
        elem = document;
    }
    return toArray(elem.querySelectorAll(selector));
}

function sort_column(elem) {
    toggle_sort_states(elem);
    var colIndex = toArray(elem.parentNode.childNodes).indexOf(elem);
    var key;
    if (elem.classList.contains('numeric')) {
        key = key_num;
    } else if (elem.classList.contains('result')) {
        key = key_result;
    } else {
        key = key_alpha;
    }
    sort_table(elem, key(colIndex));
}

function show_all_extras() {
    find_all('.col-result').forEach(show_extras);
}

function hide_all_extras() {
    find_all('.col-result').forEach(hide_extras);
}

function show_extras(colresult_elem) {
    var extras = colresult_elem.parentNode.nextElementSibling;
    var expandcollapse = colresult_elem.firstElementChild;
    extras.classList.remove("collapsed");
    expandcollapse.classList.remove("expander");
    expandcollapse.classList.add("collapser");
}

function hide_extras(colresult_elem) {
    var extras = colresult_elem.parentNode.nextElementSibling;
    var expandcollapse = colresult_elem.firstElementChild;
    extras.classList.add("collapsed");
    expandcollapse.classList.remove("collapser");
    expandcollapse.classList.add("expander");
}

function show_filters() {
    var filter_items = document.getElementsByClassName('filter');
    for (var i = 0; i < filter_items.length; i++)
        filter_items[i].hidden = false;
}

function add_collapse() {
    // Add links for show/hide all
    var resulttable = find('table#results-table');
    var showhideall = document.createElement("p");
    showhideall.innerHTML = '<a href="javascript:show_all_extras()">展开所有明细</a> / ' +
                            '<a href="javascript:hide_all_extras()">收起所有明细</a>';
    resulttable.parentElement.insertBefore(showhideall, resulttable);

    // Add show/hide link to each result
    find_all('.col-result').forEach(function(elem) {
        var extras = elem.parentNode.nextElementSibling;
        var expandcollapse = document.createElement("span");
        if (elem.innerHTML === 'Passed') {
            extras.classList.add("collapsed");
            expandcollapse.classList.add("expander");
        } else {
            expandcollapse.classList.add("collapser");
        }
        elem.appendChild(expandcollapse);

        elem.addEventListener("click", function(event) {
            if (event.currentTarget.parentNode.nextElementSibling.classList.contains("collapsed")) {
                show_extras(event.currentTarget);
            } else {
                hide_extras(event.currentTarget);
            }
        });
    })
}
addEventListener("DOMContentLoaded", function() {
    reset_sort_headers();

    add_collapse();

    show_filters();

    toggle_sort_states(find('.initial-sort'));

    find_all('.sortable').forEach(function(elem) {
        elem.addEventListener("click",
                              function(event) {
                                  sort_column(elem);
                              }, false)
    });

});

function sort_table(clicked, key_func) {
    var rows = find_all('.results-table-row');
    var reversed = !clicked.classList.contains('asc');
    var sorted_rows = sort(rows, key_func, reversed);
    /* Whole table is removed here because browsers acts much slower
     * when appending existing elements.
     */
    var thead = document.getElementById("results-table-head");
    document.getElementById('results-table').remove();
    var parent = document.createElement("table");
    parent.id = "results-table";
    parent.appendChild(thead);
    sorted_rows.forEach(function(elem) {
        parent.appendChild(elem);
    });
    document.getElementsByTagName("BODY")[0].appendChild(parent);
}

function sort(items, key_func, reversed) {
    var sort_array = items.map(function(item, i) {
        return [key_func(item), i];
    });
    var multiplier = reversed ? -1 : 1;

    sort_array.sort(function(a, b) {
        var key_a = a[0];
        var key_b = b[0];
        return multiplier * (key_a >= key_b ? 1 : -1);
    });

    return sort_array.map(function(item) {
        var index = item[1];
        return items[index];
    });
}

function key_alpha(col_index) {
    return function(elem) {
        return elem.childNodes[1].childNodes[col_index].firstChild.data.toLowerCase();
    };
}

function key_num(col_index) {
    return function(elem) {
        return parseFloat(elem.childNodes[1].childNodes[col_index].firstChild.data);
    };
}

function key_result(col_index) {
    return function(elem) {
        var strings = ['Error', 'Failed', 'Rerun', 'XFailed', 'XPassed',
                       'Skipped', 'Passed'];
        return strings.indexOf(elem.childNodes[1].childNodes[col_index].firstChild.data);
    };
}

function reset_sort_headers() {
    find_all('.sort-icon').forEach(function(elem) {
        elem.parentNode.removeChild(elem);
    });
    find_all('.sortable').forEach(function(elem) {
        var icon = document.createElement("div");
        icon.className = "sort-icon";
        icon.textContent = "vvv";
        elem.insertBefore(icon, elem.firstChild);
        elem.classList.remove("desc", "active");
        elem.classList.add("asc", "inactive");
    });
}

function toggle_sort_states(elem) {
    //if active, toggle between asc and desc
    if (elem.classList.contains('active')) {
        elem.classList.toggle('asc');
        elem.classList.toggle('desc');
    }

    //if inactive, reset all other functions and add ascending active
    if (elem.classList.contains('inactive')) {
        reset_sort_headers();
        elem.classList.remove('inactive');
        elem.classList.add('active');
    }
}

function is_all_rows_hidden(value) {
  return value.hidden == false;
}

function filter_table(elem) {
    var outcome_att = "data-test-result";
    var outcome = elem.getAttribute(outcome_att);
    class_outcome = outcome + " results-table-row";
    var outcome_rows = document.getElementsByClassName(class_outcome);

    for(var i = 0; i < outcome_rows.length; i++){
        outcome_rows[i].hidden = !elem.checked;
    }

    var rows = find_all('.results-table-row').filter(is_all_rows_hidden);
    var all_rows_hidden = rows.length == 0 ? true : false;
    var not_found_message = document.getElementById("not-found-message");
    not_found_message.hidden = !all_rows_hidden;
}
</script>
    <h2>WEB前端测试报告</h2>

    <p>共计运行: {{ test_result.case_count }} 个测试用例，运行耗时: {{ test_result.total_time| round(2, 'floor') }} 秒. </p>
    <div>
        <input checked="true" class="filter" data-test-result="passed" hidden="true" name="filter_checkbox" onChange="filter_table(this)" type="checkbox"/>
        <span class="passed">{{ test_result.pass_count }} 通过</span>,
        <input checked="true" class="filter" data-test-result="skipped" hidden="true" name="filter_checkbox" onChange="filter_table(this)" type="checkbox"/>
        <span class="skipped">{{ test_result.skipped_count }} 跳过</span>,
        <input checked="true" class="filter" data-test-result="failed" hidden="true" name="filter_checkbox" onChange="filter_table(this)" type="checkbox"/>
        <span class="failed">{{ test_result.failed_count }} 失败</span>,
        <input checked="true" class="filter" data-test-result="error" disabled="true" hidden="true" name="filter_checkbox" onChange="filter_table(this)" type="checkbox"/>
        <span class="error">{{ test_result.error_count }} 异常</span>
    </div>
    <h2>Results</h2>
    <table id="results-table">
      <thead id="results-table-head">
        <tr>
          <th class="sortable result initial-sort" col="result">Result</th>
          <th class="sortable" col="name">Test</th>
          <th class="sortable numeric" col="duration">Duration</th>
        <tr hidden="true" id="not-found-message">
          <th colspan="5">No results found. Try to check the filters</th></tr></thead>
{% for module in test_result.extras %}
    {% for case in module.cases %}
      <tbody class="{{ case.type }} results-table-row">
        <tr>
          <td class="col-result">{{ case.type|capitalize }}</td>
          <td class="col-name">{{ case.module_name }}.{{ case.name }}</td>
          <td class="col-duration">{{ case.cost_time| round(2, 'floor') }} 秒</td>
        </tr>
        <tr>
          <td class="extra" colspan="5">
            <div class="log">{{ case.log|safe }}</div>
          </td>
        </tr>
      </tbody>
    {% endfor %}
{% endfor %}
    </table>
{% if test_result.screenshoots %}
    <h2>ScreenShoots</h2>

    <div class="pikachoose">
        <ul id="pikame" class="jcarousel-skin-pika">
            {% for sc in test_result.screenshoots %}
                <li><a href="javascript:;"><img src="../{{ sc.file }}"/></a><span>{{ sc.dir }}</span></li>
            {% endfor %}
        </ul>
    </div>
{% endif %}
  </body>
</html>
"""