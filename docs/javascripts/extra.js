const dialog = document.querySelector("dialog");
const showButton = document.getElementById("export-button");
const closeButton = document.getElementById("close-citation-dialog-button");
const copyButton = document.getElementById("copy-citation");

function copyToClipboard(id)
{
var r = document.createRange();
r.selectNode(document.getElementById(id));
window.getSelection().removeAllRanges();
window.getSelection().addRange(r);
document.execCommand('copy');
window.getSelection().removeAllRanges();
}

// "Show the dialog" button opens the dialog modally
showButton.addEventListener("click", () => {
  dialog.showModal();
});

// "Close" button closes the dialog
closeButton.addEventListener("click", () => {
  dialog.close();
});

copyButton.addEventListener("click", () => {
  copyToClipboard("citation");
})
