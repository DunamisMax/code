#include <stdio.h>
#include <limits.h> 
#include <stdbool.h> // For using bool type

// Function to get a valid integer input from the user
int get_valid_integer(const char *prompt) {
    int value;
    while (true) {
        printf("%s", prompt);
        if (scanf("%d", &value) == 1 && value > 0) {
            return value;
        }
        printf("Invalid input. Please enter a positive integer.\n");
        fflush(stdin);
    }
}

// Function to calculate the area of a rectangle
int calculate_area(int length, int width) {
    // Check for potential overflow
    if (length > INT_MAX / width) {
        printf("Error: Dimensions may cause integer overflow!\n");
        return -1; 
    }
    return length * width;
}

int main() {
    bool do_continue = true; // Use bool for clarity

    while (do_continue) {
        int length = get_valid_integer("Enter the length of the rectangle: ");
        int width = get_valid_integer("Enter the width of the rectangle: ");

        int area = calculate_area(length, width);

        if (area == -1) {
            continue; // Skip to the next iteration if there was an error
        } 

        printf("The area of the rectangle is: %d\n", area);

        char continue_choice;
        printf("Calculate another area? (y/n): ");
        scanf(" %c", &continue_choice);
        do_continue = (continue_choice == 'y');
    }

    return 0;
}
