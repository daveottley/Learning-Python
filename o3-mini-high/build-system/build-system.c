#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_ELEMENTS    100

/* Node represents an adjacent vertex */
typedef struct Node {
  int vertex;
  struct Node *next;
} Node;

/* The graph is stored as an adjacency list */
typedef struct {
  int numVertices;
  Node **adjLists;
} Graph;

/* Create an orphan node with no next pointer */
Node * createNode(int v) {
  Node *newNode = malloc(sizeof(Node));
  if  (!newNode) {
    fprintf(stderr, "Memory allocation failed\n");
    exit(EXIT_FAILURE);
  }
  newNode->vertex = v;
  newNode->next = NULL;
  return newNode;
}

/* Create a graph with 'vertices' NULL vertices */
Graph *createGraph(int vertices) {
  Graph *graph = malloc(sizeof(Graph));
  if (!graph) {
    fprintf(stderr, "Memory allocation failed\n");
    exit(EXIT_FAILURE);
  }
  graph->numVertices = vertices; // Set number of vertices
  graph->adjLists = malloc(vertices * sizeof(Node *));
  if (!graph->adjLists) {
    fprintf(stderr, "Memory allocation failed\n");
    exit(EXIT_FAILURE);
  }
  for (int i = 0; i < vertices; i++)
    graph->adjLists[i] = NULL;
  return graph;
}

/* Add an edge from src to dest. For undirected graphs, add both ways */
void addEdge(Graph *graph, int src, int dest) {
  Node *node = createNode(dest);
  node->next = graph->adjLists[src];
  graph->adjLists[src] = node;

  /* Uncomment the following for an undirected graph
  node = createNode(src);
  node->next = graph->adjLists[dest];
  graph->adjLists[dest] = node;
  */
}

void printGraph(Graph *graph) {
  for (int v = 0; v < graph->numVertices; v++) {
    Node *temp = graph->adjLists[v];
    printf("Vertex %d:", v);
    while (temp) {
      printf(" -> %d", temp->vertex);
      temp = temp->next;
    }
    printf("\n");
  }
}

/* Stored as a fixed-length circular buffer */
typedef struct {
  Node * elements[MAX_ELEMENTS];
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

/* Add an element to the end of the queue in O(1) time */
int enqueue(Queue * q, Node * element) {
  if (q->count >= MAX_ELEMENTS) {
    printf("Queue is full\n");
    return 0; // Failure
  }
  q->elements[q->rear] = element;
  q->rear = (q->rear + 1) % MAX_ELEMENTS;
  q->count++;
  return 1; // Success
}

/* Remove an element from the front of the queue in O(1) time */
Node * dequeue(Queue *q) {
  if (q->count == 0) {
    printf("Queue is empty\n");
    // Return an NULL element. Caller must check this.
    return NULL;
  }
  Node * element = q->elements[q->front];
  q->front = (q->front + 1) % MAX_ELEMENTS;
  q->count--;
  return element;
}

/* Returns true if and only if q has no elements */
int is_empty(Queue *q) {
  return q->count == 0;
}

// Topologically sort the given graph according to Kahn's algorithm
// Returns a pointer to an array of ints representing the sorted
// order of the elements.
int * topo_sort_kahn(Graph * g) {
  //  Create and initialize to 0 an array for storing in-degrees
  int in_degree[g->numVertices];
  for (int i = 0; i < g->numVertices; i++) {
    in_degree[i] = 0;
  }

  // Add one to the in-degree of each node in each adjList 
  for (int i = 0; i < g->numVertices; i++) {
    Node *temp = g->adjLists[i];
    while (temp) {
      in_degree[temp->vertex]++;
      temp = temp->next;
    }
  }
  
  // Create a Queue to start popping nodes onto our ordering list
  Queue q;
  initQueue(&q);
  for (int i = 0; i < g->numVertices; i++) {
    if (in_degree[i] == 0) {
      Node * temp = malloc(sizeof(Node));
      temp->vertex = i;
      temp->next = NULL;
      enqueue(&q, temp);
    }
  }
  
  // Create an int array to return
  int * ordering =  malloc(g->numVertices * sizeof(int));

  // Pop each element from the Queue and add it to ordering
  // Reduce the in_degree of all vertexes adjacent to that 
  // vertex by 1 and if it is 0 add it to the Queue.
  for (int i = 0; !is_empty(&q); i++) {
    // Dequeue the node
    Node * element = dequeue(&q);
    // Store vertex value
    int u = element->vertex;
    // Free the node after extracting u
    free(element);

    // Creat temp variable for traversing the adjacency list
    Node * adj = g->adjLists[u];
    // Set the vertex in the sorted output list
    ordering[i] = u;
    while (adj) {
      int v = adj->vertex;
      in_degree[v]--;
      if (in_degree[v] == 0) {
        Node * newNode = malloc(sizeof(Node));
        newNode->vertex = v;
        newNode->next = NULL;
        enqueue(&q, newNode);
      }
      adj = adj->next;
    }
  }

  return ordering;
}

// Initialize the following simple graph
// Apply topological sort to the graph returning a sorted array
// of ints. Then loop through the ints and print them prettily
int main(void) {
  int vertices = 5;
  Graph *graph = createGraph(vertices);
  
  addEdge(graph, 0, 1);
  addEdge(graph, 0, 4);
  addEdge(graph, 1, 2);
  addEdge(graph, 1, 3);
  addEdge(graph, 1, 4);
  addEdge(graph, 2, 3);
  addEdge(graph, 3, 4);

  int *order = topo_sort_kahn(graph);

  // Print the raw graph
  printGraph(graph);
  
  // Print topologically sorted list of the graph
  printf("Topologically sorted order: ");
  for (int i = 0; i < vertices; i++) {
    printf("%d ", order[i]);
  }
  printf("\n");
  return 0;
}
