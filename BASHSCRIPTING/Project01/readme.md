Create a complete project where your script reads quotes from a file (`quotes.txt`) and randomly displays one of them in red text.
### **Project Structure:**
```
projects/
│
├── project1.sh   # The main script file
└── quotes.txt    # The file containing quotes
```

### **Step 1: Create the `quotes.txt` File**
First, create a `quotes.txt` file containing some sample quotes. Here's a sample:
```
"Believe you can and you're halfway there." - Theodore Roosevelt
"The only way to do great work is to love what you do." - Steve Jobs
"The purpose of our lives is to be happy." - Dalai Lama
"Life is what happens when you're busy making other plans." - John Lennon
"Get busy living or get busy dying." - Stephen King
```
Save this file as `quotes.txt` in your `projects/` directory.

### **Step 2: Create the `project1.sh` Script**
Now, create your `project1.sh` script with the following content:
```
#!/bin/bash

# Description: This script reads quotes from a file and displays a random quote in red.

# Check if quotes.txt exists in the same directory as the script
if [ ! -f "quotes.txt" ]; then
    echo "Error: quotes.txt file not found!"
    exit 1
fi

# Read the quotes from the file into an array
IFS=$'\n' read -d '' -r -a ARRAY < quotes.txt

# Check if the array is not empty
if [ ${#ARRAY[@]} -eq 0 ]; then
    echo "Error: No quotes found in quotes.txt!"
    exit 1
fi

# Select a random quote from the array
RANDOM_QUOTE=${ARRAY[$RANDOM % ${#ARRAY[@]}]}

# Display the random quote in red color
echo -e "\e[31m$RANDOM_QUOTE\e[0m"
```

### **Explanation:**
- **File Check:** The script first checks if `quotes.txt` exists in the same directory. If not, it outputs an error and exits.
    
- **Reading Quotes:** The script reads the entire `quotes.txt` file into an array, where each line represents an array element.
    
- **Empty File Check:** The script checks if the array is empty, which would indicate that `quotes.txt` has no content. If so, it exits with an error message.
    
- **Random Selection:** A random quote is selected from the array using `$RANDOM % ${#ARRAY[@]}`.
    
- **Display in Color:** The selected quote is displayed in red using `echo -e "\e[31m$RANDOM_QUOTE\e[0m"`.
    

### **Step 3: Make the Script Executable**
Before running the script, you need to make it executable:
`chmod +x project1.sh`

### **Step 4: Run the Script**

Finally, you can run the script:
`./project1.sh`

### **Output Example:**

When you run the script, you might see output like this:
`"Life is what happens when you're busy making other plans." - John Lennon`

The quote will be displayed in red text.

### **Notes:**
- **Adding More Quotes:** You can add as many quotes as you want to `quotes.txt`. Each quote should be on a new line.
- **Customization:** You can easily change the color by modifying the ANSI color code (`\e[31m` for red) in the script.

### **Sample `quotes.txt`:**
Here is a more detailed version of the `quotes.txt` file:
```
"Believe you can and you're halfway there." - Theodore Roosevelt
"The only way to do great work is to love what you do." - Steve Jobs
"The purpose of our lives is to be happy." - Dalai Lama
"Life is what happens when you're busy making other plans." - John Lennon
"Get busy living or get busy dying." - Stephen King
"Success is not final, failure is not fatal: It is the courage to continue that counts." - Winston Churchill
"You have within you right now, everything you need to deal with whatever the world can throw at you." - Brian Tracy
"Be yourself; everyone else is already taken." - Oscar Wilde
"Two things are infinite: the universe and human stupidity; and I'm not sure about the universe." - Albert Einstein
"In the end, we will remember not the words of our enemies, but the silence of our friends." - Martin Luther King Jr.
```

### **Conclusion:**
This project is a simple yet effective way to familiarize yourself with reading files, working with arrays, and adding some fun by displaying colorful output in Bash. You can further enhance it by adding more features like user input for selecting specific quotes or logging the displayed quotes to a file.