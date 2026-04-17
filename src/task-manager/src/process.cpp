#include "process.h"
#include <fstream>
#include <dirent.h>
#include <signal.h>
#include <unistd.h>
#include <algorithm>
#include <iomanip>
#include <sstream>
#include <cstring>
#include <cctype>
#include <iostream>

using namespace std;

ProcessManager::ProcessManager() {}

ProcessManager::~ProcessManager() {}

bool ProcessManager::isPidDirectory(const string& dirname) {
    if (dirname.empty()) return false;
    return all_of(dirname.begin(), dirname.end(), ::isdigit);
}

vector<Process> ProcessManager::getAllProcesses() {
    vector<Process> processes;
    DIR* procDir = opendir("/proc");

    if (!procDir) {
        perror("Failed to open /proc");
        return processes;
    }

    struct dirent* entry;
    while ((entry = readdir(procDir)) != NULL) {
        if (isPidDirectory(entry->d_name)) {
            int pid = atoi(entry->d_name);
            try {
                Process p = getProcessById(pid);
                processes.push_back(p);
            } catch (...) {
                // Process may have ended, skip it
            }
        }
    }

    closedir(procDir);
    return processes;
}

Process ProcessManager::getProcessById(int pid) {
    string statPath = "/proc/" + to_string(pid) + "/stat";

    ifstream statFile(statPath);
    if (!statFile.is_open()) {
        throw runtime_error("Cannot open stat file for PID " + to_string(pid));
    }

    Process p;
    p.pid = pid;
    p.state = "S";
    p.threads = 1;
    p.memory_kb = 0;
    p.vsize_kb = 0;
    p.start_time = 0;

    // Read /proc/[pid]/stat
    string line;
    getline(statFile, line);
    statFile.close();

    // Parse stat file carefully - comm field is in parentheses and may contain spaces
    // Format: pid (comm) state ppid pgrp session tty_nr tpgid flags minflt cminflt majflt cmajflt utime stime cutime cstime priority nice num_threads ...
    size_t firstParen = line.find('(');
    size_t lastParen = line.rfind(')');

    if (firstParen != string::npos && lastParen != string::npos && lastParen > firstParen) {
        // Extract command name from parentheses
        p.name = line.substr(firstParen + 1, lastParen - firstParen - 1);

        // Parse remaining fields after closing parenthesis
        string remainder = line.substr(lastParen + 1);
        istringstream iss(remainder);
        string field;
        int fieldNum = 0;

        while (iss >> field && fieldNum < 45) {
            try {
                switch (fieldNum) {
                    case 0:  // state
                        if (!field.empty()) p.state = field[0];
                        break;
                    case 17: // num_threads (Corrected Index)
                        p.threads = stoi(field);
                        break;
                    case 20: // vsize (Corrected Index)
                        p.vsize_kb = stol(field) / 1024;
                        break;
                    case 21: // rss in pages (Corrected Index)
                        p.memory_kb = stol(field) * 4;
                        break;
                }
            } catch (...) {
                // Skip bad conversions
            }
            fieldNum++;
        }
    }

    // Get command line
    p.cmdline = getCommandLine(pid);

    return p;
}

string ProcessManager::getCommandLine(int pid) {
    string cmdlinePath = "/proc/" + to_string(pid) + "/cmdline";
    ifstream cmdFile(cmdlinePath);

    if (!cmdFile.is_open()) {
        return "";
    }

    string cmdline;
    char c;
    while (cmdFile.get(c)) {
        if (c == '\0') {
            cmdline += ' ';  // Replace null terminators with spaces
        } else {
            cmdline += c;
        }
    }

    cmdFile.close();

    // Trim trailing space
    if (!cmdline.empty() && cmdline.back() == ' ') {
        cmdline.pop_back();
    }

    return cmdline;
}

vector<Process> ProcessManager::filterByName(const vector<Process>& processes, const string& name) {
    vector<Process> filtered;
    for (const auto& p : processes) {
        if (p.name.find(name) != string::npos || p.cmdline.find(name) != string::npos) {
            filtered.push_back(p);
        }
    }
    return filtered;
}

bool ProcessManager::killProcess(int pid) {
    if (kill(pid, SIGTERM) == 0) {
        return true;
    }
    return false;
}

void ProcessManager::displayProcesses(const vector<Process>& processes) {
    if (processes.empty()) {
        cout << "No processes found.\n";
        return;
    }

    // Header
    cout << left
         << setw(8) << "PID"
         << setw(25) << "NAME"
         << setw(8) << "STATE"
         << setw(10) << "MEMORY"
         << setw(8) << "THREADS"
         << "\n";

    cout << string(59, '-') << "\n";

    // Rows
    for (const auto& p : processes) {
        cout << left
             << setw(8) << p.pid
             << setw(25) << p.name.substr(0, 24)
             << setw(8) << p.state
             << setw(10) << (to_string(p.memory_kb / 1024) + " MB")
             << setw(8) << p.threads
             << "\n";
    }

    cout << "\nTotal processes: " << processes.size() << "\n";
}
