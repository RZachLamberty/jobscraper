/* --------------------------------------------------------------------------
 * file constants
 * -------------------------------------------------------------------------- */

var TODAY = new Date();
var YYYYMMDD = TODAY.toISOString().substring(0, 10);


/* --------------------------------------------------------------------------
 * rendering functions
 * -------------------------------------------------------------------------- */

function as_url(data, type, row, meta) {
    return "<a href='" + row.url + "'>" + row.url + "</a>";
}
/*  see this page for some of my previous work here
 *      https://github.com/rlp612/MUBS-Webpage/blob/008dc1c57d1c6695a49e52308c93e92435266f05/FlaskWebProject/static/js/buildingtable.js
 */

/* --------------------------------------------------------------------------
 * making tables
 * -------------------------------------------------------------------------- */

function draw_jobposting_table(tabId, jobData) {
    $(document).ready(function() {
        var buildingtable = $(tabId).DataTable({
            'data': jobData,
            'columns': [
                { 'title': 'Job Title', 'data': 'title' },
                { 'title': 'Company', 'data': 'company' },
                { 'title': 'Description', 'data': 'description' },
                { 'title': 'Link', 'data': 'url', 'render': as_url },
                { 'title': 'Job Board / Source', 'data': 'source' }
            ],
            'order': [1, 'desc'],
            'pageLength': 50
        });
    });
}
