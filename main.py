import db
import utils
from rich.console import Console
import threading
import asyncio

exit_program = False

def user_input_handler():
    global exit_program
    user_input = input()
    if user_input.lower() == 'q':
        exit_program = True  

async def main():
    db.init_db()
    
    
    utils.print_ascii_art()

    while True:
        action = input("Do you want to (a)dd, (r)emove, (s)wap, (o)rder, (g)raph, (c)hange currency, or (q)uit? ").lower()
        if action == 'a':
            utils.add_items_by_user_input()
        elif action == 'r':
            utils.display_stored_items()
            utils.remove_items_by_user_input()
        elif action == 'o':
            await db.sort_items_by_price()
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
        elif action == 'c':
            currency = int(input("Enter your currency code of choice: "))
            utils.update_currency(currency)
        elif action == 'q':
            break
        else:
            print("Invalid input. Please enter 'a', 'r', 'g', or 'q'.")

    while not exit_program:
        await utils.display_tracked_items()
        print("Enter q to exit the program at any time.")

        input_thread = threading.Thread(target=user_input_handler, daemon=True)
        input_thread.start()
        input_thread.join(timeout=600)
        
        if exit_program:
            break

if __name__ == "__main__":
    asyncio.run(main())

