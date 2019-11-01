var basicDump = function(response) {
    var newNumberListItem = document.createElement("li");
    var numberListValue = document.createTextNode(response);
    newNumberListItem.appendChild(numberListValue);
    document.getElementById("ul").appendChild(newNumberListItem);
}