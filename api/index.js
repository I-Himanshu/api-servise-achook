// api/index.js

const express = require('express');
const app = express();

app.use(express.json());
let issues = [];
let issueIdCounter = 1;

const getCurrentTimestamp = () => new Date().toISOString();

app.post('/api/raiseIssue', (req, res) => {
    const { title, description, priority = 'medium'} = req.body;
    if (!title || !description) {
        return res.status(400).json({
            error: 'Title and description are required fields'
        });
    }

    const newIssue = {
        id: issueIdCounter++,
        title,
        description,
        priority,
        createdAt: getCurrentTimestamp(),
        updatedAt: getCurrentTimestamp()
    };

    issues.push(newIssue);

    res.status(201).json({
        message: 'Issue created successfully',
        issue: newIssue
    });
});

app.get('/api/getIssues', (req, res) => {
    let filteredIssues = [...issues];
    res.json({
        count: filteredIssues.length,
        issues: filteredIssues
    });
});

// Export the express app
module.exports = app;