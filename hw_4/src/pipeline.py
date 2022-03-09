import codecs
import time
from datetime import datetime
from multiprocessing import Process, Queue, Pipe
from multiprocessing.connection import Connection


def worker_a(in_queue: Queue, out_pipe: Connection):
    while True:
        msg: str = in_queue.get()
        time.sleep(5)
        out_pipe.send(msg.lower())


def worker_b(in_pipe: Connection, out_pipe: Connection):
    while True:
        out_pipe.send(codecs.encode(in_pipe.recv(), "rot_13"))


def get_current_time() -> str:
    return datetime.now().strftime("%H:%M:%S")


if __name__ == "__main__":
    a_to_b, b_from_a = Pipe()
    b_to_main, main_from_b = Pipe()
    main_to_a = Queue()
    Process(target=worker_a, args=(main_to_a, a_to_b), daemon=True).start()
    Process(target=worker_b, args=(b_from_a, b_to_main), daemon=True).start()

    log_messages = []
    while True:
        message = input(">>> ")
        if message == 'quit':
            log_messages.append(f'Exit on {get_current_time()}\n')
            break
        log_messages.append(f'Receive "{message}" on {get_current_time()}\n')
        main_to_a.put(message)
        message = main_from_b.recv()
        log_messages.append(f'Processed "{message}" on {get_current_time()}\n')
        print(message)
    with open("../artifacts/hard.txt", "w") as f:
        for log_message in log_messages:
            f.write(log_message)
