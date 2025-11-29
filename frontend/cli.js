#!/usr/bin/env node

const axios = require('axios');
const inquirer = require('inquirer');
const chalk = require('chalk');
const ora = require('ora');
require('dotenv').config();

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:5000';

// Display banner
function displayBanner() {
    console.clear();
    console.log(chalk.cyan.bold('═'.repeat(80)));
    console.log(chalk.cyan.bold('  TELECOM TICKET ANALYSIS ASSISTANT - CLI'));
    console.log(chalk.cyan.bold('═'.repeat(80)));
    console.log();
}

// Display main menu
async function mainMenu() {
    const choices = [
        { name: '📝 Analyze New Ticket', value: 'analyze' },
        { name: '🔍 Search Similar Tickets', value: 'search' },
        { name: '📊 View System Stats', value: 'stats' },
        { name: '❌ Exit', value: 'exit' }
    ];

    const answer = await inquirer.prompt([
        {
            type: 'list',
            name: 'action',
            message: 'What would you like to do?',
            choices: choices
        }
    ]);

    return answer.action;
}

// Analyze ticket
async function analyzeTicket() {
    console.log(chalk.yellow('\n📝 Analyze New Ticket\n'));
    
    const answers = await inquirer.prompt([
        {
            type: 'input',
            name: 'subject',
            message: 'Ticket Subject:',
            validate: (input) => input.length > 0 || 'Subject is required'
        },
        {
            type: 'editor',
            name: 'description',
            message: 'Ticket Description (press Enter to open editor):',
            validate: (input) => input.length >= 10 || 'Description must be at least 10 characters'
        }
    ]);

    const ticketDescription = `Subject: ${answers.subject}\n\nDescription: ${answers.description}`;

    const spinner = ora('Analyzing ticket...').start();

    try {
        const response = await axios.post(`${BACKEND_URL}/api/analyze`, {
            ticket_description: ticketDescription
        });

        spinner.succeed('Analysis complete!');

        const result = response.data;
        displayAnalysisResults(result);

    } catch (error) {
        spinner.fail('Analysis failed');
        console.error(chalk.red('\nError:'), error.response?.data?.error || error.message);
    }

    await pause();
}

// Display analysis results
function displayAnalysisResults(result) {
    console.log('\n' + chalk.green.bold('═'.repeat(80)));
    console.log(chalk.green.bold('  ANALYSIS RESULTS'));
    console.log(chalk.green.bold('═'.repeat(80)));
    
    console.log(chalk.gray(`\nAnalyzed based on ${result.similar_tickets_count} similar resolved tickets\n`));
    
    console.log(chalk.cyan.bold('TOP 3 RECOMMENDED SOLUTIONS:\n'));

    result.solutions.forEach((solution, index) => {
        const percentage = solution.suitability_percentage;
        let color = chalk.green;
        if (percentage < 50) color = chalk.red;
        else if (percentage < 75) color = chalk.yellow;

        console.log(color.bold(`${solution.rank}. SOLUTION (Suitability: ${percentage}%)`));
        console.log(chalk.white('─'.repeat(80)));
        console.log(chalk.white(`\n${solution.solution}\n`));
        console.log(chalk.gray(`Reasoning: ${solution.reasoning}`));
        
        if (solution.reference_tickets && solution.reference_tickets.length > 0) {
            console.log(chalk.gray(`References: Similar tickets #${solution.reference_tickets.join(', #')}`));
        }
        console.log();
    });

    console.log(chalk.green.bold('═'.repeat(80)));
}

// Search similar tickets
async function searchSimilar() {
    console.log(chalk.yellow('\n🔍 Search Similar Tickets\n'));
    
    const answers = await inquirer.prompt([
        {
            type: 'input',
            name: 'query',
            message: 'Enter search query:',
            validate: (input) => input.length > 0 || 'Query is required'
        },
        {
            type: 'number',
            name: 'top_k',
            message: 'Number of results:',
            default: 5,
            validate: (input) => input > 0 && input <= 20 || 'Must be between 1 and 20'
        }
    ]);

    const spinner = ora('Searching...').start();

    try {
        const response = await axios.post(`${BACKEND_URL}/api/search`, {
            query: answers.query,
            top_k: answers.top_k
        });

        spinner.succeed('Search complete!');

        const results = response.data.results;
        displaySearchResults(results);

    } catch (error) {
        spinner.fail('Search failed');
        console.error(chalk.red('\nError:'), error.response?.data?.error || error.message);
    }

    await pause();
}

// Display search results
function displaySearchResults(results) {
    console.log('\n' + chalk.green.bold('═'.repeat(80)));
    console.log(chalk.green.bold(`  SEARCH RESULTS (${results.length} found)`));
    console.log(chalk.green.bold('═'.repeat(80)) + '\n');

    results.forEach((result, index) => {
        const percentage = Math.round(result.similarity_score * 100);
        console.log(chalk.cyan.bold(`${index + 1}. ${result.subject}`));
        console.log(chalk.yellow(`   Similarity: ${percentage}% | Type: ${result.type} | Priority: ${result.priority}`));
        console.log(chalk.gray(`   ${result.body.substring(0, 150)}...`));
        console.log();
    });
}

// View system stats
async function viewStats() {
    const spinner = ora('Fetching system statistics...').start();

    try {
        const response = await axios.get(`${BACKEND_URL}/api/stats`);
        spinner.succeed('Stats retrieved!');

        const stats = response.data.stats;
        
        console.log('\n' + chalk.green.bold('═'.repeat(80)));
        console.log(chalk.green.bold('  SYSTEM STATISTICS'));
        console.log(chalk.green.bold('═'.repeat(80)) + '\n');
        
        console.log(chalk.cyan('Total Tickets:       ') + chalk.white(stats.total_tickets));
        console.log(chalk.cyan('Embedding Model:     ') + chalk.white(stats.embedding_model));
        console.log(chalk.cyan('LLM Model:           ') + chalk.white(stats.llm_model));
        console.log(chalk.cyan('Embedding Dimension: ') + chalk.white(stats.embedding_dimension));
        console.log();

    } catch (error) {
        spinner.fail('Failed to retrieve stats');
        console.error(chalk.red('\nError:'), error.response?.data?.error || error.message);
    }

    await pause();
}

// Pause and wait for user
async function pause() {
    await inquirer.prompt([
        {
            type: 'input',
            name: 'continue',
            message: 'Press Enter to continue...'
        }
    ]);
}

// Check backend health
async function checkBackend() {
    const spinner = ora('Connecting to backend...').start();
    
    try {
        const response = await axios.get(`${BACKEND_URL}/health`, { timeout: 5000 });
        
        if (response.data.initialized) {
            spinner.succeed(chalk.green('Connected to backend successfully!'));
            return true;
        } else {
            spinner.warn(chalk.yellow('Backend is running but not fully initialized'));
            return false;
        }
    } catch (error) {
        spinner.fail(chalk.red('Cannot connect to backend'));
        console.error(chalk.red('\nError: Backend is not running or not accessible'));
        console.error(chalk.yellow(`\nMake sure the backend is running at: ${BACKEND_URL}`));
        console.error(chalk.yellow('Start the backend with: cd backend && python app.py\n'));
        return false;
    }
}

// Main function
async function main() {
    displayBanner();
    
    const backendOk = await checkBackend();
    
    if (!backendOk) {
        process.exit(1);
    }

    console.log();

    while (true) {
        const action = await mainMenu();

        console.log();

        switch (action) {
            case 'analyze':
                await analyzeTicket();
                break;
            case 'search':
                await searchSimilar();
                break;
            case 'stats':
                await viewStats();
                break;
            case 'exit':
                console.log(chalk.cyan('\n👋 Goodbye!\n'));
                process.exit(0);
        }

        displayBanner();
    }
}

// Run the CLI
main().catch((error) => {
    console.error(chalk.red('Fatal error:'), error);
    process.exit(1);
});
