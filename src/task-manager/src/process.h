#ifndef PROCESS_H
#define PROCESS_H

#include <string>
#include <vector>

using namespace std;

struct Process {
    int pid;
    string name;
    string state;           // R, S, D, Z, T
    int threads;
    long memory_kb;         // RSS memory
    long vsize_kb;          // Virtual memory
    long start_time;
    string cmdline;
};

class ProcessManager {
public:
    ProcessManager();
    ~ProcessManager();

    // Get all processes from /proc
    vector<Process> getAllProcesses();

    // Get single process
    Process getProcessById(int pid);

    // Filter processes by name
    vector<Process> filterByName(const vector<Process>& processes, const string& name);

    // Kill process by PID (requires confirmation in main)
    bool killProcess(int pid);

    // Display processes in table format
    void displayProcesses(const vector<Process>& processes);

private:
    // Parse /proc/[pid]/stat file
    Process parseProcessStat(int pid, const string& statFile);

    // Get command line from /proc/[pid]/cmdline
    string getCommandLine(int pid);

    // Check if directory is a PID (contains only digits)
    bool isPidDirectory(const string& dirname);
};

#endif // PROCESS_H
