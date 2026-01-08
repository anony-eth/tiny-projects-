# Add this script in task schduler 
import pyautogui
import time
import os
import google.generativeai as genai
import sys

if getattr(sys, "frozen", False):
    app_path = os.path.dirname(sys.executable)  # If exe
else:
    app_path = os.path.dirname(os.path.abspath(__file__))  # If Python script

FILE_PATH = os.path.join(app_path, "list_of_searches.txt")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))  # type: ignore

GEMINI_PROMPT = "generate 150 unique and realistic search queries across various topics like news, sports, games, and entertainment, and present them as a simple, unformatted way without numbering, titles,placeholders."


def append_gemini_content_if_lines_met(filename: str = FILE_PATH):
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")  # type: ignore
        response = model.generate_content(GEMINI_PROMPT)
        generated_text = response.text.strip()

        with open(filename, "a", encoding="utf-8") as f:
            f.write(generated_text + "\n\n")

    except Exception as e:
        print(f"An error occurred during Gemini content generation or file write: {e}")


def auto_search(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File not found at '{file_path}'. Please update FILE_PATH.")
        return

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

        if len(lines) < 30:
            append_gemini_content_if_lines_met()
            with open(file_path, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
            # print(f"File now contains {len(lines)}.") # To check number of lines generated. 

    except Exception as e:
        print(f"Error processing file '{file_path}': {e}")
        return

    while True:
        try:
            # num_searches = int(input("How many searches do you want to make?: ")) //Comment to make .exe
            num_searches = 9 # Usual need
            if 0 < num_searches <= len(lines):
                break
            else:
                print("Invalid number.")
        except ValueError as e:
            print(f"Error! {e}")
        break

    selected_lines = lines[:num_searches]
    remaining_lines = lines[num_searches:]

    et = len(selected_lines) * 7 + 5
    # m, s = divmod(et, 60)
    # print(f"Performing {len(selected_lines)} searches Est. ~ {f'{m}m ' if m else ''}{s}s. \nPlease do not touch your mouse or keyboard.")
    print(f"{len(selected_lines)} searches, Time:- {et} s.")
    time.sleep(1)

    # pyautogui.press('win')
    # time.sleep(.1)

    for i, line in enumerate(selected_lines):
        pyautogui.write(line, interval=0.01)  # 0.02 -slow
        pyautogui.press("enter")
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                for line in remaining_lines:
                    f.write(line + "\n")
        except Exception as e:
            print(f"Error rewriting file '{file_path}': {e}")
        time.sleep(7)
        pyautogui.press("a")
        pyautogui.hotkey('ctrl','a')
    pyautogui.hotkey("ctrl", "l")  # Let the user know its completed.
    print("Done.")  # let the terminal show its over between you and him.


if __name__ == "__main__":
    if not os.path.exists(FILE_PATH):
        try:
            with open(FILE_PATH, "w", encoding="utf-8") as f:
                f.write("")
        except Exception as e:
            print(f"Error creating file '{FILE_PATH}': {e}")
            sys.exit(1)
    auto_search(FILE_PATH)
