import streamlit as st
st.set_page_config(layout="wide")
a,b = st.columns(2)
with a:
    with st.expander("FCFS"):
        st.code(
            '''
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/shm.h>
#include <sys/ipc.h>
#include <unistd.h>

int n;
int SHMSZ;

struct process {
    int at;  // Arrival time
    int bt;  // Burst time
    int status;  // Status of the process (0 = not finished, 1 = finished)
    int ft;  // Finish time
};

int dispatcher(int time, struct process *ready) {
    int i, arriv = 99, index = -1;
    for (i = 0; i < n; i++) {
        if (ready[i].status != 1 && ready[i].at <= time) {
            if (ready[i].at < arriv) {
                index = i;
                arriv = ready[i].at;
            }
        }
    }
    return index;
}

int main() {
    printf("\t\tFCFS Scheduling\n");
    int arr, bur, ct, tat, wt;
    float avg1 = 0, avg2 = 0, avg3 = 0;
    int i, cur_time, pid;
    int shmid;
    key_t key = 3199;
    
    printf("Enter number of processes: ");
    scanf("%d", &n);
    SHMSZ = (sizeof(struct process) * n);
    struct process *ready;

    shmid = shmget(key, SHMSZ, IPC_CREAT | 0666);
    if (shmid < 0) { perror("shmget"); exit(1); }

    ready = (struct process *)shmat(shmid, NULL, 0);
    if (ready == (struct process *)-1) { perror("shmat"); exit(1); }

    if (fork() > 0) {
        for (i = 0; i < n; i++) {
            printf("\nProcess %d\n", i + 1);
            printf("Enter Arrival Time: ");
            scanf("%d", &ready[i].at);
            printf("Enter Service Time: ");
            scanf("%d", &ready[i].bt);
            ready[i].status = 0;
        }
        wait(NULL);
        shmdt(ready);
    } else {
        sleep(10);
        shmdt(ready);
        ready = (struct process *)shmat(shmid, NULL, 0);
        if (ready == (struct process *)-1) { perror("shmat"); exit(1); }

        i = 0; cur_time = 0;
        printf("\nGantt Chart:\t");
        while (i < n) {
            pid = dispatcher(cur_time, ready);
            if (pid >= 0) {
                ready[pid].ft = cur_time + ready[pid].bt;
                ready[pid].status = 1;
                printf("P%d(%d-%d)\t", (pid + 1), cur_time, ready[pid].ft);
                cur_time = ready[pid].ft;
                i++;
            } else {
                printf("Idle(%d-%d)\t", cur_time, cur_time + 1);
                cur_time++;
            }
        }
        printf("\nProcess\tAT\tBT\tCT\tTAT\tWT\n\n");
        for (i = 0; i < n; i++) {
            arr = ready[i].at;
            bur = ready[i].bt;
            ct = ready[i].ft;
            tat = ct - arr;
            wt = tat - bur;
            avg1 += ct;
            avg2 += tat;
            avg3 += wt;
            printf("%d\t%d\t%d\t%d\t%d\t%d\n", (i + 1), arr, bur, ct, tat, wt);
        }

        avg1 /= n;
        avg2 /= n;
        avg3 /= n;
        printf("Avg:\t\t\t%3.2f\t%3.2f\t%3.2f\n", avg1, avg2, avg3);
        float thr = (float)n / (float)cur_time;
        printf("\nThe THROUGHPUT is: %f\n", thr);

        shmdt(ready);
        shmctl(shmid, IPC_RMID, NULL);
        exit(0);
    }
    return 0;
}
'''
        )
    with st.expander("SJF"):
        st.code(
'''
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/shm.h>
#include <sys/ipc.h>
#include <unistd.h>

int n;
int SHMSZ;

struct process {
    int at;  // Arrival time
    int bt;  // Burst time
    int status;  // Status of the process (0 = not finished, 1 = finished)
    int ft;  // Finish time
};

int dispatcher(int time, struct process *ready) {
    int i, burst = 99, index = -1;
    for (i = 0; i < n; i++) {
        if (ready[i].status != 1 && ready[i].at <= time) {
            if (ready[i].bt < burst) {
                index = i;
                burst = ready[i].bt;
            }
        }
    }
    return index;
}

int main() {
    printf("\t\tSJF Scheduling\n");
    int arr, bur, ct, tat, wt;
    float avg1 = 0, avg2 = 0, avg3 = 0;
    int i, cur_time, pid;
    int shmid;
    key_t key = 3199;
    
    printf("Enter number of processes: ");
    scanf("%d", &n);
    SHMSZ = (sizeof(struct process) * n);
    struct process *ready;

    shmid = shmget(key, SHMSZ, IPC_CREAT | 0666);
    if (shmid < 0) { perror("shmget"); exit(1); }

    ready = (struct process *)shmat(shmid, NULL, 0);
    if (ready == (struct process *)-1) { perror("shmat"); exit(1); }

    if (fork() > 0) {
        for (i = 0; i < n; i++) {
            printf("\nProcess %d\n", i + 1);
            printf("Enter Arrival Time: ");
            scanf("%d", &ready[i].at);
            printf("Enter Service Time: ");
            scanf("%d", &ready[i].bt);
            ready[i].status = 0;
        }
        wait(NULL);
        shmdt(ready);
    } else {
        sleep(10);
        shmdt(ready);
        ready = (struct process *)shmat(shmid, NULL, 0);
        if (ready == (struct process *)-1) { perror("shmat"); exit(1); }

        i = 0; cur_time = 0;
        printf("\nGantt Chart:\t");
        while (i < n) {
            pid = dispatcher(cur_time, ready);
            if (pid >= 0) {
                ready[pid].ft = cur_time + ready[pid].bt;
                ready[pid].status = 1;
                printf("P%d(%d-%d)\t", (pid + 1), cur_time, ready[pid].ft);
                cur_time = ready[pid].ft;
                i++;
            } else {
                printf("Idle(%d-%d)\t", cur_time, cur_time + 1);
                cur_time++;
            }
        }
        printf("\nProcess\tAT\tBT\tCT\tTAT\tWT\n\n");
        for (i = 0; i < n; i++) {
            arr = ready[i].at;
            bur = ready[i].bt;
            ct = ready[i].ft;
            tat = ct - arr;
            wt = tat - bur;
            avg1 += ct;
            avg2 += tat;
            avg3 += wt;
            printf("%d\t%d\t%d\t%d\t%d\t%d\n", (i + 1), arr, bur, ct, tat, wt);
        }

        avg1 /= n;
        avg2 /= n;
        avg3 /= n;
        printf("Avg:\t\t\t%3.2f\t%3.2f\t%3.2f\n", avg1, avg2, avg3);
        float thr = (float)n / (float)cur_time;
        printf("\nThe THROUGHPUT is: %f\n", thr);

        shmdt(ready);
        shmctl(shmid, IPC_RMID, NULL);
        exit(0);
    }
    return 0;
}

'''
        )
    with st.expander("SRTF"):
        st.code(
'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/types.h>
#include <unistd.h>
#include <limits.h>
#include <sys/wait.h>

#define MAX_PROCESSES 100
#define SHM_SIZE sizeof(struct process) * MAX_PROCESSES

struct process {
    char name[5];
    int ar;  // Arrival time
    int ser; // Burst time
};

void print_gantt_chart(struct process *p, int n, int *completion_time) {
    printf("Gantt Chart:\n");
    int time = 0;
    int min_index;
    int min_remaining;
    int remaining_time[MAX_PROCESSES];
    int executed[MAX_PROCESSES] = {0};

    for (int i = 0; i < n; i++) {
        remaining_time[i] = p[i].ser;
    }

    printf("0 ");
    while (1) {
        min_index = -1;
        min_remaining = INT_MAX;
        int all_done = 1;

        for (int i = 0; i < n; i++) {
            if (p[i].ar <= time && remaining_time[i] > 0) {
                all_done = 0;
                if (remaining_time[i] < min_remaining) {
                    min_remaining = remaining_time[i];
                    min_index = i;
                }
            }
        }

        if (min_index == -1) {
            break;
        }

        int exec_time = remaining_time[min_index];
        printf("P%s(%d-%d) ", p[min_index].name, time, time + exec_time);
        time += exec_time;
        remaining_time[min_index] = 0;
        executed[min_index] = 1;

        completion_time[min_index] = time;

        if (all_done) break;
    }
    printf("\n");
}

void calculate_times(struct process *p, int n, int *completion_time, int *turnaround_time, int *waiting_time) {
    int remaining_time[MAX_PROCESSES];
    for (int i = 0; i < n; i++) {
        remaining_time[i] = p[i].ser;
    }

    int time = 0;
    int completed = 0;
    while (completed < n) {
        int min_index = -1;
        int min_remaining = INT_MAX;

        for (int i = 0; i < n; i++) {
            if (p[i].ar <= time && remaining_time[i] > 0 && remaining_time[i] < min_remaining) {
                min_remaining = remaining_time[i];
                min_index = i;
            }
        }

        if (min_index == -1) {
            time++;
            continue;
        }

        remaining_time[min_index]--;
        time++;

        if (remaining_time[min_index] == 0) {
            completion_time[min_index] = time;
            turnaround_time[min_index] = completion_time[min_index] - p[min_index].ar;
            waiting_time[min_index] = turnaround_time[min_index] - p[min_index].ser;
            completed++;
        }
    }
}

void print_times(struct process *p, int n, int *completion_time, int *turnaround_time, int *waiting_time) {
    printf("\nProcess\tArrival\tBurst\tCompletion\tTurnaround\tWaiting\n");
    for (int i = 0; i < n; i++) {
        printf("%s\t%d\t%d\t%d\t\t%d\t\t%d\n", p[i].name, p[i].ar, p[i].ser,
               completion_time[i], turnaround_time[i], waiting_time[i]);
    }
}

int main() {
    int shmid;
    struct process *p;
    struct process *shared_memory;
    int n;
    pid_t pid;

    key_t key = 1234;
    shmid = shmget(key, SHM_SIZE, 0666 | IPC_CREAT);
    if (shmid < 0) {
        perror("shmget failed");
        exit(1);
    }

    shared_memory = (struct process *)shmat(shmid, NULL, 0);
    if (shared_memory == (struct process *)-1) {
        perror("shmat failed");
        exit(1);
    }

    printf("Enter number of processes: ");
    scanf("%d", &n);

    p = shared_memory;
    for (int i = 0; i < n; i++) {
        printf("Enter process name, arrival time, and burst time for process %d:\n", i + 1);
        scanf("%s %d %d", p[i].name, &p[i].ar, &p[i].ser);
    }

    pid = fork();
    if (pid < 0) {
        perror("fork failed");
        exit(1);
    }

    if (pid == 0) {
        struct process *p = shared_memory;
        int completion_time[MAX_PROCESSES];
        int turnaround_time[MAX_PROCESSES];
        int waiting_time[MAX_PROCESSES];

        calculate_times(p, n, completion_time, turnaround_time, waiting_time);
        print_gantt_chart(p, n, completion_time);
        print_times(p, n, completion_time, turnaround_time, waiting_time);

        shmdt(shared_memory);
        shmctl(shmid, IPC_RMID, NULL);
    } else {
        wait(NULL);
    }

    return 0;
}
'''
        )

with b:
    with st.expander("PIPE"):
        st.code(
            '''
#include <stdio.h>
#include <unistd.h>
#include <string.h>

int main() {
    int pipefd[2];
    pid_t pid;
    char write_msg[] = "Hello from parent!";
    char read_msg[100];

    // Create a pipe
    if (pipe(pipefd) == -1) {
        perror("pipe failed");
        return 1;
    }

    // Create a child process
    pid = fork();

    if (pid < 0) {
        perror("fork failed");
        return 1;
    }

    if (pid > 0) { 
        // Parent process
        close(pipefd[0]); // Close unused read end
        write(pipefd[1], write_msg, strlen(write_msg) + 1); // Write to pipe
        close(pipefd[1]); // Close write end after writing
    } else { 
        // Child process
        close(pipefd[1]); // Close unused write end
        read(pipefd[0], read_msg, sizeof(read_msg)); // Read from pipe
        printf("Child received: %s\n", read_msg);
        close(pipefd[0]); // Close read end after reading
    }

    return 0;
}

'''
        )
    with st.expander("SHM"):
        st.code(
            '''
#include <stdio.h>
#include <stdlib.h>
#include <sys/shm.h>
#include <sys/ipc.h>
#include <string.h>
#include <unistd.h>

int main() {
    // Generate a unique key for shared memory
    key_t key = ftok("shmfile", 65);

    // Create a shared memory segment
    int shmid = shmget(key, 1024, 0666 | IPC_CREAT);

    // Fork to create sender and receiver processes
    pid_t pid = fork();

    if (pid < 0) {
        perror("fork failed");
        return 1;
    }

    if (pid > 0) { // Parent Process (Sender)
        // Attach to the shared memory segment
        char *str = (char *) shmat(shmid, NULL, 0);

        // Write a message into the shared memory
        strcpy(str, "Hello from Sender!");

        // Detach from the shared memory
        shmdt(str);

        // Wait for the child process (Receiver) to complete
        wait(NULL);

        // Destroy the shared memory segment
        shmctl(shmid, IPC_RMID, NULL);
    } else { // Child Process (Receiver)
        sleep(1); // Ensure sender runs first

        // Attach to the shared memory segment
        char *str = (char *) shmat(shmid, NULL, 0);

        // Read the message from shared memory and display it
        printf("Receiver received: %s\n", str);

        // Detach from the shared memory
        shmdt(str);
    }

    return 0;
}
'''
        )
