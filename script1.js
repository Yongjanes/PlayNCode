const { ipcRenderer } = require('electron');

// Get the current window
document.getElementById('minimize').addEventListener('click', () => {
    window.api.minimize();
});

document.getElementById('maximize').addEventListener('click', () => {
    window.api.maximize();
});

document.getElementById('close').addEventListener('click', () => {
    window.api.close();
});

    
// Get references to DOM elements
const textElement = document.getElementById('string');
const runButton = document.getElementById('runPythonButton');

// Add click event listener to the button
runButton.addEventListener('click', () => {
    const domText = textElement.innerText;

    // Send the DOM text to the main process to run the Python script
    ipcRenderer.send('run-python', domText);
});

//Toggle function for btn switching
function hideRunbtn(){
    document.getElementById("getSortedClonedElementsWithId").style.display = 'none';
    document.getElementById("runPythonButton").style.display = 'flex';
}

function hideUploadbtn(){
    document.getElementById("getSortedClonedElementsWithId").style.display = 'flex';
    document.getElementById("runPythonButton").style.display = 'none';
}