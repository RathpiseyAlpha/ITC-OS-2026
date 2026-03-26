// ─── Site Configuration ───
// Edit these values to match your repository and services.

const CONFIG = {
    // GitHub repository (used to dynamically fetch file tree)
    github: {
        owner: 'RathpiseyAlpha',
        repo: 'ITC-OS-2026',
        branch: 'main',
        // Set to a GitHub personal access token for higher rate limits (5000/hr vs 60/hr)
        // Leave empty to use unauthenticated requests
        token: ''
    },

    // Presence server (tracks logged-in Linux users on the server)
    // Run `python3 app/server/app.py` on your Linux server, then set the URL below.
    // See app/server/README.md for setup instructions (systemd, nginx, etc.)
    server: {
        url: '',            // e.g. 'https://your-server.example.com' or 'http://server-ip:5000'
        pollInterval: 10000 // poll /api/users every 10 seconds
    },

    // Firebase Realtime Database (for web visitor presence tracking)
    // Create a free project at https://console.firebase.google.com
    // 1. Create a new project → Add a Realtime Database
    // 2. Set database rules:
    //    { "rules": { "presence": { ".read": true, ".write": true } } }
    // 3. Copy your config values below and set enabled: true
    firebase: {
        enabled: false,
        apiKey: '',
        authDomain: '',
        databaseURL: '',
        projectId: ''
    },

    // Course info (displayed in UI)
    course: {
        title: 'ITC Operating Systems 2026',
        code: 'SE-019',
        institution: 'Institute of Technology of Cambodia',
        department: 'Department of Information and Communication Engineering',
        instructor: 'Heng Rathpisey',
        repoUrl: 'https://github.com/RathpiseyAlpha/ITC-OS-2026'
    },

    // Lecture schedule mapping: week number → { file, title }
    // Used by sidebar to show schedule with status indicators
    schedule: [
        { week: 1,  file: 'lectures/files/ch1.pdf',  title: 'Intro to OS' },
        { week: 2,  file: 'lectures/files/ch2.pdf',  title: 'OS Structures' },
        { week: 3,  file: 'lectures/files/ch3.pdf',  title: 'Processes' },
        { week: 4,  file: 'lectures/files/ch4.pdf',  title: 'Threads' },
        { week: 5,  file: 'lectures/files/ch5.pdf',  title: 'CPU Scheduling I' },
        { week: 6,  file: 'lectures/files/ch6.pdf',  title: 'CPU Scheduling II' },
        { week: 7,  file: 'lectures/files/ch7.pdf',  title: 'Critical Sections' },
        { week: 8,  file: 'lectures/files/ch8.pdf',  title: 'Semaphores' },
        { week: 9,  file: 'lectures/files/ch9.pdf',  title: 'Deadlocks' },
        { week: 10, file: 'lectures/files/ch10.pdf', title: 'Memory Mgmt' },
        { week: 11, file: 'lectures/files/ch11.pdf', title: 'Virtual Memory' },
        { week: 12, file: 'lectures/files/ch12.pdf', title: 'File Systems' }
    ],

    // Cache duration for GitHub API responses (ms)
    cacheDuration: 5 * 60 * 1000 // 5 minutes
};
