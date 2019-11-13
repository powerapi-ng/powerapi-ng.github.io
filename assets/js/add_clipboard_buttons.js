var nodes = document.getElementsByClassName('copyable')

for (var i = 0; i < nodes.length; i++) {
    node = nodes[i].getElementsByTagName("code")[0]
    node_id = "button" + i
    node.setAttribute("id", node_id)
    var button = document.createElement("button");
    button.className = "clipboard_button"
    button.setAttribute("data-clipboard-target", "#"+node_id);

    node.parentNode.insertBefore(button, node);
}

var clipboard = new ClipboardJS(".clipboard_button");
clipboard.on('success', function(e) {
    console.log(e);
});
clipboard.on('error', function(e) {
    console.log(e);
});
