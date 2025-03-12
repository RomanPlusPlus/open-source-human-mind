import re
import os
import random


LIFE_PERIODS_ORDER = [
    "kindergarten",
    "kindergarten_or_school",
    "school",
    "school_or_uni",
    "uni",
    "uni_or_emigration_prep",
    "emigration_prep",
    "integration_into_Germany",
    "first_startup",
    "second_startup",
    "ai_dev_work",
]


# Define a class to hold personal memories
class PersonalMemory:
    def __init__(self, life_period, location, people, memory_text):
        self.life_period = life_period
        self.location = location
        self.people = people
        self.memory_text = memory_text

    def __repr__(self):
        return (
            f"PersonalMemory(life_period='{self.life_period}', "
            f"location='{self.location}', people='{self.people}', "
            f"memory_text='{self.memory_text}')"
        )


# Function to parse the structured memories file
def parse_memories(file_path):
    memories = []

    # Check if the file exists before attempting to open it
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Error: File not found at '{file_path}'. Please check the file path.")
        return memories

    life_period_pattern = re.compile(
        r'<life_period="(.*?)">(.*?)<\/life_period="\1">', re.DOTALL
    )
    location_pattern = re.compile(
        r'<location="(.*?)">(.*?)<\/location="\1">', re.DOTALL
    )
    people_pattern = re.compile(r'<people="(.*?)">(.*?)<\/people="\1">', re.DOTALL)
    memory_item_pattern = re.compile(r"- (.*?)\n")

    for life_period_match in life_period_pattern.finditer(content):
        life_period, life_period_content = life_period_match.groups()

        for location_match in location_pattern.finditer(life_period_content):
            location = location_match.group(1)
            location_content = location_match.group(2)

            for people_match in people_pattern.finditer(location_content):
                people = people_match.group(1)
                people_content = people_match.group(2)

                for memory_match in memory_item_pattern.finditer(people_content):
                    memory_text = memory_match.group(1).strip()
                    memories.append(
                        PersonalMemory(life_period, location, people, memory_text)
                    )

    return memories


# Function to serialize memories back to structured format
def serialize_memories(memories):
    structured_data = ""
    memory_dict = {}

    # Organize memories into nested dictionaries
    for mem in memories:
        memory_dict.setdefault(mem.life_period, {}).setdefault(
            mem.location, {}
        ).setdefault(mem.people, []).append(mem.memory_text)

    # Serialize nested dictionaries into structured format sorted by LIFE_PERIODS_ORDER
    for life_period in LIFE_PERIODS_ORDER:
        if life_period in memory_dict:
            structured_data += f'<life_period="{life_period}">\n'
            locations = memory_dict[life_period]
            for location, people_groups in locations.items():
                structured_data += f'  <location="{location}">\n'
                for people, memory_texts in people_groups.items():
                    structured_data += f'    <people="{people}">\n'
                    for memory_text in memory_texts:
                        structured_data += f"      - {memory_text}\n"
                    structured_data += f'    </people="{people}">\n'
                structured_data += f'  </location="{location}">\n'
            structured_data += f'</life_period="{life_period}">\n'

    return structured_data


# Function to reduce memories randomly until the target size is reached
def reduce_memories_to_target_size(memories, target_size_kb):
    # Shuffle memories randomly
    random.shuffle(memories)

    # Iteratively remove memories until target size is reached
    while True:
        serialized_data = serialize_memories(memories)
        current_size_kb = len(serialized_data.encode("utf-8")) / 1024

        if current_size_kb <= target_size_kb or len(memories) == 0:
            break

        # Remove one memory at a time
        memories.pop()

    return memories


# Example usage:
if __name__ == "__main__":
    file_path = "../full_dataset/structured_memories.txt"
    target_size_kb = 415  # Set your desired target size here

    filesystem_overhead = 0.92  # written files are a bit bigger than in RAM
    adjusted_target_size_kb = target_size_kb * filesystem_overhead

    memories = parse_memories(file_path)

    if memories:
        reduced_memories = reduce_memories_to_target_size(
            memories, adjusted_target_size_kb
        )
        serialized_data = serialize_memories(reduced_memories)

        # Save the reduced memories to a new file to preserve the original
        reduced_file_path = (
            f"{target_size_kb}kb_structured_memories_randomly_pruned.txt"
        )
        with open(reduced_file_path, "w", encoding="utf-8") as file:
            file.write(serialized_data)

        print(
            f"Reduced memories saved to '{reduced_file_path}'. Final size: {len(serialized_data.encode('utf-8')) / 1024:.2f} KB"
        )
    else:
        print("No memories loaded. Please check the input file.")
