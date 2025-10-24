// generate rotation Gray codes for stamp foldings and semi-meanders
// https://doi.org/10.1007/978-3-031-34347-6_23

#include <stdio.h>
#include <stdlib.h>
#define MAX 100

int N, q[MAX], total = 0, type;

struct linked_list {
    int element;
    struct linked_list *prev;
    struct linked_list *next;
};

//--------------------------------------------------
struct linked_list* Rotate(struct linked_list *p, int k, int d) {
    if (d)
        for (int i=0; i<k%N; i++) p = p->prev;
    else
        for (int i=0; i<k%N; i++) p = p->next;
    
    return p;
}

//--------------------------------------------------
int IndexOf(int e, struct linked_list *p) {
    for (int i=1; i<=N; i++) {
        if (p->element==e) return i;
        p = p->next;
    }
    return 1;
}

//--------------------------------------------------
int NextSemiMeander(struct linked_list* p, int t, int d) {
    int j;
    
    if (d) j = p->element;
    else j = p->prev->element;
    
    if (j==1 && !(t%2)) return 1;
    else if (j%2==t%2) {
        if (d) return IndexOf(j+1, p);
        else return t - IndexOf(j+1, p) + 1;
    }
    else {
        if (d) return IndexOf(j-1, p);
        else return t - IndexOf(j-1, p) + 1;
    }
}


//--------------------------------------------------
void Print(struct linked_list *p) {
    for (int i=0; i<N; i++) {
        printf("%d ", p->element);
        p = p->next;
    }
    printf("\n");   total += 1;
}

//--------------------------------------------------
void Gen(struct linked_list *p, int t) {
    int i=1, j=0;
    
    while (i<=t) {
        if (t>=N) Print(p);
        else {
            struct linked_list *r = NULL;
            r = (struct linked_list*)malloc(sizeof(struct linked_list));
            r->element = t+1;
            r->next = p;    r->prev = p->prev;
            r->next->prev = r;  r->prev->next = r;

            if (q[t+1]) Gen(p, t+1);
            else Gen(r, t+1);
            
            q[t+1] = !q[t+1];
            p->prev = r->prev;  p->prev->next = p;
        }
        
        if (type==1 && t>=N) j = 1; // generate stamp foldings
        else j = NextSemiMeander(p, t, q[t]);
        p = Rotate(p, j, !q[t]);
        i = i + j;
    }
}

//--------------------------------------------------
int main() {
    printf("ENTER n: "); scanf("%d", &N);
    printf("Enter selection # (1. Stamp foldings, 2. Semi-meanders): ");
    scanf("%d", &type);

    for (int i=0; i<=N; i++) q[i] = 1;
    
    struct linked_list *p = NULL;
    p = (struct linked_list*)malloc(sizeof(struct linked_list));
    p->element = 1;
    p->prev = p;    p->next = p;

    Gen(p, 1);
    printf("\nTotal: %d", total);
}