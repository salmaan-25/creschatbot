import express from 'express';
import bodyParser from 'body-parser';
import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

// Resolve __dirname for ES module compatibility
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = 3000;

// Middleware
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Render the index page
app.get('/', (req, res) => {
    res.render('index');
});

// Handle form submission
app.post('/chat', (req, res) => {
    const userInput = req.body.userInput;

    // Spawn a Python process to scrape the URL based on user input
    const pythonProcess = spawn('python', ['C:\\Users\\MOHAMED SALMAAN\\OneDrive\\Desktop\\crescentchatbot-master\\crescentchatbot-master\\chatbot.py', userInput]);

    let responseData = '';

    pythonProcess.stdout.on('data', (data) => {
        responseData += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
        if (!res.headersSent) {
            res.status(500).send('An error occurred while processing your request.');
        }
    });

    pythonProcess.on('close', (code) => {
        console.log(`Python process exited with code ${code}`);
        if (code === 0 && !res.headersSent) {
            try {
                const parsedResponse = JSON.parse(responseData);
                res.json(parsedResponse);  // Send the JSON response to the frontend
            } catch (err) {
                res.status(500).send('Error parsing Python response.');
            }
        }
    });
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
