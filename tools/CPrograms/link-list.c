#include <stdio.h>
#include <stdlib.h>

#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

struct node {
	int no;
	struct node *next;
};

struct node *new_node(int no)
{
	struct node *n = malloc(sizeof(*n));

	if (!n) {
		fprintf(stderr, "Memory allocation failed.\n");
		return NULL;
	}

	n->no = no;
	n->next = NULL;
	return n;
}

/*
 * we are not returning anything from this function, let's check if this
 * error is detected by various tools.
 */
int add_node(struct node **head, struct node *n)
{
	struct node *t;
	if (*head == NULL) {
		*head = n;
	} else {
		n->next = *head;
		(*head)= n;
	}
}

void print_list(struct node *head)
{
	struct node *n = head;

	while (n) {
		printf("%d\n", n->no);
		n = n->next;
	}
}

int main(int argc, char *argv[])
{
	struct node *n;
	struct node *head;
	int i;
	int no;
	int fd;

	head = NULL;
	for (no = 0; no < 10; no++) {
		n = new_node(no);
		add_node(&head, n);
	}

	print_list(head);
	free(head);

	open(argv[0], O_RDONLY);
	open(argv[0], O_RDONLY);
	return 0;
}
