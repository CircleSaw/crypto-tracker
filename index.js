const { app, BrowserWindow, Menu, ipcMain } = require("electron");
const url = require("url");
const path = require("path");
const axios = require("axios");

let mainWindow;

app.on("ready", () => {
    mainWindow = new BrowserWindow({
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        }
    });

    mainWindow.loadURL(
        url.format({
            pathname: path.join(__dirname, "index.html"),
            protocol: "file:",
            slashes: true
        })
    );

    const mainMenu = Menu.buildFromTemplate(mainMenuTemplate);
    Menu.setApplicationMenu(mainMenu);

    ipcMain.on("key:getCryptoList", async (event, data) => {
        try {
            const response = await axios.post("http://localhost:1337/get_crypto_list", {
                currency: data.currency
            });
            event.reply("key:cryptoResponse", response.data);
        } catch (error) {
            event.reply("key:cryptoResponse", { status: "error", message: "Backend'e bağlanılamadı!" });
        }
    });
});

const mainMenuTemplate = [
    {
        label: "Dev Tools",
        submenu: [
            { label: "Yenile", role: "reload" },
            { label: "Çıkış", role: "quit" }
        ]
    }
];
