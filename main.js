const { app, BrowserWindow, ipcMain } = require('electron')
const path = require('path');
const { exec } = require('child_process');


function createWindow () {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    // frame:false,
    // titleBarStyle:'hidden',
    webPreferences: {
      enableRemoteModule:false,
      nodeIntegration: true,
      contextIsolation: false 
    }
  })
  
  win.loadFile('index.html')
  win.webContents.openDevTools();
}

ipcMain.on('run-python', (event, domText) => {
  console.log(`Text received from DOM: ${domText}`);

  // Run Python script and pass the DOM text as an argument
  exec(`python write_again.py "${domText}"`, (error, stdout, stderr) => {
      if (error) {
          console.error(`Error: ${error.message}`);
          return;
      }
      if (stderr) {
          console.error(`Stderr: ${stderr}`);
          return;
      }
      console.log(stdout);
      event.reply(stdout); // Send output back to the renderer
  });
});

app.whenReady().then(createWindow)

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow()
  }
})