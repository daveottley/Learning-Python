/*
TMS.enqueue():
    when receiving a ticket from customer:
    place at rear of queue

TMS.dequeue():
    when free:
    process ticket at front of queue

--> ChatGPT o3-mini-high suggested changes below <--

TMS.initialize():
    Create an empty queue Q

TMS.enqueue(ticket):
    Append ticket to the rear of Q

TMS.dequeue():
    If Q is empty:
        Return an error or message "No tickets to process"
    Else:
        ticket = Remove ticket from the front of Q
        Process the ticket
        Return ticket

Insight: 
* I don't need to write conditions inside functions in pseudocode.
The calling function will decide when to call.
* I need to include parameters in psuedocode
* Conditionals, returns, and assignments can draw from Python syntax


from collections import deque

front_index = (front_index + 1) % MAX_SIZE;
class TMS():
    # Set supplied ticket_queue to member variable.
    # This allows multiple TMSs to be produced, as needed.
    def __init__(self, ticket_queue=None):
        if ticket_queue is not None:
            self.__ticket_queue = ticket_queue
        else:
            self.__ticket_queue = deque()
    
    # Add a ticket to the rear of the queue
    def add(self, ticket):
        self.__ticket_queue.append(ticket)
        return True

    # Remove the longest-waiting ticket from the front of the queue
    def take_ticket(self):
        if len(self.__ticket_queue) > 0:
            ticket = self.__ticket_queue.popleft()
            try:
                ticket.process()
            except Exception as e:
                print("An error occured while processing your ticket:", e)
            return ticket
        else: # No tickets to process
            print("No tickets to process")
            return None


Custom circular buffer (C-style)
Conceptual
---
I will create a fixed sized list (array) of MAX_SIZE
When the queue is empty it should return None
When the queue is full it should throw an error when add()ing
I don't understand circular buffers or tracking front or rear indices
so I will need some guidance here.

Pseudocode
---
Initialize TMS
    * Create a fixed size list (array) of MAX_SIZE
    * Set front_index, rear_index, count = 0

Enqueue
    * Check for a full queue
    * Insert the element at rear
    * Update rear index to be rear = (rear + 1) % MAX_SIZE
    * Incremement the count

Dequeue
    * Check for empty queue
    * Remove element at front
    * Update front index
    * Decrement the count

MAX_SIZE = 100

class TMS():
    def __init__(self, ticket_queue=None):
        if ticket_queue is not None:
            self.__ticket_queue = ticket_queue
        else:
            self.__ticket_queue = [None] * MAX_SIZE
        self.front_index = self.rear_index = self.count = 0
    
    def enqueue(self, ticket):
        if self.count >= MAX_SIZE: # Full queue
            print("Error: The Ticket Manaegment System is full. Cannot add ticket.")
            return False
        else: # We still have space
            try:
                self.__ticket_queue[self.rear_index] =  ticket
                self.rear_index = (self.rear_index + 1) % MAX_SIZE
                self.count += 1
                return True
            except Exception as e:
                print("Error: Could not add your ticket to the Ticket Management System: ", e)
                return False

    def dequeue(self):
        if self.count == 0: # Queue not empty 
            try:
                ticket = self.__ticket_queue[self.front_index]
                #self.__ticket_queue[self.front_index] = None # Optional: clear the slot
                self.front_index = (self.front_index + 1) % MAX_SIZE
                self.count -= 1
                return ticket
            except Exception as e:
                print("Error: Could not remove a ticket from the Ticket Management System: ", e)
                return None 
        else: # Empty queue
            print("Error: There are no tickets in the Ticket Management System to remove.")
            return None
*/

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






