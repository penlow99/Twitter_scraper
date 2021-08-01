let objTable = document.getElementsByClassName("dataframe");
objTable[0].style.fontSize = "x-small";
console.log(document.getElementById('content_csv').innerHTML);

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