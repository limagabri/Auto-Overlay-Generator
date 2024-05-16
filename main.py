import os
import cv2
import re

# Function to list available image files in the current directory
# Função para listar os arquivos de imagem disponíveis no diretório atual
def list_image_files(directory="."):
    image_files = [file for file in os.listdir(directory) if file.endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
    return image_files

# Function to add text to the image
# Função para adicionar texto à imagem
def add_text(image, text, position, font, font_scale, color, thickness=1, line_type=cv2.LINE_AA):
    (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, thickness)
    text_x = int(position[0] - text_width / 2)
    text_y = int(position[1] + text_height / 2)
    cv2.putText(image, text, (text_x, text_y), font, font_scale, color, thickness, line_type)

# Function to convert hexadecimal code to RGB
# Função para converter código hexadecimal para RGB
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# Function to choose color based on name or hexadecimal code
# Função para escolher cor baseada no nome ou código hexadecimal
def choose_color(color_input):
    color_input = color_input.lower()
    predefined_colors = {
        "red": (0, 0, 255),    # Red / Vermelho
        "blue": (255, 0, 0),   # Blue / Azul
        "white": (255, 255, 255)  # White / Branco
    }
    if color_input in predefined_colors:
        return predefined_colors[color_input]
    elif re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color_input):
        return hex_to_rgb(color_input)
    else:
        return None

# Function to validate input as a number within a specific range
# Função para validar a entrada como um número dentro de um intervalo específico
def validate_number_input(prompt, min_value, max_value):
    while True:
        user_input = input(prompt)
        if user_input.isdigit():
            user_input = int(user_input)
            if min_value <= user_input <= max_value:
                return user_input
        print(f"Please enter a number between {min_value} and {max_value}.")

# Function to validate input as a floating point number
# Função para validar a entrada como um número de ponto flutuante
def validate_float_input(prompt, min_value, max_value):
    while True:
        user_input = input(prompt)
        try:
            user_input = float(user_input)
            if min_value <= user_input <= max_value:
                return user_input
        except ValueError:
            pass
        print(f"Please enter a number between {min_value} and {max_value}.")

# Function to validate input as text to restart or terminate the program
# Função para validar a entrada como texto para reiniciar ou encerrar o programa
def validate_choice_input(prompt, choices):
    while True:
        user_input = input(prompt).lower()
        if user_input in choices:
            return user_input
        print(f"Please enter '{choices[0]}' to restart or '{choices[1]}' to finish.")

# Main function
# Função principal
def main():
    while True:
        # List available image files in the current directory
        # Listar os arquivos de imagem disponíveis no diretório atual
        image_files = list_image_files()
        if not image_files:
            print("No image files available in this folder. Please add images to the correct folder.")
            return

        # Display available image files for user to choose
        # Mostrar os arquivos de imagem disponíveis para o usuário escolher
        print("Available images:")
        for i, image_file in enumerate(image_files, start=1):
            print(f"{i}. {image_file}")

        # Allow user to choose the image
        # Permitir que o usuário escolha a imagem
        image_choice_index = validate_number_input("Enter the number of the desired image: ", 1, len(image_files)) - 1
        chosen_image_path = image_files[image_choice_index]

        # Load the background image
        # Carregar a imagem de fundo
        background_image = cv2.imread(chosen_image_path)
        image_height, image_width = background_image.shape[0], background_image.shape[1]

        # Prompt user to input title and hashtag number
        # Solicitar ao usuário que insira o título e o número da hashtag
        title = input("Enter the title: ")
        hashtag_text = validate_number_input("Enter the hashtag number (without #): ", 0, 99999)
        hashtag = f"#{hashtag_text}"

        # Choose the font
        # Escolher a fonte
        font_choices = [
            "FONT_HERSHEY_SIMPLEX",
            "FONT_HERSHEY_PLAIN",
            "FONT_HERSHEY_DUPLEX",
            "FONT_HERSHEY_COMPLEX",
            "FONT_HERSHEY_TRIPLEX",
            "FONT_HERSHEY_COMPLEX_SMALL",
            "FONT_HERSHEY_SCRIPT_SIMPLEX",
            "FONT_HERSHEY_SCRIPT_COMPLEX"
        ]
        print("Choose the font:")
        for i, font in enumerate(font_choices, start=1):
            print(f"{i}. {font}")
        font_choice_index = validate_number_input("Enter the number of the desired font: ", 1, len(font_choices)) - 1
        chosen_font = getattr(cv2, font_choices[font_choice_index])

        # Allow user to choose the text size
        # Permitir que o usuário escolha o tamanho do texto
        font_scale = validate_float_input("Enter the text size (default is 1.0): ", 0.1, 10)

        # Allow user to choose the text color
        # Permitir que o usuário escolha a cor do texto
        color_choice = input("Enter the name of the text color (red, blue, or white) or the hexadecimal code: ")
        color = choose_color(color_choice)
        while color is None:
            color_choice = input("Invalid color. Please enter again: ")
            color = choose_color(color_choice)

        # Define spacings
        # Definir os espaçamentos
        top_padding = int(image_height * 0.05)  # Spacing between top edge and text
        text_spacing = int(image_height * 0.05)  # Spacing between title and hashtag

        # Calculate text positions
        # Calcular posições do texto
        title_position = (image_width // 2, top_padding + int(image_height * 0.1))  # Title position
        hashtag_position = (image_width // 2, title_position[1] + text_spacing + int(image_height * 0.3))  # Hashtag position

        # Add text to the background image
        # Adicionar texto à imagem de fundo
        add_text(background_image, title, title_position, chosen_font, font_scale, color, thickness=2)
        add_text(background_image, hashtag, hashtag_position, chosen_font, font_scale, color, thickness=2)

        # Display the image with added text
        # Exibir a imagem com o texto adicionado
        cv2.imshow("Overlay Image", background_image)
        cv2.waitKey(0)

        # Save the image
        # Salvar a imagem
        while True:
            save_choice = input("Do you want to save the image? (y/n): ").lower()
            if save_choice == 'y' or save_choice == 'n':
                break
            else:
                print("Please enter 'y' to save or 'n' to not save.")

        if save_choice == 'y':
            save_path = input("Enter the file name and extension ('.jpg', '.jpeg', '.png', '.bmp'): ")
            cv2.imwrite(save_path, background_image)
            print("Image saved successfully!")

        # Option to restart or terminate the program
        # Opção de reiniciar ou encerrar o programa
        choice = validate_choice_input("Do you want to restart (r) or finish the program (f)? ", ['r', 'f'])
        if choice != 'r':
            break

if __name__ == "__main__":
    main()
