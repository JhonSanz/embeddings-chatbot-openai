import json


class LocalMemory:
    def format_memory(self, memory: list):
        return ", ".join(memory)

    def set_memory(self, question: str) -> None:
        memory = []
        try:
            with open("memory.json", "r") as f:
                memory = json.load(f)
        except FileNotFoundError:
            pass

        memory.append(question)
        with open("memory.json", "w") as f:
            json.dump(memory, f)

    def get_memory(self) -> str:
        memory = []
        try:
            with open("memory.json", "r") as f:
                memory = json.load(f)
        except FileNotFoundError:
            pass

        return self.format_memory(memory)
