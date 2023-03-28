import db
import utils
from rich.console import Console
import threading

exit_program = False

def user_input_handler():
    global exit_program
    user_input = input()
    if user_input.lower() == 'q':
        exit_program = True  

if __name__ == "__main__":
    db.init_db()
    console = Console()
    utils.print_ascii_art()

    while True:
        action = input("Do you want to (a)dd, (r)emove, (s)wap, (g)raph, or (q)uit? ").lower()
        if action == 'a':
            utils.add_items_by_user_input()
        elif action == 'r':
            utils.remove_items_by_user_input()
        elif action == 'g':
            utils.display_stored_items()
            index_str = input("Enter the index of the item you want to graph (or 'q' to quit): ")
            if index_str.lower() == 'q':
                continue
            else:
                try:
                    index = int(index_str)
                    item = utils.get_item_by_index(index)
                    if item is not None:
                        name, _ = item
                        utils.plot_item_price_graph(name)
                    else:
                        print(f"Invalid index. Please enter a valid index.")
                except ValueError:
                    print("Invalid input. Please enter a valid index or 'q' to quit.")
        elif action == 's':
            utils.display_stored_items()
            index1 = int(input("Enter the index of the first item: "))
            index2 = int(input("Enter the index of the second item: "))
            db.swap_items(index1, index2)
        elif action == 'q':
            break
        else:
            print("Invalid input. Please enter 'a', 'r', 'g', or 'q'.")

    while not exit_program:
        utils.display_tracked_items()
        print("Enter q to exit the program at any time.")

        input_thread = threading.Thread(target=user_input_handler, daemon=True)
        input_thread.start()
        input_thread.join(timeout=600)

        if exit_program:
            break