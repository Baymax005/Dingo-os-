#include "process.h"
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <cstdlib>
#include <cstring>

using namespace std;

void printUsage(const char* programName) {
    cout << "Usage: " << programName << " [OPTIONS]\n";
    cout << "  --list              List all processes\n";
    cout << "  --filter <name>     Filter by process name\n";
    cout << "  --sort <field>      Sort by field (pid, name, memory)\n";
    cout << "  --kill <pid>        Kill process by PID\n";
    cout << "  --help              Show this message\n";
    cout << "  (no args)           Interactive mode (list all)\n";
}

int main(int argc, char* argv[]) {
    ProcessManager pm;

    if (argc == 1 || (argc > 1 && string(argv[1]) == "--list")) {
        // Default: list all processes
        vector<Process> processes = pm.getAllProcesses();
        pm.displayProcesses(processes);
        return 0;
    }

    if (argc > 1 && string(argv[1]) == "--filter" && argc > 2) {
        string filterName = argv[2];
        vector<Process> processes = pm.getAllProcesses();
        vector<Process> filtered = pm.filterByName(processes, filterName);
        pm.displayProcesses(filtered);
        return 0;
    }

    if (argc > 1 && string(argv[1]) == "--kill" && argc > 2) {
        int pid = atoi(argv[2]);
        cout << "Kill process " << pid << "? (y/n): ";
        char response;
        cin >> response;
        if (response == 'y' || response == 'Y') {
            if (pm.killProcess(pid)) {
                cout << "Process " << pid << " killed successfully.\n";
            } else {
                cerr << "Failed to kill process " << pid << "\n";
                return 1;
            }
        } else {
            cout << "Cancelled.\n";
        }
        return 0;
    }

    if (argc > 1 && string(argv[1]) == "--help") {
        printUsage(argv[0]);
        return 0;
    }

    // Default behavior: show all processes
    vector<Process> processes = pm.getAllProcesses();
    pm.displayProcesses(processes);

    return 0;
}
