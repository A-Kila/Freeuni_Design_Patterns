from read_eval import ReadEval

if __name__ == "__main__":
    read_eval: ReadEval = ReadEval()

    while True:
        command: str = input(">>> ")

        if command == "-1":
            break

        read_eval.execute_command(command)
