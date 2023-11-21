#include <iostream>
using namespace std;

class Node {
    public:
        int data;
        Node* next;
        Node* prev;

        Node(int value){
            this->data = value;
            this->prev = nullptr;
            this->next = nullptr;
        }
};

class doublyLinkedList{
    private:
        Node* head;
        Node* tail;
    public:
        doublyLinkedList() {
            head = nullptr;
            tail = nullptr;
        }

        void addFront(int new_data){
            Node* newNode = new Node(new_data);

            if(head == nullptr){
                head = newNode;
                tail = newNode;
            } else{
                newNode->next = head;
                head->prev    = newNode;
                head          = newNode;
            }
        }

        void addEnd(int new_data){
            Node* newNode = new Node(new_data);

            if(tail == nullptr){
                head = newNode;
                tail = newNode;
            } else{
                newNode->prev = tail;
                tail->next    = newNode;
                tail          = newNode;
            }
        }

        void addAfter(int data, int after_data) {
            Node* newNode = new Node(data);

            Node* current = head;
            while (current != nullptr) {
                if (current->data == afterValue) {
                    newNode->prev = current;
                    newNode->next = current->next;

                    if (current->next != nullptr) {
                        current->next->prev = newNode;
                    } else {
                        tail = newNode;
                    }

                    current->next = newNode;
                    break;
                }

                current = current->next;
            }
        }

        void display() {
            Node* current = head;

            while (current != nullptr) {
                cout << current->data << "<==>";
                current = current->next;
            }   
            // if(current == Null){
            //     cout<<"Null";
            // }

            cout << endl;
        }

};

int main() {
    doublyLinkedList list;

    list.addFront(10);
    list.addFront(5);
    list.addEnd(15);
    // list.addFront(2);
    // list.insertAfter(7, 5); // Insert 7 after 5

    list.display();

    return 0;
}