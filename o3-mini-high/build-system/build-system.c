#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_ELEMENTS    100

// The graph is stored as an adjacency list
typedef struct {

} Graph;

// Stored as a fixed-length circular buffer
typedef struct {
  int elements[MAX_ELEMENTS];
  int front;
  int rear;
  int count;
} Queue;

// Initialize the Queue. Set front, rear and count to 0
// No need to initialize elements. Will be managed with pointers
void initQueue(Queue *q) {
  q->front = 0;
  q->rear = 0;
  q->count = 0;
}

// Add an element to the end of the queue
// O(1) time
int enqueue(Queue * q, int element) {
  if (q->count >= MAX_ELEMENTS) {
    printf("Queue is full\n");
    return 0; // Failure
  }
  q->elements[q.rear] = element;
  q->rear = (q->rear + 1) % MAX_ELEMENTS;
  q->count++;
  return 1; // Success
}

// Remove an element from the front of the queue
// O(1) time
int dequeue(Queue *q) {
  int element;
  if (q->count == 0) {
    printf("Queue is empty\n");
    // Return an 'empty' element. Caller must check this.
    element = -1;
    return element;
  }
  element = q->elements[q->front];
  q->front = (q->front + 1) % MAX_TICKETS;
  q->count--;
  return element;
}

// Returns true if and only if q has no elements
int is_empty(Queue *q) {
  return count == 0;
}

// Topologically sort the given graph according to Kahn's algorithm
// Returns a pointer to an array of ints representing the sorted
// order of the elements.
int * topo_sort_kahn(Graph * g, int * size) {

}

// Initialize the following simple graph
// Apply topological sort to the graph returning a sorted array
// of ints. Then loop through the ints and print them prettily
int main(void) {
  Graph graph;
  int size;
  
  int *order = topo_sort_kahn(&graph, &size);

  // %d is for integers.
  printf("Topologically sorted order: ");
  for (int i = 0; i < size; i++) {
    printf("%d ", order[i]);
  }
  printf("\n");
  return 0;
}
