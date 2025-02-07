#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_TICKETS     100
#define MAX_NAME_CHARS  75
#define MAX_ISSUE_CHARS 5000

typedef struct {
    int id;
    char author[MAX_NAME_CHARS];
    char issue[MAX_ISSUE_CHARS];
} Ticket;

typedef struct {
    Ticket ticket_queue[MAX_TICKETS];
    int front;
    int rear;
    int count;
} TMS; 

// Initialize the TMS: set front, rear, and count to 0.
void initTMS(TMS *tms) {
    tms->front = 0;
    tms->rear = 0;
    tms->count = 0;
}

// Enqueue: add a ticket at the rear if queue is not full.
int enqueue(TMS *tms, Ticket ticket) {
    if (tms->count >= MAX_TICKETS) {
        printf("Queue is full\n");
        return 0; // Failure
    }
    tms->ticket_queue[tms->rear] = ticket;
    tms->rear = (tms->rear + 1) % MAX_TICKETS;
    tms->count++;
    return 1; // Success
}

Ticket dequeue(TMS *tms) {
    Ticket ticket;
    if (tms->count == 0) {
        printf("Queue is empty\n");
        // Return an 'empty' ticket. Caller must check this.
        ticket.id = -1;
        strcpy(ticket.author, "None");
        strcpy(ticket.issue, "Empty Ticket Queue.");
        return ticket;
    }
    ticket = tms->ticket_queue[tms->front];
    tms->front = (tms->front + 1) % MAX_TICKETS;
    tms->count--;
    return ticket;
}

int main(void) {
    TMS tms;
    initTMS(&tms);

    // Create sample tickets.
    Ticket t1 = {1, "Dave Ottley", "First Ticket"};
    Ticket t2 = {2, "Dave Ottley", "Second Ticket"};

    // Enqueue tickets.
    enqueue(&tms, t1);
    enqueue(&tms, t2);

    // Dequeue one ticket and print its ID.
    Ticket ticket = dequeue(&tms);
    printf("Dequeued Ticket ID: %d\n", ticket.id);

    return 0;
}






