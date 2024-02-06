from tkinter import Tk, Button, Entry, Label

def submit_name(entry):
    name = entry.get()
    print(name)
    return name

def getCategory(root):
    label = Label(root, text="Enter the wound category (e.g., luka_merah)")
    label.pack()

    entry = Entry(root)
    entry.pack()

    button = Button(root, text="Submit", command=lambda: root.quit())
    button.pack()

    root.mainloop()  # Wait for the user to enter the category
    return submit_name(entry)

def main():
    root = Tk()
    root.title("Text Input Example")

    category_name = getCategory(root)
    print("The category name entered was:", category_name)

if __name__ == "__main__":
    main()
