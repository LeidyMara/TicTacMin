import tkinter as tk
from tkinter import messagebox

# Crear ventana principal
root = tk.Tk()
root.title("Tic Tac Toe - MinMax")

# Configuración del tamaño de los botones y la ventana
button_size = 200
canvas_size = button_size * 3

# Estado inicial del tablero
board = [["", "", ""],
         ["", "", ""],
         ["", "", ""]]

# Función para verificar si hay un ganador
def check_winner():
    # Verificar filas y columnas
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "":
            return True, [(i, 0), (i, 1), (i, 2)]  # Ganador en fila i
        if board[0][i] == board[1][i] == board[2][i] != "":
            return True, [(0, i), (1, i), (2, i)]  # Ganador en columna i

    # Verificar diagonales
    if board[0][0] == board[1][1] == board[2][2] != "":
        return True, [(0, 0), (1, 1), (2, 2)]  # Ganador en diagonal principal
    if board[0][2] == board[1][1] == board[2][0] != "":
        return True, [(0, 2), (1, 1), (2, 0)]  # Ganador en diagonal secundaria

    return False, []

# Función para verificar si el tablero está lleno
def is_board_full():
    for row in board:
        if "" in row:
            return False
    return True

# Función para determinar el resultado de la partida (ganador o empate)
def game_result():
    winner, winning_cells = check_winner()
    if winner:
        highlight_winner(winning_cells)
        show_winner_dialog(board[winning_cells[0][0]][winning_cells[0][1]])
        reset_game()
    elif is_board_full():
        show_winner_dialog("Empate")
        reset_game()

# Función para mostrar el cuadro de diálogo del ganador
def show_winner_dialog(winner):
    if winner == "Empate":
        messagebox.showinfo("Resultado", "¡Empate!")
    else:
        messagebox.showinfo("Resultado", f"¡El jugador {winner} ha ganado!")

# Función para resaltar las casillas ganadoras con una línea
def highlight_winner(cells):
    winner_color = "tan1" if board[cells[0][0]][cells[0][1]] == "X" else "salmon4"

    # Dibujar una línea sobre las celdas ganadoras
    for cell in cells:
        row, col = cell
        if row == col:
            canvas.create_line(col * button_size + 10, row * button_size + 10,
                               (col + 1) * button_size - 10, (row + 1) * button_size - 10,
                               fill=winner_color, width=5)
        if row + col == 2:
            canvas.create_line((col + 1) * button_size - 10, row * button_size + 10,
                               col * button_size + 10, (row + 1) * button_size - 10,
                               fill=winner_color, width=5)

# Función para reiniciar el juego
def reset_game():
    global board
    board = [["", "", ""],
             ["", "", ""],
             ["", "", ""]]
    canvas.delete("all")
    draw_board()

# Función para manejar el clic en un botón (jugada humana)
def on_click(row, col):
    if board[row][col] == "":
        board[row][col] = "X"
        draw_board()
        game_result()
        if not is_board_full():
            ai_move()  # Después de la jugada del humano, la IA realiza su movimiento

# Función para dibujar el tablero y los botones
def draw_board():
    canvas.delete("all")
    for i in range(3):
        for j in range(3):
            x1, y1 = j * button_size, i * button_size
            x2, y2 = (j + 1) * button_size, (i + 1) * button_size
            canvas.create_rectangle(x1, y1, x2, y2, outline="Black", width=2)

            # Dibujar 'X' y 'O'
            if board[i][j] == "X":
                canvas.create_line(x1 + 10, y1 + 10, x2 - 10, y2 - 10, fill="tan1", width=3)
                canvas.create_line(x1 + 10, y2 - 10, x2 - 10, y1 + 10, fill="tan1", width=3)
            elif board[i][j] == "O":
                canvas.create_oval(x1 + 10, y1 + 10, x2 - 10, y2 - 10, outline="salmon4", width=3)

# Función para que la IA (círculo) realice su movimiento
def ai_move():
    best_score = -float('inf')
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == "":
                board[i][j] = "O"
                score = minimax(board, 0, False)
                board[i][j] = ""
                if score > best_score:
                    best_score = score
                    move = (i, j)

    if move:
        row, col = move
        board[row][col] = "O"
        draw_board()
        game_result()

# Implementación del algoritmo Minimax para la IA
def minimax(board, depth, is_maximizing):
    if check_winner()[0]:
        if is_maximizing:
            return -1  # Si el jugador X (IA) gana, es malo para la IA (círculo)
        else:
            return 1  # Si el jugador O (humano) gana, es bueno para la IA (círculo)
    elif is_board_full():
        return 0  # Empate

    if is_maximizing:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "O"
                    score = minimax(board, depth + 1, False)
                    board[i][j] = ""
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "X"
                    score = minimax(board, depth + 1, True)
                    board[i][j] = ""
                    best_score = min(score, best_score)
        return best_score

# Crear y posicionar el lienzo (canvas) en la ventana
canvas = tk.Canvas(root, width=canvas_size, height=canvas_size, bg="pale goldenrod")
canvas.pack()

# Dibujar el tablero inicial
draw_board()

# Manejar el clic en el lienzo (detectar clic en una celda del tablero)
def canvas_click(event):
    col = event.x // button_size
    row = event.y // button_size
    on_click(row, col)

canvas.bind("<Button-1>", canvas_click)

# Obtener el ancho y alto de la pantalla
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calcular las coordenadas para centrar la ventana
x = (screen_width - root.winfo_reqwidth()) / 3
y = (screen_height - root.winfo_reqheight()) * -1

# Establecer las coordenadas de la ventana
root.geometry("+%d+%d" % (x, y))

# Ejecutar la ventana principal
root.mainloop()
