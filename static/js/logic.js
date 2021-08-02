// shrinks text size of results table for better viewing
if(document.URL.indexOf("scrape") >= 0){ 
    let objTable = document.getElementsByClassName("dataframe");
    objTable[0].style.fontSize = "x-small";
}

// exports csv to downloads folder
function exportCSV() {
    data = document.getElementById("content_csv").textContent;
    let d = new Date();
    fileName = 'twitter_scrape_' + d.toISOString() + '.csv';
    const a = document.createElement("a");
    a.setAttribute('href', 'data:text/csv;charset=utf-8,' + encodeURIComponent(data));
    a.setAttribute('download', fileName);
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

// disables the form and displays message when scraping commences
function disableFieldset() {
    //document.getElementById("fieldset1").setAttribute("disabled", "");
    document.getElementById("scrapeMessage").style.display = 'block';
}
