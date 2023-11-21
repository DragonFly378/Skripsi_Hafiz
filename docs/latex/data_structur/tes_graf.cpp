#include <iostream>

class Node {
public:
    int data;
    Node* prev;
    Node* next;

    Node(int value) {
        data = value;
        prev = nullptr;
        next = nullptr;
    }
};

class DoublyLinkedList {
    private:
        Node* head;
        Node* tail;

    public:
        DoublyLinkedList() {
            head = nullptr;
            tail = nullptr;
        }

        void insertAtFront(int new_data) {
            Node* newNode = new Node(new_data);

            if (head == nullptr) {
                head = newNode;
                tail = newNode;
            } else {
                newNode->next = head;
                head->prev = newNode;
                head = newNode;
            }
        }

        void insertAtEnd(int new_data) {
            Node* newNode = new Node(new_data);

            if (tail == nullptr) {
                head = newNode;
                tail = newNode;
            } else {
                newNode->prev = tail;
                tail->next = newNode;
                tail = newNode;
            }
        }

        // void insertAfter(int value, int afterValue) {
        //     Node* newNode = new Node(value);

        //     Node* current = head;
        //     while (current != nullptr) {
        //         if (current->data == afterValue) {
        //             newNode->prev = current;
        //             newNode->next = current->next;

        //             if (current->next != nullptr) {
        //                 current->next->prev = newNode;
        //             } else {
        //                 tail = newNode;
        //             }

        //             current->next = newNode;
        //             break;
        //         }

        //         current = current->next;
        //     }
        // }

        void display() {
            Node* current = head;

            while (current != nullptr) {
                std::cout << current->data << "...";
                current = current->next;
            }

            std::cout << std::endl;
        }
};

int main() {
    DoublyLinkedList list;

    list.insertAtEnd(10);
    list.insertAtFront(5);
    list.insertAtEnd(15);
    list.insertAtFront(2);
    // list.insertAfter(7, 5); // Insert 7 after 5

    list.display();

    return 0;
}
